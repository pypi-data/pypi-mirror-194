import time
from typing import Optional, Mapping
from ..client.pyscript import SlurmPythonJobApi
from ..client.job_io.base_io import Future


class SlurmExecutor:
    def __init__(
        self,
        api_object=None,
        pre_script: Optional[str] = None,
        post_script: Optional[str] = None,
        python_cmd: Optional[str] = None,
        parameters: Optional[Mapping] = None,
        request_options: Optional[Mapping] = None,
        **kw
    ) -> None:
        self.spawn_options = dict()
        self.spawn_options["pre_script"] = pre_script
        self.spawn_options["post_script"] = post_script
        self.spawn_options["python_cmd"] = python_cmd
        self.spawn_options["parameters"] = parameters
        self.spawn_options["request_options"] = request_options
        if api_object is None:
            self.pyapi = SlurmPythonJobApi(**kw)
        else:
            self.pyapi = api_object

    def submit(self, func, *args, _spawn_options=None, **kwargs) -> Future:
        spawnkw = dict(self.spawn_options)
        if _spawn_options:
            spawnkw.update(_spawn_options)
        return self.pyapi.spawn(func, args=args, kwargs=kwargs, **spawnkw)

    def map(self, fn, *iterables, timeout=None):
        """From `concurrent.future._base.Executor`

        Returns an iterator equivalent to map(fn, iter).

        Args:
            fn: A callable that will take as many arguments as there are
                passed iterables.
            timeout: The maximum number of seconds to wait. If None, then there
                is no limit on the wait time.

        Returns:
            An iterator equivalent to: map(func, *iterables) but the calls may
            be evaluated out-of-order.

        Raises:
            TimeoutError: If the entire result iterator could not be generated
                before the given timeout.
            Exception: If fn(*args) raises for any values.
        """
        if timeout is not None:
            end_time = timeout + time.monotonic()

        fs = [self.submit(fn, *args) for args in zip(*iterables)]

        # Yield must be hidden in closure so that the futures are submitted
        # before the first iterator value is required.
        def result_iterator():
            try:
                # reverse to keep finishing order
                fs.reverse()
                while fs:
                    # Careful not to keep a reference to the popped future
                    if timeout is None:
                        yield fs.pop().result()
                    else:
                        yield fs.pop().result(end_time - time.monotonic())
            finally:
                for future in fs:
                    future.cancel()

        return result_iterator()

    def shutdown(self, wait: bool = True, cancel_futures: bool = False):
        self.pyapi.cleanup(wait=wait, cancel_futures=cancel_futures)

    def __enter__(self):
        self.pyapi.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return self.pyapi.__exit__(exc_type, exc_val, exc_tb)
