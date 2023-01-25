""" 
This module contains decorators 
"""
import threading
from logging import Logger
from typing import Callable, Any




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



def run_threaded(
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
            def main_function():
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    if logger:
                        logger.exception(e)
                    raise
            return threading.Thread(
                target=main_function,
                name=name,
                daemon=daemon
            ).start()
        return wrapper
    return top_level_wrapper



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


