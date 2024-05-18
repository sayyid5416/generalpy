"""
Module for signal and slot related functions
"""
import asyncio
import time
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
        self, 
        name = 'Signal',
        threaded = False,
        daemon = False,
        logger: Logger | None = None
    ):
        # Mods
        if logger is None:
            from ._utils import _get_basic_logger
            logger = _get_basic_logger()

        # Args
        self.__name = name
        self.__threaded = threaded
        self.__daemon = daemon
        self.__logger = logger

        # Data
        self.__connected_function_ran = False
        self.__returnedValue_from_cb = None
        self.disconnect()
    
    def __repr__(self) -> str:
        from .general import generate_repr_str
        return generate_repr_str(
            self, 'name', 'threaded', 'daemon', 'logger'
        )
    
    @property
    def name(self):
        return self.__name
    
    @property
    def logger(self):
        return self.__logger
    
    @logger.setter
    def logger(self, value: Logger):
        self.__logger = value
    
    def connect(self, callback: Callable, defaultReturnValue: Any = None, *args, **kwargs):
        """
        Connects a callback to the signal.
        
        Args:
            `callback`: The function to be connected.
            `defaultReturnValue`: The value to be returned if the callback has not been emitted yet.
            *args, **kwargs: Additional arguments to be passed to the callback.
        """
        self._callback = callback
        self.cb_args = args
        self.cb_kwargs = kwargs
        self.__returnedValue_from_cb = defaultReturnValue
        self.__connected_function_ran = False
        self.__logger.debug(f'Callback "{callback.__name__}({args=}, {kwargs=})" connected to "{self.__name}" signal')

    def disconnect(self):
        """ Disconnects a callback from the signal """
        self._callback: Callable | None = None
        self.cb_args = tuple()
        self.cb_kwargs = dict()
        self.__logger.debug(f'Callback disconnected from "{self.__name}" signal')

    def emit(self, *args: Any, **kwargs: Any):
        """
        Emits the signal with the given arguments.
            
        Args:
            *args: Positional arguments to be passed to the callback.
            **kwargs: Keyword arguments to be passed to the callback.
        Notes:
            - The connected callback will run synchronously unless it's in a separate thread (controlled by the 'threaded' attribute).
            - The final arguments passed to the callback are a combination of those set during connection and those provided during signal emission.
            - These `kwargs` will take precedence (in case of duplication) over those which were set in `.connect(...)` method
        """
        # Modify
        _args = self.cb_args + args
        _kwargs = {**self.cb_kwargs, **kwargs}

        # Run
        if self._callback:
            self.__connected_function_ran = False
            if self.__threaded:
                from .decorator import run_threaded
                run_threaded(
                    daemon=self.__daemon,
                    name=f'Signal Thread {self._callback.__name__}',
                    logger=self.__logger,
                )(self._callback)(*_args, **_kwargs)
            else:
                self.__returnedValue_from_cb = self._callback(*_args, **_kwargs)
            self.__connected_function_ran = True

    async def emit_async(self, *args: Any, **kwargs: Any):
        """
        Asynchronously emits the signal with the given arguments.

        Args:
            *args: Positional arguments to be passed to the callback.
            **kwargs: Keyword arguments to be passed to the callback.
        Notes:
            - The connected callback is expected to be an async function and will be awaited.
            - The final arguments passed to the callback are a combination of those set during connection and those provided during signal emission.
            - These `kwargs` will take precedence (in case of duplication) over those which were set in `.connect(...)` method
        """
        # Modify
        _args = self.cb_args + args
        _kwargs = {**self.cb_kwargs, **kwargs}

        # Run
        if self._callback:
            self.__connected_function_ran = False
            self.__returnedValue_from_cb = await self._callback(*args, **kwargs)
            self.__connected_function_ran = True

    def get_returned_value(self, returnAfterComplete: bool=False):
        """
        Returns the returned value of the connected callback.

        Args:
            `returnAfterComplete`: If True, waits until the callback has completed before returning the value.
        Notes:
            - Returns the `defaultReturnValue` (which was set in `.connect(...)`) if the callback is running in a different thread (i.e using `threaded`) or if `emit()` has not been called.
            - Setting `returnAfterComplete=True` will block the script until the callback has completed, except when the callback is running in a different thread.
            - Use `returnAfterComplete=True` with caution as it may block the execution flow indefinitely if the callback never completes.
        """
        if returnAfterComplete:
            while True:
                if self.__connected_function_ran:
                    break
                time.sleep(1)
        return self.__returnedValue_from_cb

    async def get_returned_value_async(self, returnAfterComplete: bool=False):
        """
        Returns the returned value of the connected callback.

        Args:
            `returnAfterComplete` (wait using `asyncio.sleep`) : If True, waits until the callback has completed before returning the value.
        Notes:
            - Returns the `defaultReturnValue` (which was set in `.connect(...)`) if the callback is running in a different thread (i.e using `threaded`) or if `emit()` has not been called.
            - Setting `returnAfterComplete=True` will block the script until the callback has completed, except when the callback is running in a different thread.
            - Use `returnAfterComplete=True` with caution as it may block the execution flow indefinitely if the callback never completes.
            - This method is asynchronous and requires await when calling it.
        """
        if returnAfterComplete:
            while True:
                if self.__connected_function_ran:
                    break
                await asyncio.sleep(1)
        return self.__returnedValue_from_cb
