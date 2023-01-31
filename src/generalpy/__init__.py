""" 
Library for general classes and methods.

- PyPI: https://pypi.org/project/generalpy/
- GitHub: https://github.com/sayyid5416/generalpy

You can import classes and methods directly from this library, like `from generalpy import CustomLogging` 
or from their specific modules like `from generalpy.custom_logging import CustomLogging`
"""

from .cli import (
    Attrib,
    ICACLS,
    TaskList
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
    platform_specific,
    run_threaded,
    time_it
)

from .exceptions import (
    IgnoreError
)

from .files import (
    delete_files_by_condition,
    delete_files_by_prefix_suffix,
    get_new_path,
    get_random_file_path,
    read_file_chunks,
)

from .general import (
    generate_repr_str,
    get_digit_from_text,
    is_python,
    replace_multiple_chars,
    set_app_user_model_id
)
