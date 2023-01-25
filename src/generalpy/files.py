""" 
This module contains methods and classes related files
"""
from io import BufferedReader
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



def read_file_chunks(
    file: str | BufferedReader,
    chunkSize: int = 4096,
    separator: bytes | None = None,
    ignoreSeperator: bytes | None = None
):
    """
    Read `file` and returns possible data of `chunkSize` 
    
    Args:
    - `file` : File to be read
    - `chunkSize` : Size of the chunk to read at a time
    - `separator` : Data would be read only upto this separator (remaining data would be read next time)
    - `ignoreSeperator` : Any data before this seperator would be ignored
    """
    # Open file
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
    
    # Close file
    if isinstance(file, str):
        fileObj.close()

