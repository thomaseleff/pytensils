"""
Information
---------------------------------------------------------------------
Name        : test_logging.py
Location    : ~/tests
Author      : Tom Eleff
Published   : 2024-03-22
Revised on  : .

Description
---------------------------------------------------------------------
Tests methods within `pytensils.logging`.
"""

import os
import pandas as pd
import logging as clogging
import pytest
from pytensils import logging


def test_logging_success():

    # Set up logging parameters
    path = os.path.join(
        os.path.dirname(__file__),
        'resources'
    )
    file_name = 'example.log'

    # Initialize logging
    Logging = logging.Handler(
        path=path,
        file_name=file_name,
        job_information=''.join([
            'Generates example user-log content for',
            ' all `pytenstils.logging` functionality.'
        ]),
        parameters={
            'Extra parameter (1)': 1,
            'Extra parameter (2)': 2
        },
        create=True,
        debug_console=False
    )

    # Generate `str` test(s)
    Logging.write_header(
        header='Examples: `str`'
    )
    Logging.write(
        content='This is a critical error string',
        level='CRITICAL'
    )
    Logging.write(
        content=''.join([
            'This is an error string that exceeds the',
            ' line-length limit set for the log-file.'
        ]),
        level='ERROR'
    )
    Logging.write(
        content='This is a warning string.',
        level='WARNING'
    )
    Logging.write(
        content='This is a debug string.',
        level='DEBUG'
    )
    Logging.write(
        content=''.join([
            'This is a boring short story.'
            ' The quick brown fox jumped over the lazy dog.'
            ' The end.'
        ]),
        level='INFO'
    )
    Logging.write(
        content='This is an unset string.'
    )

    # Generate `list` test(s)
    Logging.write_header(
        header='Examples: `list`',
        divider=True
    )
    Logging.write(
        content='This is a list output.'
    )
    Logging.write(
        content=[
            ' '.join(str(i) for i in list(range(52))),
            ['A', 'B', 'C'],
            ('A', 'B', 'C'),
            1,
            2,
            3,
        ]
    )

    # Generate `dict` test(s)
    Logging.write_header(
        header='Examples: `dict`',
        divider=True
    )
    Logging.write(
        content='This is a dictionary output.'
    )
    Logging.write(
        content={
            'A': 'a',
            'B': 'b',
            '123s': ' '.join(str(i) for i in list(range(52))),
            'Nineteen characters': 19,
            'List': ['A', 'B', 'C'],
            'Tupple': ('A', 'B', 'C')
        }
    )

    # Generate `pd.DataFrame` test(s)
    Logging.write_header(
        header='Examples: `pd.DataFrame`',
        divider=True
    )
    Logging.write(
        content='This is a dataframe output.'
    )
    Logging.write(
        content=pd.DataFrame(
            {
                "Calories": [420, 380, 390],
                "Duration": [50, 40, 45],
                "Day": ['Monday', 'Tuesday', 'Wednesday']
            }
        )
    )

    # Close
    Logging.close()

    # Iterate and compare logs
    test = open(os.path.join(path, file_name), 'r')
    compare = open(os.path.join(path, 'compare.log'), 'r')

    test_lines = test.readlines()
    compare_lines = compare.readlines()

    test.close()
    compare.close()

    # Assert both test and compare are the same length
    assert len(test_lines) == len(compare_lines)

    # Assert test and compare contain the same content
    #   Skip lines 6, 72, 73, 74 as these contain
    #   date-time values that cannot be compared due
    #   to different execution windows.
    for index in range(len(test_lines)):
        if index not in [6, 72, 73, 74]:
            assert test_lines[index] == compare_lines[index]


def test_init_oserror():
    with pytest.raises(OSError):

        # Set up logging parameters
        path = os.path.join(
            os.path.dirname(__file__),
            'path-does-not-exist'
        )

        # Initialize logging
        _ = logging.Handler(
            path=path,
        )


def test_init_filenotfounderror():
    with pytest.raises(FileNotFoundError):

        # Set up logging parameters
        path = os.path.join(
            os.path.dirname(__file__),
            'resources'
        )

        # Initialize logging
        _ = logging.Handler(
            path=path,
            file_name='file-not-found.log',
            create=False
        )


def test_write_header_valueerror():
    with pytest.raises(ValueError):

        # Set up logging parameters
        path = os.path.join(
            os.path.dirname(__file__),
            'resources'
        )

        # Initialize logging
        Logging = logging.Handler(
            path=path,
            create=True
        )

        Logging.write_header(
            header='X'*(logging.LINE_LENGTH-logging.INDENT+1)
        )


def test_write_header_typeerror():
    with pytest.raises(TypeError):

        # Set up logging parameters
        path = os.path.join(
            os.path.dirname(__file__),
            'resources'
        )

        # Initialize logging
        Logging = logging.Handler(
            path=path,
            create=True
        )

        Logging.write_header(
            header=1
        )


def test_write_typeerror():
    with pytest.raises(TypeError):

        # Set up logging parameters
        path = os.path.join(
            os.path.dirname(__file__),
            'resources'
        )

        # Initialize logging
        Logging = logging.Handler(
            path=path,
            create=True
        )

        Logging.write(
            content=('A', 1)
        )


def test_debug_console(caplog):
    caplog.set_level(clogging.DEBUG)

    # Set up logging parameters
    path = os.path.join(
        os.path.dirname(__file__),
        'resources'
    )

    # Initialize logging
    Logging = logging.Handler(
        path=path,
        create=True,
        debug_console=True
    )

    # Create debug console output
    Logging.write(content='Log-content-for-the-output-console')

    # Cleanup
    os.remove(
        os.path.join(
            os.path.dirname(__file__),
            'resources',
            'python.log'
        )
    )

    assert 'Log-content-for-the-output-console' in caplog.text


def test_pretty_dict_valueerror():
    with pytest.raises(ValueError):

        # Set up logging parameters
        path = os.path.join(
            os.path.dirname(__file__),
            'resources'
        )

        # Initialize logging
        Logging = logging.Handler(
            path=path,
            create=True
        )

        # Cleanup
        os.remove(
            os.path.join(
                os.path.dirname(__file__),
                'resources',
                'python.log'
            )
        )

        _ = Logging._pretty_dict(dict_object={'A': {'B': {'C': 'c'}}})


def test_validate_level_valueerror():
    with pytest.raises(ValueError):
        logging._validate_level(level='unknown-logging-level')


def test_logging_close_on_exception_success():

    # Set up logging parameters
    path = os.path.join(
        os.path.dirname(__file__),
        'resources'
    )

    # Initialize logging
    Logging = logging.Handler(
        path=path,
        file_name='closes-on-exception-success.log',
        job_information=''.join([
            'Generates close-on-exception content for',
            ' `pytenstils.logging` functionality.'
        ]),
        create=True,
        debug_console=False
    )

    @Logging.close_on_exception
    def divide_by_1():
        return 1 / 1

    assert divide_by_1() == 1

    # Close
    Logging.close()


def test_logging_close_on_exception_zerodivisionerror():
    with pytest.raises(ZeroDivisionError):

        # Set up logging parameters
        path = os.path.join(
            os.path.dirname(__file__),
            'resources'
        )

        # Initialize logging
        Logging = logging.Handler(
            path=path,
            file_name='closes-on-exception.log',
            job_information=''.join([
                'Generates close-on-exception content for',
                ' `pytenstils.logging` functionality.'
            ]),
            create=True,
            debug_console=False
        )

        @Logging.close_on_exception
        def divide_by_zero():
            return 1 / 0

        divide_by_zero()
