"""
Information
---------------------------------------------------------------------
Name        : test_config.py
Location    : ~/tests
Author      : Tom Eleff
Published   : 2024-03-19
Revised on  : .

Description
---------------------------------------------------------------------
Tests methods within `pytilities.config`.
"""

import os
import pytest
from pytensils import config


# Config management function(s)
@pytest.fixture
def config_object() -> config.Handler:
    return config.Handler(
        path=os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)
            ),
            'resources'
        ),
        file_name='config.json'
    )


@pytest.fixture
def dtype_object() -> config.Handler:
    return config.Handler(
        path=os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)
            ),
            'resources'
        ),
        file_name='dtypes.json'
    )


@pytest.fixture
def config_invalid_object() -> config.Handler:
    return config.Handler(
        path=os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)
            ),
            'resources'
        ),
        file_name='config_invalid.json'
    )


@pytest.fixture
def config_validation_error_object() -> config.Handler:
    return config.Handler(
        path=os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)
            ),
            'resources'
        ),
        file_name='config_validation_error.json'
    )


def test_init_success(config_object):
    assert config_object.path == os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)
        ),
        'resources'
    )
    assert config_object.file_name == 'config.json'


def test_init_oserror():
    with pytest.raises(OSError):
        _ = config.Handler(
            path=os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)
                ),
                'path-does-not-exist'
            ),
            file_name='config.json'
        )


def test_init_filenotfounderror():
    with pytest.raises(FileNotFoundError):
        _ = config.Handler(
            path=os.path.join(
                os.path.abspath(
                    os.path.dirname(__file__)
                ),
                'resources'
            ),
            file_name='file-not-found.json'
        )


def test_read_success(config_object):
    assert config_object.read() == {
        "config": {
            "str": "ABC",
            "bool": True,
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


def test_read_ioerror(config_invalid_object):
    with pytest.raises(IOError):
        config_invalid_object.read()


def test_validate_success(config_object, dtype_object):
    assert config.validate(
        config=config_object.read(),
        dtype=dtype_object.read()
    )


def test_validate_typeerror(config_validation_error_object, dtype_object):
    with pytest.raises(TypeError):
        config.validate(
            config=config_validation_error_object.read(),
            dtype=dtype_object.read()
        )


def test_write_success(tmp_path):

    # Create an empty config-file
    with open(os.path.join(tmp_path, 'config_temp.json'), 'w') as file:
        file.write('')

    # Output content to the config-file
    temp = config.Handler(
        path=tmp_path,
        file_name='config_temp.json'
    )
    temp.write(
        config={
            "config": {
                "str": "ABC",
                "bool": True,
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
    )
    assert temp.read() == {
        "config": {
            "str": "ABC",
            "bool": True,
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
