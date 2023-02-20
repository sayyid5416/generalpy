"""
This module is private, 
It's not recommanded to use it directly.
"""
import logging

"""
Items imported inside functions/classes

- from .custom_logging import CustomLogging
"""





def _get_basic_logger():
    """
    Returns `CustomLogging.logger`
    """
    from .custom_logging import CustomLogging
    return CustomLogging(
        loggingLevel=logging.DEBUG
    ).logger