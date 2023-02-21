"""
Module for signal and slot related functions
"""
from typing import Any, Callable




class Signal:
    """
    A signal object that can be used to connect callbacks.
    - Simply connect a callback using `.connect(...)` method
    - Emit the signal using `.emit(...)` method: All connected callbacks will run with given args and kwargs

    Attributes:
        - _callbacks: list of callback functions that are connected to this signal
    """

    def __init__(self):
        self._callbacks: list[Callable] = []

    def __iadd__(self, callback: Callable) -> "Signal":
        """
        Connect `callback` function to signal using the += operator.
        """
        self.connect(callback)
        return self

    def __isub__(self, callback: Callable) -> "Signal":
        """
        Disconnect `callback` function from signal (if present) using the -= operator
        """
        self.disconnect(callback)
        return self


    def connect(self, callback: Callable):
        """ Connect `callback` function to signal """
        self._callbacks.append(callback)

    def disconnect(self, callback: Callable):
        """ Disconnect `callback` function from signal (if present) """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def disconnect_all(self):
        """ Disconnect all callback functions from signal """
        self._callbacks.clear()
    
    def emit(self, *args: Any, **kwargs: Any):
        """
        Emit the signal with the given arguments
        - All connected callback functions will be called with the given arguments
        """
        for callback in self._callbacks:
            callback(*args, **kwargs)

    def count(self) -> int:
        """ Returns the number of connected callback functions """
        return len(self._callbacks)

