"""Base classes for IO to/from SLURM python jobs
"""

import logging
from contextlib import contextmanager
from numbers import Number
from typing import Any, List, Optional, Tuple
from weakref import proxy
from weakref import WeakValueDictionary
from ..errors import CancelledResultError
from ..errors import PendingResultError

logger = logging.getLogger(__name__)


class Future:
    """Mimic `concurrent.futures` API"""

    def __init__(self, job_id: int, api_object=None) -> None:
        self.job_id = job_id
        self._api_object = api_object

    def __repr__(self):
        return f"{type(self).__name__}({self.job_id})"

    def cancel(self) -> bool:
        """Non-blocking and returns `True` when cancelled.
        The SLURM job is not affected.
        """
        raise NotImplementedError

    def cancel_job(self) -> None:
        """Cancel the SLURM job"""
        try:
            if self._api_object is None:
                return None
            return self._api_object.cancel_job(self.job_id)
        except ReferenceError:
            pass

    def job_status(self) -> None:
        try:
            if self._api_object is None:
                return None
            return self._api_object.get_status(self.job_id)
        except ReferenceError:
            pass

    def result(self, timeout: Optional[Number] = None) -> Any:
        """Waits for the result indefinitely by default.

        :raises:
            PendingResultError: the job is not finished
            CancelledResultError: the job IO was cancelled
            Exception: the exception raised by the job
        """
        raise NotImplementedError

    def exception(self, timeout: Optional[Number] = None) -> Optional[Exception]:
        """Waits for the result indefinitely by default.

        :raises:
            PendingResultError: the job is not finished
            CancelledResultError: the job IO was cancelled
        """
        raise NotImplementedError

    def done(self) -> bool:
        raise NotImplementedError

    def cancelled(self) -> bool:
        raise NotImplementedError

    def wait(self, timeout: Optional[Number] = None) -> bool:
        try:
            self.exception(timeout=timeout)
        except PendingResultError:
            return False
        except CancelledResultError:
            return True
        return True


class JobIoHandler:
    def __init__(self, api_object=None) -> None:
        if api_object is None:
            self._api_object = None
        else:
            self._api_object = proxy(api_object)
        self._futures = WeakValueDictionary()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False

    def get_future(self, job_id: int) -> Optional[Future]:
        return self._futures.get(job_id, None)

    @contextmanager
    def start_job_io(
        self, data: Any, timeout: Optional[Number] = None
    ) -> Tuple[str, dict, Future]:
        """Returns the script, environment variables and pending result parameters"""
        raise NotImplementedError

    def _finalize_start_job_io(self, future: Future):
        if future.job_id < 0:
            future.cancel()
            return
        self._futures[future.job_id] = future

    def shutdown(self, wait: bool = True, cancel_futures: bool = False) -> None:
        logger.debug("Shutdown %s ...", type(self).__name__)
        for future in list(self._futures.values()):
            if cancel_futures:
                future.cancel()
            elif wait:
                try:
                    future.exception()
                except CancelledResultError:
                    pass
        logger.debug("Shutdown %s finished", type(self).__name__)

    def get_job_ids(self) -> List[str]:
        """Only the jobs with active futures"""
        return list(self._futures)

    def worker_count(self):
        raise NotImplementedError
