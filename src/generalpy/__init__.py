""" 
Library for general classes and methods.

- PyPI: https://pypi.org/project/generalpy/
- GitHub: https://github.com/sayyid5416/generalpy

You can import classes and methods directly from this library, like `from generalpy import CustomLogging` 
or from their specific modules like `from generalpy.custom_logging import CustomLogging`
"""

from .custom_logging import (
    LevelFormatter,
    CustomLogging
)

from .decorator import (
    run_threaded,
    combine_single_items,
    conditional
)

from .files import (
    get_new_path,
    read_file_chunks
)

from .settings import Settings