"""
This module contains general classes and methods
"""
import re




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
