"""
This module contains general classes and methods
"""
import re
import sys
from pathlib import Path
from string import punctuation
from typing import Any, Iterable

# This import could not be done inside any function.
# So, be aware of circular imports.
from .decorator import platform_specific

# winreg is imported in functions, because it was causing issues on linux machines




def first_capital(text: str) -> str:
    """
    Returns text after making first letter capital
    - Do not change any other thing
    """
    first = text[:1]
    return text.replace(
        first, first.capitalize(), 1
    )



def format_bytes(size: float):
    """
    Converts bytes into a human-readable format.

    Args:
        size (int): Size in bytes.
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    
    formatted_size = f'{size:.2f}'
    if '.' in formatted_size:
        formatted_size = formatted_size.rstrip('0').rstrip('.')
        
    return f"{formatted_size} {units[i]}"



def format_dict(data: dict, indent: int = 4, keyPrefix: str = None, modifyKeys: bool = True, initialIndent: int = 0):
    """
    Converts dict into a human-readable format.
    
    Args:
        - `data`: The dictionary to be formatted.
        - `indent`: The number of spaces for indentation.
        - `keyPrefix`: Prefix to be added before keys.
        - `modifyKeys`: Whether to modify keys text to make them more readable.
        - `initialIndent`: The initial indentation level.

    """
    
    def format_key(item: str) -> str:
        """ Format dictionary keys into a more readable form. """
        if modifyKeys:
            item = item.replace("_", " ").title()
            item = f'<b>{item}</b>'
        return f'{keyPrefix}{item}' if keyPrefix else item

    formattedString = ""
    for key, value in data.items():
        if isinstance(value, dict):
            formattedString += f"{' ' * initialIndent}{format_key(key)}:\n"
            formattedString += format_dict(
                value,
                indent=indent,
                keyPrefix=keyPrefix,
                modifyKeys=modifyKeys,
                initialIndent=initialIndent + indent
            )
        else:
            formattedString += f"{' ' * initialIndent}{format_key(key)}: {value}\n"
    
    return formattedString



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



def get_adjusted_color(hex_color, percentageDark: int = None, percentageBright: int = None):
    """
    Adjusts the brightness of a color in hexadecimal format.

    Args:
        hex_color (str): The color in hexadecimal format (e.g., '#RRGGBB').
        percentageDark (int, optional): The percentage by which to darken the color.
        percentageBright (int, optional): The percentage by which to brighten the color.

    Returns:
        str: The adjusted color in hexadecimal format.
    """
    # Convert hex to RGB
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Adjust color if either percentageDark or percentageBright is provided
    if percentageDark is not None:
        adjustment = 1 - (percentageDark / 100)
    elif percentageBright is not None:
        adjustment = 1 + (percentageBright / 100)
    else:
        return '#' + hex_color
    
    # Calculate adjusted color
    r_adjusted = max(0, min(255, int(r * adjustment)))
    g_adjusted = max(0, min(255, int(g * adjustment)))
    b_adjusted = max(0, min(255, int(b * adjustment)))
    
    # Convert RGB to hex
    adjusted_hex = '#{:02x}{:02x}{:02x}'.format(r_adjusted, g_adjusted, b_adjusted)
    
    return adjusted_hex



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



def get_first_non_alphabet(string: str, ignoredChars: list[str] | None = None) -> str:
    """
    Returns the first non-alphabet character from `string`.
    - `ignoredChars`: These characters will be ignored
    """
    if ignoredChars is None:
        ignoredChars = []
    for char in string:
        if not char.isalpha() and char not in ignoredChars:
            return char
    return ' '



@platform_specific('win32')
def get_installed_fonts(sanitize: bool=True):
    """ Returns a list of fonts installed on Windows 
    - sanitize: Remove Bold, Italic etc
    """
    import winreg
    fonts_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts")
    installed_fonts = []
    try:
        index = 0
        while True:
            font_name, *_ = winreg.EnumValue(fonts_key, index)
            
            # sanitize
            if sanitize:
                font_name = font_name.strip().split(' (')[0]
                font_name = font_name.strip().split(' &')[0]
                for i in ['Light', 'Medium', 'Regular', 'Semilight', 'Bold', 'Italic', 'ExtraBold']:
                    font_name = font_name.replace(f' {i}', '').strip()
                font_name = font_name.strip()

            # Add font
            if font_name not in installed_fonts:
                installed_fonts.append(font_name)
            index += 1
    except OSError:
        pass
    return installed_fonts



def is_python() -> bool:
    """
    Returns: `True` if current running app is `python`
    """
    appPath = Path(sys.executable)
    appName = appPath.stem.lower()
    return appName == 'python' or appName == 'pythonw'



def punctuate(text: str, punc: str = '.'):
    """ 
    Adds `punc` in the end of `text`,
    if no punctuation available 
    """
    if not text.endswith(tuple(punctuation)):
        text += punc
    return text



def remove_extra_spaces(s: str) -> str:
    """
    Removed extra white spaces between words.
    - New lines are preserved
    - Also removes leading and trailing whitespace/new-lines
    """
    # Split the string into lines
    lines = s.split('\n')

    # Remove extra whitespace between words on each line
    for i, line in enumerate(lines):
        line = re.sub(r'[\x00-\x1f\x7f-\x9f\u200b-\u200f\u2028-\u202f\ufeff]', ' ', line)       # invisible chars
        line = line.replace(r'&#32;', ' ')                                                      # HTML space
        lines[i] = ' '.join(line.split())

    # Join the lines and return the result
    return '\n'.join(lines).strip()



def replace_html_tags(text: str, repl: str='', ignore: list[str] | None = None):
    """ 
    Returns: `text` after replacing all HTML tags with `repl`
    - `ignore`: these tags will be ignored
    """
    if ignore:
        # Build a regex pattern to match all tags except the ones in `ignore`
        ignoredTags = '|'.join(fr'/?{tag}' for tag in ignore)
        condition = fr'(?!(?:{ignoredTags})\b)'
        pattern = fr'<{condition}.*?>'
    else:
        # If `ignore` is not specified, match all tags
        pattern = r'<.*?>'

    return re.sub(pattern, repl, text)



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



def similarized(mainList: Iterable[str], sep: str | None = None) -> list[list[str]] :
    """ Takes a list of strings and returns a list of sublists of similar-strings.
    - Ex: `['HE_bro', 'SHE_why', 'HE_yes', 'SHE_ok', ...]` -> `[['HE_bro', 'HE_yes'], ['SHE_why', 'SHE_ok'], ...]`
    - `sep`: If passed, elements would be parsed according to it, else on first-non-alphabet
    """
    finalList: list[list[str]] = []
    similars: list[str] = []
    current_prefix = None

    for i in sorted(mainList):
        prefix = i.split(
            sep or get_first_non_alphabet(i)
        )[0]
        if prefix == current_prefix:
            similars.append(i)
        else:
            if similars:
                finalList.append(similars)
                similars = []
            current_prefix = prefix
            similars.append(i)
    
    if similars:
        finalList.append(similars)

    return finalList



def sliced_list(mainList: list[Any], n: int = 3):
    """
    Returns a list of sublists, 
    where each sublist contains `n` items, 
    created by slicing `mainList`.
    """
    return [
        mainList[i:i+n] 
        for i in range(
            0, len(mainList), n
        )
    ]











class Calender_Class:
    """
    Class Containing functions related to Calendar
    """        
    
    def __init__(self):
        """
        Class Containing functions related to Calendar
        """        
        
        # Months Names Dict
        self.gregorian_months_dict = {
            1: ('january', 'jan'),
            2: ('february', 'feb'),
            3: ('march', 'mar'),
            4: ('april', 'apr'),
            5: ('may', 'may'),
            6: ('june', 'jun'),
            7: ('july', 'july'),
            8: ('august', 'aug'),
            9: ('september', 'sep'),
            10: ('october', 'oct'),
            11: ('november', 'nov'),
            12: ('december', 'dec')
        }
        
        # Months List
        self.months_31 = [1, 3, 5, 7, 8, 10, 12]
        self.months_30 = [4, 6, 9, 11]
        self.months_feb = [2]
    

    def getMonthName(self, month_num:int, full_month_name:bool=True, capital:bool=False) -> str:
        """
        RETURNS: proper month name
        """
        
        # Val to Return
        if 1 <= month_num <=12:
            if full_month_name:
                val = self.gregorian_months_dict[month_num][0]
            else:
                val = self.gregorian_months_dict[month_num][1]
        else:
            val = 'not-applicable'
        
        # Capital
        if capital:
            val = val.title()
        
        return val


    def get_months_days_num(self, month_num:int, leap_year:bool=False) -> int:
        """
        RETURNS: Number of days in a month
        """        

        # Checks
        if month_num in self.months_30:
            return 30
        elif month_num in self.months_31:
            return 31
        elif month_num in self.months_feb:
            if leap_year:
                return 29
            else:
                return 28
        else:
            return 0
    
    
    def check_months_num_validity(self, month_num:int, month_days:int, leap_year:bool=False) -> bool:
        """
        RETURNS:
            - True: if month "month_num" contains "month_days" number of days
            - False: if above condition doesn't met
        """        
        
        # Checks
        if month_num in self.months_31 and month_days > 31:
            return False
        elif month_num in self.months_30 and month_days > 30:
            return False
        elif month_num in self.months_feb and leap_year == True and month_days > 29:
            return False
        elif month_num in self.months_feb and leap_year == False and month_days > 28:
            return False
        else:
            return True

