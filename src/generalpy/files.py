""" 
This module contains methods and classes related files
"""
from io import BufferedReader
import logging
import random
import os
from pathlib import Path

from .custom_logging import CustomLogging




def delete_files_by_prefix_suffix(
    directory: str,
    prefix: str | None = None,
    suffix: str | None = None,
    logger: logging.Logger | None = None
):
    """
    Deletes all files in `directory` and its subdirectories
    which have `prefix` as prefix or `suffix` as suffix in their name.
    - `prefix=''` or `suffix=''` will remove all possible files in `directory`
    - `prefix` and `suffix` are not case sensitive
    - `logger`: for logging purposes
    """
    if prefix is None and suffix is None:
        return
    if logger is None:
        logger = CustomLogging(loggingLevel=logging.DEBUG).logger
    
    def file_should_delete(fileName: str):
        """ Returns True if file with `fileName` needs to be deleted """
        fileName = fileName.lower()
        if prefix and fileName.startswith(prefix.lower()):
            return True
        if suffix and fileName.endswith(suffix.lower()):
            return True
        return False

    def delete_file(filePath: Path):
        """ Deletes the file at `filePath` """
        try:
            os.remove(filePath)
        except Exception as e:
            logger.warning(f'Not Deleted: {filePath}. Reason: {e}')
        else:
            logger.debug(f'Deleted: {filePath}')

    for parentFolder, foldersList, filesList in os.walk(directory):
        for fileName in filesList:
            
            # [Delete file]
            if file_should_delete(fileName):
                filePath = Path(parentFolder, fileName)
                delete_file(filePath)



def get_new_path(filePath: str | Path, checkDir=False) -> str:
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
