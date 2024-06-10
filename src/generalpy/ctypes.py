""" This module contains ctypes related functions and classes """

import ctypes
from logging import Logger

from ._utils import _get_basic_logger

# This import could not be done inside any function.
# So, be aware of circular imports.
from .decorator import platform_specific










@platform_specific('win32')
def run_ShellExecuteW(verb: str, command: str, file: str=None):
    """
    Execute `ctypes.windll.shell32.ShellExecuteW(None, verb, command, file, None, 1)`
    - Raises `ValueError` on error
    - Ex: `_shell_execute_W('runas', sys.executable, __file__)`
    """
    # Execute the ShellExecuteW function
    result = ctypes.windll.shell32.ShellExecuteW(None, verb, command, file, None, 1)
    
    # Check the return value
    if result <= 32:
        # Map error codes to error messages
        error_messages = {
            0: "The operation failed.",
            2: "The specified file was not found.",
            3: "The specified path was not found.",
            5: "Access is denied.",
            8: "Not enough memory to complete the operation.",
            11: "Invalid .exe file.",
            26: "A sharing violation occurred.",
            27: "The file name association is incomplete or invalid.",
            28: "The DDE transaction timed out.",
            29: "The DDE transaction failed.",
            30: "Other DDE transactions were already in progress.",
            31: "There is no application associated with the specified file extension.",
            32: "The specified dynamic-link library (DLL) was not found."
        }
        # Get the error message corresponding to the result
        error_message = error_messages.get(result, f"Unknown error (code {result})")
        
        # Raise an exception with the error message
        raise ValueError(f"ShellExecuteW failed: {error_message}")



@platform_specific('win32')
def running_as_admin(logger: Logger=None):
    """ Check if the current process is running with administrative privileges. """
    logger = logger or _get_basic_logger()
    
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        logger.debug(f"Error checking admin privileges: {e}")
        return False



@platform_specific('win32')
def set_app_user_model_id(appID: str):
    """
    Sets the App User Model ID for the current process. It is:
    - setted using `SetCurrentProcessExplicitAppUserModelID` windows API.
    - a string that identifies a specific application to the Windows operating system.
    - used by Windows to group windows and taskbar items for a specific application, 
    as well as to launch and activate the application.
    """
    ctypes.windll.shell32.\
        SetCurrentProcessExplicitAppUserModelID(appID)


