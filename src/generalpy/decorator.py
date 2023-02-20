""" 
This module contains decorators 
"""
import logging
import sys
import threading
import time
from typing import Callable, Any

"""
Items imported inside functions/classes

- from .custom_logging import CustomLogging
"""




def combine_single_items(func: Callable):
    """
    Decorator to combine item of sublists (which contain only one item) in a single sublist.
    - New sublist would be attached in last
    - Ex: `[['a'], ['b'], ['c', 'd']]` -> `[['c', 'd'], ['a', 'b']]`

    Args:
    - `func` (decorated function): It must return `list[list[str]]`
    """
    def wrapper(*args, **kwargs) -> list[list[str]]:
        # Get lists
        lists: list[list[str]] = func(*args, **kwargs)

        # Parsing
        combined_list: list[list[str]] = []
        single_items: list[str] = []
        for sublist in lists:
            if len(sublist) == 1:
                single_items.extend(sublist)
            else:
                combined_list.append(sublist)
        if single_items:
            combined_list.append(single_items)

        return combined_list
    return wrapper



def conditional(condition: bool, defaultValue: Any = None):
    """ 
    Decorator to run the decorated function and return it's value, only when `condition=True`
    - Otherwise, `defaultValue` would be returned without running the decorated function
    """
    def top_level_wrapper(func:Callable):
        def wrapper(*args, **kwargs):
            if condition:
                return func(
                    *args, **kwargs
                )
            return defaultValue
        return wrapper
    return top_level_wrapper



def platform_specific(*supportedPlatforms: str):
    """
    Decorator to run decorated function only if current platform is one of the `supportedPlatforms`
    """
    def check_platform():
        if sys.platform not in supportedPlatforms:
            spfs = ', '.join(supportedPlatforms) if supportedPlatforms else 'None'
            raise Exception(
                f"This function is only supported on: {spfs}. "
                f"Your platform ({sys.platform}) is not supported."
            )
    
    def top_level_wrapper(func: Callable):
        def wrapper(*args, **kwargs):
            check_platform()
            return func(*args, **kwargs)
        return wrapper
    return top_level_wrapper



def retry_support(
    num: int = 3, 
    logger: logging.Logger | None = None,
    onFailure: Callable[[Exception], Any] | None = None,
    retryWait: float = 1
):
    """
    Decorator to retry the decorated function `num` times
    - Retry occurs, if any `Exception` occurs in decorated function
    - Retry occurs by `retryWait` seconds gap
    - After `num` retries, if error is still raised:
        - If `onFailure` present: This function will run (exception will be passed to that value), else
        - That same exception will be re-raised
    """
    if logger is None:
        from .custom_logging import CustomLogging
        logger = CustomLogging(loggingLevel=logging.DEBUG).logger
    
    def top_lvl_wrapper(fctn: Callable):
        def wrapper(*args, **kwargs):
            _retries = 0
            while True:
                try:
                    rv = fctn(*args, **kwargs)
                except Exception as e:
                    _retries += 1
                    if _retries > num:
                        logger.debug(f'[Retry - limit reached] {fctn.__name__}. Re-raising Error: ({type(e).__name__}) {e}')
                        if onFailure:
                            onFailure(e)
                        else:
                            raise
                    logger.error(f'[Retry - {_retries}] {fctn.__name__}. Error: ({type(e).__name__}) {e}')
                    time.sleep(retryWait)
                else:
                    return rv
        return wrapper
    return top_lvl_wrapper



def run_threaded(
    daemon: bool = True,
    name: str = 'Decorator thread', 
    logger: logging.Logger | None = None
):
    """ 
    Decorator to run the decorated function in a new thread 

    Args:
    - `daemon`: If thread should be daemon or not
    - `name`: Name of the new thread
    - `logger`: for logging purposes
    """
    if logger is None:
        from .custom_logging import CustomLogging
        logger = CustomLogging(loggingLevel=logging.DEBUG).logger
        
    def top_level_wrapper(func:Callable):
        def wrapper(*args, **kwargs):
            def main_function():
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    logger.exception(e)
                    raise
            return threading.Thread(
                target=main_function,
                name=name,
                daemon=daemon
            ).start()
        return wrapper
    return top_level_wrapper



def time_it(func):
    """
    Decorator to print time taken by the decorated function
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        rv = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'[Time taken: {end - start} seconds]')
        return rv
    return wrapper
