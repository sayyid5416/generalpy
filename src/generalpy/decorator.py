""" This module contains decorators """
from typing import Callable, Any




def availability_check(checker: bool, defaultValue: Any = None):
    """ 
    This decorator runs the decorated function and return it's value, only when `checker=True`
    - Otherwise, `defaultValue` would be returned without running the decorated function
    """
    def top_level_wrapper(func:Callable):
        def wrapper(*args, **kwargs):
            if checker:
                return func(
                    *args, **kwargs
                )
            return defaultValue
        return wrapper
    return top_level_wrapper

