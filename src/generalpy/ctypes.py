""" This module contains ctypes related functions and classes """

import ctypes

# This import could not be done inside any function.
# So, be aware of circular imports.
from .decorator import platform_specific






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


