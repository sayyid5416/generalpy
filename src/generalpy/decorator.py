""" 
This module contains decorators 
"""
import asyncio
import logging
import sys
import threading
import time
from functools import wraps
from typing import Callable, Any

from ._utils import _get_basic_logger







def combine_single_items(func):
    """
    Decorator to combine item of sublists (which contain only one item) in a single sublist.
    - New sublist would be attached in last
    - Ex: `[['a'], ['b'], ['c', 'd']]` -> `[['c', 'd'], ['a', 'b']]`

    Args:
    - `func` (decorated function): It must return `list[list[str]]`
    """
    @wraps(func)
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
    - Supports both `sync` and `async` methods
    """
    def top_level_wrapper(func):
        
        @wraps(func)
        def wrapper_sync(*args, **kwargs):
            if condition:
                return func(*args, **kwargs)
            return defaultValue
        
        @wraps(func)
        async def wrapper_async(*args, **kwargs):
            if condition:
                return await func(*args, **kwargs)
            return defaultValue
        
        if asyncio.iscoroutinefunction(func):
            return wrapper_async
        else:
            return wrapper_sync
        
    return top_level_wrapper



def log_it(logger: logging.Logger | None = None):
    """
    Decorator to log when the decorated function runs and what it returns
    
    - `logger`: for logging purposes (if not provided, default logger will be used)
    """
    
    logger = logger or _get_basic_logger()
    
    def top_level_wrapper(func):
        def wrapper(*args, **kwargs):
            # Function
            t1 = time.perf_counter()
            retVal = func(*args, **kwargs)
            t2 = time.perf_counter()

            # Log
            logger.info(f'[LOG_IT] "{func.__name__}" ran and returned "{retVal}" [Time taken: {t2 - t1} seconds]')

            return retVal
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
    
    def top_level_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            check_platform()
            return func(*args, **kwargs)
        return wrapper
    return top_level_wrapper



def retry_support(
    num: int = 3, 
    logger: logging.Logger | None = None,
    onFailure: Callable[[Exception], Any] | None = None,
    retryWait: float = 1,
    exponentialTime: bool = False,
    ignore: tuple[type[Exception], ...] | None = None
):
    """
    Decorator to retry the decorated function `num` times.

    - Retry occurs if any `Exception` occurs in the decorated function.
    - Retry occurs with a gap of `retryWait` seconds.
    
    - After `num` retries, if an error is still raised:
        - If `onFailure` is present: This function will run (exception will be passed to that value), else
        - That same exception will be re-raised.

    Parameters:
    - `num` (int): Number of retry attempts.
    - `logger` (Logger | None): Logger instance for logging purposes. If None, a basic logger will be used.
    - `onFailure` (Callable[[Exception], Any] | None): Optional function to run when retries are exhausted.
    - `retryWait` (float): Time to wait between retries in seconds.
    - `exponentialTime` (bool): If True, retry time will increase exponentially with each attempt.
    - `ignore` (tuple[type[Exception], ...] | None): Exceptions to ignore and not trigger retries.

    NOTE: This decorator can handle both `sync` and `async` methods, but both the decorated method and the 'onFailure' method should be of the same type.
    """
    logger = logger or _get_basic_logger()
    ignore = ignore or tuple()

    def top_lvl_wrapper(func):

        # Checks
        if onFailure is not None:
            if asyncio.iscoroutinefunction(func) != asyncio.iscoroutinefunction(onFailure):
                raise ValueError(f'[retry_support decorator] Both decorated function and onFailure function should be of same type, either sync or async')

        def _retry_on_failure(e: Exception):
            if onFailure is None:
                logger.debug(f'[Retry - limit reached] {func.__name__}. Re-raising Error: ({type(e).__name__}) {e}')
                logger.exception(e)
                raise
            logger.debug(f'[Retry - limit reached] {func.__name__}. Running "{onFailure}" function for Error: ({type(e).__name__}) {e}')
        
        def _retry_time(retrialNum: int, e: Exception):
            logger.error(f'[Retry - {retrialNum}] {func.__name__}. Error: ({type(e).__name__}) {e}')
            sleepTime = (retryWait * (2 ** retrialNum)) if exponentialTime else retryWait
            return sleepTime

        @wraps(func)
        async def wrapper_async(*args, **kwargs):
            _retries = 0
            while True:
                try:
                    rv = await func(*args, **kwargs)
                except Exception as e:
                    if isinstance(e, ignore):
                        raise
                    if _retries >= num:
                        _retry_on_failure(e)
                        await onFailure(e)
                        return
                    await asyncio.sleep(_retry_time(_retries, e))
                    _retries += 1
                else:
                    return rv

        @wraps(func)
        def wrapper_sync(*args, **kwargs):
            _retries = 0
            while True:
                try:
                    rv = func(*args, **kwargs)
                except Exception as e:
                    if isinstance(e, ignore):
                        raise
                    if _retries >= num:
                        _retry_on_failure(e)
                        onFailure(e)
                        return
                    time.sleep(_retry_time(_retries, e))
                    _retries += 1
                else:
                    return rv

        # Return the appropriate wrapper based on whether the function is asynchronous
        if asyncio.iscoroutinefunction(func):
            return wrapper_async
        else:
            return wrapper_sync

    return top_lvl_wrapper



def run_threaded(
    daemon: bool = True,
    name: str = '', 
    logger: logging.Logger | None = None
):
    """ 
    Decorator to run the decorated function in a new thread 
    - Use `__wrapped__` attribute to run the main function without running a thread
    - This decorator can handle both `sync` and `async` methods, BUT remember async functions would be started using `asyncio.create_task` and NOT run in a different thread

    Args:
    - `daemon`: If thread should be daemon or not
    - `name`: Name of the new thread (by default decorated function `__name__` will be used)
    - `logger`: for logging purposes
    """
    logger = logger or _get_basic_logger()
    
    def top_level_wrapper(func):
        
        @wraps(func)
        def wrapper_sync(*args, **kwargs):
            def main_function():
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    logger.debug(f'Error occured in {func.__name__} threaded function: {e}')
                    logger.exception(e)
                    raise
            threading.Thread(target=main_function, name=name or func.__name__, daemon=daemon).start()
        
        @wraps(func)
        async def wrapper_async(*args, **kwargs):
            asyncio.create_task(func(*args, **kwargs), name=name or func.__name__)
        
        # Return
        if asyncio.iscoroutinefunction(func):
            return wrapper_async
        else:
            return wrapper_sync
    
    return top_level_wrapper

