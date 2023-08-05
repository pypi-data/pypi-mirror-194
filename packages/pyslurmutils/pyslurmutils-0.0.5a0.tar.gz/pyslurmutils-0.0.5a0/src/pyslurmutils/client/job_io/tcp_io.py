"""IO to/from SLURM python jobs over TCP
"""

import pickle
import socket
import time
import logging
import weakref
from numbers import Number
from contextlib import contextmanager
from typing import Any, Optional, Tuple
from threading import Event
from concurrent.futures import Future as ConcurrentFuture
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FutureTimeoutError
from concurrent.futures import CancelledError
from . import base_io
from .. import errors

logger = logging.getLogger(__name__)


class Future(base_io.Future):
    def __init__(
        self, job_id: int, future: ConcurrentFuture, stop: Event, api_object=None
    ) -> None:
        super().__init__(job_id, api_object=api_object)
        self._future = future
        self._stop = stop

    def done(self) -> bool:
        return self._future.done()

    def cancelled(self) -> bool:
        return self._future.cancelled()

    def cancel(self) -> bool:
        logger.debug("[JOB ID=%s] cancel SLURM job IO ...", self.job_id)
        self._stop.set()
        result = self._future.cancel()
        logger.debug("[JOB ID=%s] SLURM job IO cancelled", self.job_id)
        return result

    def shutdown(self) -> None:
        self._stop.set()

    def result(self, timeout: Optional[Number] = None) -> Any:
        """Waits for the result indefinitely by default.

        :raises:
            PendingResultError: the job is not finished
            CancelledResultError: the job IO was cancelled
            Exception: the exception raised by the job
        """
        try:
            result, tb = self._future.result(timeout=timeout)
        except FutureTimeoutError:
            raise errors.PendingResultError(
                f"SLURM job {self.job_id} has no result yet"
            ) from None
        except CancelledError:
            raise errors.CancelledResultError(
                f"SLURM job {self.job_id} IO was cancelled"
            ) from None
        if tb:
            errors.reraise_remote_slurm_error(result, tb)
        return result

    def exception(self, timeout: Optional[Number] = None) -> Optional[Exception]:
        """Waits for the result indefinitely by default.

        :raises:
            PendingResultError: the job is not finished
            CancelledResultError: the job IO was cancelled
        """
        try:
            exception = self._future.exception(timeout=timeout)
        except FutureTimeoutError:
            raise errors.PendingResultError(
                f"SLURM job {self.job_id} has no result yet"
            ) from None
        except CancelledError:
            raise errors.CancelledResultError(
                f"SLURM job {self.job_id} IO was cancelled"
            ) from None
        if exception is None:
            result, tb = self._future.result(timeout=timeout)
            if tb:
                return errors.get_remote_slurm_error(result, tb)
        return exception


class JobTcpIoHandler(base_io.JobIoHandler):
    def __init__(self, max_workers: Optional[int] = None, api_object=None) -> None:
        super().__init__()
        self.__executor = ThreadPoolExecutor(max_workers=max_workers)
        self._stop_events = weakref.WeakSet()
        if api_object is None:
            self._api_object = api_object
        else:
            self._api_object = weakref.proxy(api_object)

    def __enter__(self):
        self.__executor.__enter__()
        return super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.__executor.__exit__(exc_type, exc_val, exc_tb)
        return False

    def shutdown(self, wait: bool = True, cancel_futures: bool = False) -> None:
        for ev in list(self._stop_events):
            ev.set()
        super().shutdown(wait=wait, cancel_futures=cancel_futures)
        self.__executor.shutdown(wait=wait)

    @contextmanager
    def start_job_io(
        self, data: Any, timeout: Optional[Number] = None
    ) -> Tuple[str, dict, Future]:
        host, port = _get_free_port()
        online_event = Event()
        stop_event = Event()
        self._stop_events.add(stop_event)
        future = self.__executor.submit(
            _send_end_receive, host, port, data, online_event, stop_event
        )
        if not online_event.wait(timeout):
            raise TimeoutError(f"Job IO did not start in {timeout} seconds")
        future = Future(
            job_id=-1, future=future, stop=stop_event, api_object=self._api_object
        )
        environment = {
            "_PYSLURMUTILS_HOST": host,
            "_PYSLURMUTILS_PORT": port,
        }
        try:
            yield _PYTHON_SCRIPT, environment, future
        finally:
            self._finalize_start_job_io(future)

    def worker_count(self):
        return len(self.__executor._threads)


