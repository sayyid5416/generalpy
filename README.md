<p align="center">
  <a href="https://github.com/sayyid5416/generalpy/actions/workflows/publish.yml"><img src="https://github.com/sayyid5416/generalpy/actions/workflows/publish.yml/badge.svg"></a>
  <a href="https://pypi.org/project/generalpy"><img alt="PyPI" src="https://img.shields.io/pypi/v/generalpy?label=PyPI%20Package%20Version&logo=pypi&logoColor=white&style=plastic"></a>
</p>

### 🔰 generalpy
- Python package for general classes and methods
- Install using `pip install generalpy`


---


### 💠 `Attrib` class _(windows OS only)_
  - Handles the `attrib` command from windows OS.
  - To set/modify/remove the `A/H/I/R/S` attributes for files/folders.
  - Use `attrib /?` in CMD for more info.


### 💠 `CustomLogging` class
  - Class to handle logging in easy way.
  - All logging class features + more.
  - Compact & Full formatting are applied wherever applicable.
  - Stream logging to Terminal.
  - File logging: For all logs, and error logs in different files.
  - You can also set different time zone for `%(asctime)s`.


### 💠 `DatabaseCollection` class
  - Handles the data of a collection `collectionName` in some database.
  - This database will be in memory, but you can extend this functionality by using this class as a base class.
  - And you can create a class which handles db locally or on cloud like MongoDB.
  - **Database** structure should be: `DataBase > collection > collection-data`.
  - Structure of **collection-data**: `dict[str, dict[str, Any]]` i.e `dataID: {dataType: dataValue, ...}, ...`


### 💠 `ICACLS` class _(windows OS only)_
  - Handles functions related to `icacls` command from windows OS.
  - To set/modify/remove the permissions for files/folders.
  - Use `icacls /?` in CMD for more info.


### 💠 `IgnoreError(Exception)` class
  - This exception should be ignored after catching it for the sake of continuity.
  - You can ignore it in `try: ... except IgnoreError: pass` block, or
  - By logging/printing to console.


### 💠 `LevelFormatter` class
  - Custom `logging.Formatter` class.
  - To set formatting based on logging Levels. Like `logging.INFO`, `logging.ERROR` etc.
  - You can also set different time zone for `%(asctime)s`


### 💠 `Settings` class
  - Handles all settings related aspect for an app.
  - Based on settings file stored in storage.


### 💠 `Signal` class
  - A signal object that can be used to connect callback.
  - Simply connect a callback using `.connect(...)` method.
  - Emit the signal using `.emit(...)` method.


### 💠 `TaskList` class _(windows OS only)_
  - Handles functions related to `tasklist` command of windows OS.
  - Get running tasks/executables.
  - Check if an exe is running or not, or how many of it's instances are running.


---


### 💠 `decorator` module
  This module contains decorators
  - `combine_single_items`: Combine item of sublists _(which contain only one item)_ into a single sublist.
  - `conditional`: Run decorated function and return it's value, only if provided condition is True.
  - `platform_specific`: Run decorated function only if current platform is one of the `supportedPlatforms`
  - `retry_support`: Retry the decorated function gracefully.
  - `run_threaded`: Run decorated function in a new thread.
  - `time_it`: Prints the time taken by decorated function.


### 💠 `files` module
  This module contains methods to work with files
  - `delete_files_by_condition`: Deletes all files in directory and its subdirectories according to some condition.
  - `delete_files_by_prefix_suffix`: Deletes all files in directory and its subdirectories according to prefix/suffix in their name.
  - `get_new_path`: Returns new filePath for files _(which do not exist)_ by appending (1/2/3/..).
  - `get_random_file_path`: Returns a random path of a file _(which do not exist)_ in parentDirectory.
  - `read_file_chunks`: Read file and returns possible data chunk by chunk.


### 💠 `general` module
  This module contains general methods
  - `first_capital`: Make first letter capital without changing any other thing.
  - `generate_repr_str`: Returns a suitable string for `__repr__` method of classes.
  - `get_digit_from_text`: Returns the digit from the first occurrence of `(digit)`.
  - `get_first_non_alphabet`: Returns the first non-alphabet character from string.
  - `is_python`: Returns `True` if current running app is `python`.
  - `punctuate`: Adds punctuation after string, if not present.
  - `remove_extra_spaces`: Removed extra spaces between words.
  - `replace_html_tags`: Replace html tags from a string.
  - `replace_multiple_chars`: Replace multiple characters from a string.
  - `set_app_user_model_id`: Sets the App User Model ID for the current process on windows OS.
  - `similarized`: Takes a list of strings and returns a list of sublists of similar-strings.
  - `sliced_list`: Slice a list into a list of sublists, where each sublist contains specific no. of items.