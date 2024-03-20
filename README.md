# pytensils
`pytensils` is a Python package that provides general utility functions for managing configuration, directories and data-types as well as a basic run-time profiler.

# Installation
The source code is available on [GitHub](https://github.com/thomaseleff/pytensils).

```
# Via PyPI
pip install pytensils
```

# Documentation & examples
An overview of all public `pytentils` objects, functions and methods exposed within the `pytensils.*` namespace.

- `.config` [Configuration-file management](#configuration-file-management)
- `.utils` [General utilities](#general-utilities)
- `.profiler` [Run-time profiler](#run-time-profiler)

## Configuration-file management
`.config` contains the `class` methods for reading, writing and validating `.json` format configuration-files. Access the [Source](https://github.com/thomaseleff/pytensils/blob/main/pytensils/config.py) code via GitHub.

### Initialize an instance of the config-handler
The `config.Handler(path: str, file_name: str)` constructor initializes an instance of the config `class` and validates that `path` and `file_name` exist. Should the `path` not exist, the constructor raises an `OSError`. Should the `file_name` not exist, the constructor raises a `FileNotFoundError`. 

``` python
import os
from pytensils import config

"""
    Assume there is a file, named './config.json' within the same folder
    as the executed Python program with the following contents,

        {
            "config": {
                "str": "ABC",
                "bool": true,
                "int": 1,
                "float": 9.9,
                "list": ["A", "B", "C"],
                "dict": {
                    "A": "a",
                    "B": "b",
                    "C": "c"
                }
            }
        }

"""

# Initialize the config handler `class`
Config = config.Handler(
    path=os.path.dirname(__file__),
    file_name='config.json'
)
```

### Read the configuration-file
The `.read()` method parses the `.json` configuration-file and raises an `IOError` if the content of the file cannot be parsed as `.json`.

``` python
import os
from pytensils import config

# Initialize the config handler `class`
Config = config.Handler(
    path=os.path.dirname(__file__),
    file_name='config.json'
)

# Read
conf_dict_object = Config.read()
```

### Validate the configuration-file
The `validate(config: dict, dtype: dict)` function validates that the structure of `config` matches the structure of `dtype` and returns `True` when validation is successful. The function raises any type errors within the console output as a `TypeError` when validation fails.

``` python
import os
from pytensils import config

# Static config structure and type dictionary
dtype_dict_object = {
    "config": {
        "str": "str",
        "bool": "bool",
        "int": "int",
        "float": "float",
        "list": "list",
        "dict": "dict"
    }
}

# Initialize the config handler `class`
Config = config.Handler(
    path=os.path.dirname(__file__),
    file_name='config.json'
)

# Read
conf_dict_object = Config.read()

# Validate
if config.validate(
    config=conf_dict_object,
    dtype=dtype_dict_object
):
    print('NOTE: Validation succeeded.')
```

### Write a dictionary to a `.json` configuration-file
The `.write(config: dict)` method parses the `dict` object into a `.json` configuration-file.

``` python
import os
from pytensils import config

# Initialize the config handler `class`
Config = config.Handler(
    path=os.path.dirname(__file__),
    file_name='config.json'
)

# Read
conf_dict_object = Config.read()

# Change the value of the "str" parameter within the "config" object
conf_dict_object['config']['str'] = "DEF"

# Write
Config.write(
    config=conf_dict_object
)
```

## General utilities
`.utils` contains the general functions for generating output directories and parsing data-types. Access the [Source](https://github.com/thomaseleff/pytensils/blob/main/pytensils/utils.py) code via GitHub.

### Generate an output directory
The `generate_output_directory(path: str, root: str, sub_folders: list | None)` function generates an output directory within `path` that contains `root` and all `sub_folders`. Should `root` already exist in `path`, the function raises an `OSError`.

``` python
import os
from pytensils import utils

# Create an output directory, called 'Outputs' with two sub-folders, 'A' and 'B'
utils.generate_output_directory(
    path=os.path.dirname(__file__),
    root='Outputs',
    sub_folders=['A', 'B']
)
```

### Parse a string value into any data-type
The `as_type(value: str, return_dtype: str)` function parses a string `value` into the `return_dtype` and returns `value` as that type. Should `value` not convert into `return_dtype`, the function raises a `TypeError`. If the `return_dtype` is invalid, the function raises a `NameError`.

``` python
from pytensils import utils

# Parse a string value into an `int`
int_value = utils.as_type(
    value='1',
    return_dtype='int'
)

# Parse a list as a string into a `list`
list_object = utils.as_type(
    value='["A", "B", "C"]',
    return_dtype='list'
)
```

## Run-time profiler
`.profiler` contains the general run-time decorator for timing the execution of functions. Access the [Source](https://github.com/thomaseleff/pytensils/blob/main/pytensils/profiler.py) code via GitHub.

### Time the execution of a function
The `run_time(func: Callable)` decorator function returns the result of `func` and prints and execution time of `func` within the console output.

``` python
import time
from pytensils import profiler

# Write and time a function that waits 1-second
@profiler.run_time
def wait_1_second():
    time.sleep(1)

if __name__ == "__main__":
    wait_1_second()
```
```
Output
------
> INFO: Function {wait_1_second()} executed in 00:00:01 hh:mm:ss
```