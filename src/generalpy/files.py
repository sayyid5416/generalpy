""" This module contains methods and classes related files """
from pathlib import Path



def get_new_path(filePath: str, checkDir=False) -> str:
    """
    Returns new `filePath` for files, which do not exist by appending (1/2/3/..). 
    - `checkDir`: If `True`, it would work for directory paths too.
    """
    path = Path(filePath)
    if path.exists() and bool(path.is_file() or checkDir):
        i = 1
        while path.exists():
            # creates a new file path 
            # by appending (i) to the file name
            path = Path(
                path.parent,
                f'{path.stem}({i}){path.suffix}'
            )
            i += 1
    return str(path)





