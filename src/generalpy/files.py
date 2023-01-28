""" 
This module contains methods and classes related files
"""
from io import BufferedReader
import logging
import random
import os
from pathlib import Path
from typing import Callable

"""
Items imported inside functions/classes

- from .custom_logging import CustomLogging
- from .general import get_digit_from_text
"""



def delete_files_by_condition(
    directory: str,
    condition: Callable[[str], bool],
    logger: logging.Logger | None = None
):
    """
    Deletes all files in `directory` and its subdirectories if `condition(filename)` returns `True`

    Args
    - `directory`: Directory to search for files
    - `condition`: A condition which will be checked before deleting individual files. `filename` would be passed to it.
    - `logger`: for logging purposes
    """
    if logger is None:
        from .custom_logging import CustomLogging
        logger = CustomLogging(loggingLevel=logging.DEBUG).logger
    
    def delete_file(filePath: Path):
        """ Deletes the file at `filePath` """
        try:
            os.remove(filePath)
        except Exception as e:
            logger.warning(f'Not Deleted: {filePath}. Reason: {e}')
        else:
            logger.debug(f'Deleted: {filePath}')

    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if condition(filename):
                filepath = Path(dirpath, filename)
                delete_file(filepath)
    


def delete_files_by_prefix_suffix(
    directory: str,
    prefix: str | None = None,
    suffix: str | None = None,
    logger: logging.Logger | None = None
):
    """
    Deletes all files in `directory` and its subdirectories
    which have `prefix` as prefix or `suffix` as suffix in their name.
    
    Args:
    - `prefix=''` or `suffix=''` will remove all possible files in `directory`
    - `prefix` and `suffix` are not case sensitive
    - `logger`: for logging purposes
    """
    if prefix is None and suffix is None:
        return
    
    def file_should_delete(fileName: str):
        """ 
        Returns `True` if `fileName` contains `prefix` or `suffix`
        """
        fileName = fileName.lower()
        if prefix and fileName.startswith(prefix.lower()):
            return True
        if suffix and fileName.endswith(suffix.lower()):
            return True
        return False

    # Delete files
    delete_files_by_condition(
        directory=directory,
        condition=file_should_delete,
        logger=logger
    )



def get_new_path(filePath: str | Path, checkDir=False) -> str:
    """
    Returns new `filePath` for files, which do not exist by appending (1/2/3/..). 
    - `checkDir`: If `True`, it would work for directory paths too.
    """
    path = Path(filePath)
    if path.exists() and bool(path.is_file() or checkDir):
        i = 1

        # File name
        from .general import get_digit_from_text
        fileName = path.stem.strip()
        availableNum = get_digit_from_text(fileName[-3:])
        if availableNum:
            i += availableNum                                           # Numbering will start from this number
            fileName = fileName[:-3]                                    # Remove already available number
        
        # Creating new path
        # by appending (i) to the file name
        while path.exists():
            path = Path(
                path.parent,
                f'{fileName}({i}){path.suffix}'
            )
            i += 1
    return str(path)



def get_random_file_path(
    fileExtension: str,
    parentDirectory: str | None = None,
    filePrefix: str = 'random-file-',
    justFileName=False
):
    """
    Returns a random path of a file which is not present, in `parentDirectory`
    
    Args:
    - `fileExtension`: Type of file. Ex: `fileExtension='mp4'`
    - `parentDirectory`: If None, current working directory would be used
    - `filePrefix`: Prefix for the filename
    - `justFileName`: If True, only filename would be returned
    """
    def get_file_name():
        """ Returns a random filename """
        return f'{filePrefix}{random.randint(1, 100000)}.{fileExtension}'
    
    # [Modify] parent directory
    if not parentDirectory:
        parentDirectory = os.getcwd()
    
    # Get filePath
    filePath = get_new_path(
        Path(
            parentDirectory,
            get_file_name()
        )
    )
    
    # Return
    if justFileName:
        return Path(filePath).name
    return filePath



def read_file_chunks(
    file: str | BufferedReader,
    chunkSize: int = 4096,
    separator: str | bytes | None = None,
    ignoreSeperator: str | bytes | None = None
):
    """
    Read `file` and returns possible data of `chunkSize` 
    
    Args:
    - `file` : File to be read
    - `chunkSize` : Size of the chunk to read at a time
    - `separator` : Data would be read only upto this separator (remaining data would be read next time)
    - `ignoreSeperator` : Any data before this seperator would be ignored
    """
    # [Modify] Args
    if isinstance(separator, str):
        separator = separator.encode()
    if isinstance(ignoreSeperator, str):
        ignoreSeperator = ignoreSeperator.encode()
    
    # [Open] file
    if isinstance(file, str):
        fileObj = open(file, 'rb')
    else:
        fileObj = file

    # Yield data
    while True:
        
        # Read data
        data = fileObj.read(chunkSize)
        if not data:
            break
        
        # [Modification] Consider data only AFTER separator2 (delete remaining data)
        if ignoreSeperator and ignoreSeperator in data:
            _, data = data.split(ignoreSeperator, 1)
            data = data.replace(ignoreSeperator, b'')

        # [Modification] Consider data only BEFORE separator (keep remaining data)
        if separator and separator in data:
            data, remainder = data.split(separator, 1)
        else:
            data, remainder = data, b''
        
        # Yield
        if data:
            yield data
        
        # Go back if data is remaining
        fileObj.seek(-len(remainder), 1)
    
    # [Close] file
    if isinstance(file, str):
        fileObj.close()
