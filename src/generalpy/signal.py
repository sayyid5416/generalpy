"""
Module for signal and slot related functions
"""
from logging import Logger
from typing import Any, Callable

"""
Items imported inside functions/classes

- from .decorator import run_threaded
- from .general import generate_repr_str
"""



class Signal:
    """
    A signal object that can be used to connect callbacks and emit signals.
    - Connect a callback using `.connect(...)` method
        - Newer callback will overwrite the older callback
    - Emit the signal using `.emit(...)` method to run the connected callback
    
    Args:
        - `name`: Name of the signal
        - `threaded`: Emit the signal in a new thread
        - `daemon`: If `threaded`, thread should be daemon or not
        - `logger`: `Logger` to be used for logging
    """

    def __init__(
        self, name = 'Signal',
        threaded = False,
        daemon = False,
        logger: Logger | None = None
    ):
        # Mods
        if logger is None:
            from ._utils import _get_basic_logger
            logger = _get_basic_logger()

        # Args
        self.name = name
        self.threaded = threaded
        self.daemon = daemon
        self.logger = logger

        # Data
        self._callback: Callable | None = None
        self.cb_args = tuple()
        self.cb_kwargs = dict()
        self.returnedValue_from_cb = None
        self._set_default_values()
    
    def __repr__(self) -> str:
        from .general import generate_repr_str
        return generate_repr_str(
            self, 'name', 'threaded', 'daemon', 'logger'
        )
    
    def _set_default_values(self):
        """ Sets the default values for items """
        self._callback = None
        self.cb_args = tuple()
        self.cb_kwargs = dict()
        self.returnedValue_from_cb = None

    def connect(self, callback: Callable, defaultReturnValue: Any = None, *args, **kwargs):
        """ 
        Connect `callback` to signal 
        - `defaultReturnValue`: This value will be returned on `.get_returned_value()` 
        if callback has not been emitted yet.
        - `args`, `kwargs`: They would be passed to callback on runtime
        """
        self._callback = callback
        self.cb_args = args
        self.cb_kwargs = kwargs
        self.returnedValue_from_cb = defaultReturnValue
        self.logger.debug(f'Callback "{callback.__name__}({args=}, {kwargs=})" setted for "{self.name}" signal')

    def disconnect(self, callback: Callable, ignoreError = False):
        """ 
        Disconnect `callback` from signal
        - raise `ValueError`, if `callback` is not connected to signal
        - If `ignoreError = True`, `ValueError` won't be raised
        """
        if self._callback != callback:
            if ignoreError:
                self.logger.debug(f'"{callback.__name__}" is not connected to "{self.name}" signal')
                return
            raise ValueError(f'"{callback.__name__}" is not connected to "{self.name}" signal')
        self.logger.debug(f'Removed "{callback.__name__}" from "{self.name}" signal')
        self._set_default_values()

    def emit(self, *args: Any, **kwargs: Any):
        """
        Emit the signal with the given arguments
        - Connected callback will run with `args` and `kwargs` (if present)
            - These `args` and `kwargs` be passed along with those which were set in `.connect(...)` method
            - These `kwargs` will take precedence (in case of duplication) over those which were set in `.connect(...)` method
            - Final Args would be like `(earlier_args, these_args, final_kwargs)`
        """
        # Modify
        _args = self.cb_args + args
        _kwargs = {**self.cb_kwargs, **kwargs}

        # Run
        if self._callback:
            if self.threaded:
                from .decorator import run_threaded
                run_threaded(
                    daemon=self.daemon,
                    name=f'Signal Thread {self._callback.__name__}',
                    logger=self.logger,
                )(self._callback)(*_args, **_kwargs)
            else:
                self.returnedValue_from_cb = self._callback(*_args, **_kwargs)

    async def emit_async(self, *args: Any, **kwargs: Any):
        """
        (`Async`) Emit the signal with the given arguments
        - Connected callback will run with `args` and `kwargs` (if present)
            - Callback will run using `async` and `await`
            - These `args` and `kwargs` be passed along with those which were set in `.connect(...)` method
            - These `kwargs` will take precedence (in case of duplication) over those which were set in `.connect(...)` method
            - Final Args would be like `(earlier_args, these_args, final_kwargs)`
        """
        # Modify
        _args = self.cb_args + args
        _kwargs = {**self.cb_kwargs, **kwargs}

        # Run
        if self._callback:
            self.returnedValue_from_cb = await self._callback(*args, **kwargs)

    def get_returned_value(self):
        """
        Returns the returned-value of connected callback
        - you must use `.emit(...)` method first to run the callback
            - Else `defaultReturnValue` would be returned (which was set in `.connect(...)`)
        - It doesn't work if callback is running in a different thread (i.e using `threaded`)
        """
        return self.returnedValue_from_cb
