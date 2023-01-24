""" This module contains decorators """
import threading
from logging import Logger
from typing import Callable, Any




def availability_check(checker: bool, defaultValue: Any = None):
    """ 
    Decorator to run the decorated function and return it's value, only when `checker=True`
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



def threaded(
    daemon: bool = True,
    name: str = 'Decorator thread', 
    logger: Logger | None = None
):
    """ 
    Decorator to run the decorated function in a new thread 

    Args:
    - `daemon`: If thread should be daemon or not
    - `name`: Name of the new thread
    - `logger`: `logging.Logger` to handle the `Exception`
    """
    def top_level_wrapper(func:Callable):
        def wrapper(*args, **kwargs):
            def newFucntion():
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    if logger:
                        logger.exception(e)
                    raise
            return threading.Thread(
                target=newFucntion,
                name=name,
                daemon=daemon
            ).start()
        return wrapper
    return top_level_wrapper
