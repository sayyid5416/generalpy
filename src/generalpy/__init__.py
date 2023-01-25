""" 
Library for general classes and methods.

- PyPI: https://pypi.org/project/generalpy/
- GitHub: https://github.com/sayyid5416/generalpy

You can import classes and methods directly from this library, like `from generalpy import CustomLogging` 
or from their specific modules like `from generalpy.custom_logging import CustomLogging`
"""

from .custom_logging import (
    CustomLogging,
    LevelFormatter,
)

from .decorator import (
    combine_single_items,
    conditional,
    run_threaded,
)

from .exceptions import (
    IgnoreError
)

from .files import (
    delete_files_by_prefix_suffix,
    get_new_path,
    get_random_file_path,
    read_file_chunks,
)

from .settings import Settings