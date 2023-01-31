"""
This module contains general classes and methods
"""
import ctypes
from pathlib import Path
import re
import sys

# This import could not be done inside any function.
# So, be aware of circular imports.
from .decorator import platform_specific





def generate_repr_str(classInst, *args: str):
    """
    Returns a suitable string for `__repr__` method of classes.
    - Return format: `classInst(arg1 = arg1Value, arg2 = arg2Value, ...)`
    - `args` must be an attribute of `classInst`
    """
    info = ''
    for arg in args:
        info += f'{arg} = {getattr(classInst, arg)}, '
    info = info.strip().removesuffix(',')
    
    return f'{classInst.__class__.__name__}({info})'



def get_digit_from_text(text: str) -> int | None:
    """
    Returns the digit from the first occuurance of `(digit)`. 
    - For ex: `2` would be returned from `text='file(1 ) and file (2) and  file(3).txt'`
    - decimals are not supported
    """
    match = re.search(r'\(\d+\)', text)
    if match:
        val = match.group().removeprefix('(').removesuffix(')')
        if val.isdigit():
            return int(val)



def is_python() -> bool:
    """
    Returns: `True` if current running app is `python`
    """
    appPath = Path(sys.executable)
    appName = appPath.stem.lower()
    return appName == 'python' or appName == 'pythonw'



def replace_multiple_chars(
    text: str,
    old: list[str] | list[tuple[str, str]],
    new: str = '-',
    count: int=-1
):
    """ 
    Replace multiple characters from a string.
    - Returns `text` after replacing all items of `old` with `new`
    - If `old = list[tuple[str, str]]`: 
        - `new` would be ignored.
        - 1st item of tuple would be replaced 2nd item
    - `count`: 
        - Maximum number of occurrences to replace. 
        - Default = -1 : means replace all occurrences.
    """
    for i in old:
        if isinstance(i, str):
            text = text.replace(
                i, new, count
            )
        else:
            text = text.replace(
                i[0], i[1], count
            )
    return text



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


