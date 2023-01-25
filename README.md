<p align="center">
  <a href="../../actions/workflows/publish.yml"><img src="../../actions/workflows/publish.yml/badge.svg"></a>
  <a href="https://pypi.org/project/generalpy"><img alt="PyPI" src="https://img.shields.io/pypi/v/generalpy?label=PyPI%20Package%20Version&logo=pypi&logoColor=white&style=plastic"></a>
</p>

# 🔰 generalpy
- Python package for general classes and methods
- Install using `pip install generalpy`


### 💠 `Settings` class
  - Class to handle all settings related aspect for an app.
  - Based on settings file stored in storage.
     

### 💠 `LevelFormatter` class
  - Custom `logging.Formatter` class.
  - To set formatting based on logging Levels. Like `logging.INFO`, `logging.ERROR` etc.
  - You can also set different time zone for `%(asctime)s`
     

### 💠 `CustomLogging` class
  - Class to handle logging in easy way.
  - All logging class features + more.
  - Compact & Full formatting are applied wherever applicable.
  - Stream logging to Terminal.
  - File logging: For all logs, and error logs in different files.
  - You can also set different time zone for `%(asctime)s`.


### 💠 `decorator` module
  This module contains decorators
  - `combine_single_items`: Combine item of sublists _(which contain only one item)_ into a single sublist.
  - `conditional`: Runs the decorated function and return it's value, only if provided condition is True.
  - `run_threaded`: Runs the decorated function in a new thread.


### 💠 `files` module
  This module contains methods to work with files
  - `delete_files_by_prefix_suffix`: Deletes all files in directory and its subdirectories according to prefix/suffix in their name.
  - `get_new_path`: Returns new filePath for files _(which do not exist)_ by appending (1/2/3/..).
  - `get_random_file_path`: Returns a random path of a file _(which do not exist)_ in parentDirectory.
  - `read_file_chunks`: Read file and returns possible data chunk by chunk.
