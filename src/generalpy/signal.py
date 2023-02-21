"""
Module for signal and slot related functions
"""
from typing import Any, Callable




class Signal:
    """
    A signal object that can be used to connect callback.
    - Connect a callback using `.connect(...)` method
        - Newer callback will overwrite the older callback
    - Emit the signal using `.emit(...)` method to run the connected callback
    
    Args:
        - `name`: Name of the signal
    """

    def __init__(self, name = 'Signal'):
        self._callback: Callable | None = None
        self.name = name
    
    def __repr__(self) -> str:
        from .general import generate_repr_str
        return generate_repr_str(
            self, 'name'
        )

    def connect(self, callback: Callable):
        """ Connect `callback` to signal """
        self._callback = callback

    def disconnect(self, callback: Callable, ignoreError = False):
        """ 
        Disconnect `callback` from signal
        - raise `ValueError`, if `callback` is not connected to signal
        - If `ignoreError = True`, `ValueError` won't be raised
        """
        if self._callback != callback:
            if ignoreError:
                return
            raise ValueError(f'"{callback.__name__}" is not connected to "{self.name}" signal')
        self._callback = None

    def emit(self, *args: Any, **kwargs: Any):
        """
        Emit the signal with the given arguments
        - Connect callback will be called with the given arguments (if present)
        """
        if self._callback:
            self._callback(*args, **kwargs)

