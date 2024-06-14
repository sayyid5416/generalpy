""" 
Library for general classes and methods.

- PyPI: https://pypi.org/project/generalpy/
- GitHub: https://github.com/sayyid5416/generalpy

You can import classes and methods directly from this library, like `from generalpy import CustomLogging` 
or from their specific modules like `from generalpy.custom_logging import CustomLogging`
"""

from .api import (
    Api_Call
)

from .cli import (
    Attrib,
    ICACLS,
    TaskList
)

from .ctypes import (
    run_ShellExecuteW,
    running_as_admin,
    set_app_user_model_id,
)

from .custom_logging import (
    CustomLogging,
    LevelFormatter,
)

from .database import (
    DatabaseCollection,
    Settings,
)

from .decorator import (
    combine_single_items,
    conditional,
    log_it,
    platform_specific,
    retry_support,
    run_threaded,
)

from .exceptions import (
    IgnoreError
)

from .files import (
    delete_files_by_condition,
    delete_files_by_prefix_suffix,
    get_new_path,
    get_random_file_path,
    get_unsupported_file_path_chars,
    read_file_chunks,
    sanitised_filename,
)

from .general import (
    first_capital,
    format_bytes,
    format_dict,
    generate_repr_str,
    get_adjusted_color,
    get_digit_from_text,
    get_first_non_alphabet,
    get_installed_fonts,
    is_python,
    punctuate,
    remove_extra_spaces,
    replace_html_tags,
    replace_multiple_chars,
    similarized,
    sliced_list,
    Calender_Class
)

from .signal import (
    Signal
)