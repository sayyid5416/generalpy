""" This module contains methods and classes related files """
from pathlib import Path



def get_new_path(file_path: str, check_dir_too=False) -> str:
    """
    Returns new `file_path` for files, which do not exist by appending (1/2/3/..). 
    - `check_dir_too`: If `True`, it would work for directory paths too.
    """
    path = Path(file_path)
    if path.exists() and bool(path.is_file() or check_dir_too):
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