def _send_end_receive(
    host: str, port: int, data: Any, online_event: Event, stop_event: Event
) -> Any:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen()
        online_event.set()
        logger.debug("Wait until the SLURM job started and connected ...")
        sock.settimeout(0.5)
        conn = None
        while not stop_event.is_set():
            try:
                conn, _ = sock.accept()
                break
            except socket.timeout:
                pass
        if conn is None:
            raise errors.CancelledResultError(
                "Cancelled before making a connection to the SLURM job"
            )
        logger.debug("SLURM job connected. Send work ...")
        conn.settimeout(10)
        _send(conn, data)
        logger.debug("SLURM job work send, wait for result ...")
        conn.settimeout(None)
        result = _receive(conn, stop_event)
        logger.debug("SLURM job result received")
        return result


def _send(sock: socket.socket, data: Any) -> None:
    bdata = pickle.dumps(data)
    sock.sendall(len(bdata).to_bytes(4, "big"))
    sock.sendall(bdata)


def _receive(
    sock: socket.socket, stop_event: Event, period: Optional[Number] = None
) -> Any:
    data = _receive_nbytes(sock, 4, stop_event, period)
    nbytes = int.from_bytes(data, "big")
    data = _receive_nbytes(sock, nbytes, stop_event, period)
    if not data:
        raise errors.CancelledResultError(
            "SLURM job returned nothing (most likely cancelled)"
        )
    return pickle.loads(data)


def _receive_nbytes(
    sock: socket.socket, nbytes: int, stop_event: Event, period: Optional[Number] = None
) -> bytes:
    data = b""
    block = min(nbytes, 512)
    if period is None:
        period = 0.5
    while not stop_event.is_set() and len(data) < nbytes:
        data += sock.recv(block)
        time.sleep(period)
    return data


def _get_free_port() -> Tuple[str, int]:
    with socket.socket() as sock:
        sock.bind(("", 0))
        port = sock.getsockname()[-1]
        host = socket.gethostbyname(socket.gethostname())
        return host, port


def job_test_client(env, response=None):
    host = env.get("_PYSLURMUTILS_HOST")
    port = int(env.get("_PYSLURMUTILS_PORT"))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(10)
        s.connect((host, port))
        data = _receive(s, Event())
        if response is not None:
            _send(s, response)
        return data


_PYTHON_SCRIPT = """
import os,sys,pickle,socket,time,traceback
print("Python version: %s" % sys.version)
print("working directory: %s" % os.getcwd())

def send(s, data):
    bdata = pickle.dumps(data)
    nbytes = len(bdata)
    s.sendall(nbytes.to_bytes(4, "big"))
    s.sendall(bdata)

def receive_nbytes(s, nbytes):
    data = b""
    block = min(nbytes, 512)
    while len(data) < nbytes:
        data += s.recv(block)
        time.sleep(0.1)
    return data

def receive(s):
    data = receive_nbytes(s, 4)
    nbytes = int.from_bytes(data, "big")
    data = receive_nbytes(s, nbytes)
    return pickle.loads(data)

host = os.environ.get("_PYSLURMUTILS_HOST")
port = int(os.environ.get("_PYSLURMUTILS_PORT"))
try:
    hostname = socket.gethostbyaddr(host)[0]
except Exception:
    hostname = host
hostport = "%s:%s" % (hostname, port)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting to", hostport, "...")
    s.settimeout(10)
    s.connect((host, port))

    try:
        print("Receiving work from", hostport, "...")
        func, args, kw = receive(s)

        print("Executing work:", func)
        if args is None:
            args = tuple()
        if kw is None:
            kw = dict()
        result = func(*args, **kw)
        tb = None
    except Exception as e:
        traceback.print_exc()
        result = e
        tb = traceback.format_exc()

    print("Sending result", type(result), "to", hostport, "...")
    try:
        send(s, (result, tb))
    except Exception:
        traceback.print_exc()
        print("JOB succeeded but client went down first")
"""
