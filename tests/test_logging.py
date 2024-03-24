"""
Information
---------------------------------------------------------------------
Name        : test_logging.py
Location    : ~/tests
Author      : Tom Eleff
Published   : 2024-03-24
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

PATH = os.path.join(
    os.path.dirname(__file__),
    'resources'
)


@pytest.fixture
def LOGGING_FIXTURE():
    return logging.Handler(
        path=PATH,
        file_name='example.log',
        description=''.join([
            'Generates example user-log content for',
            ' all `pytenstils.logging` functionality.'
        ]),
        metadata={
            'Extra parameter (1)': 1,
            'Extra parameter (2)': 2
        },
        create=True,
        debug_console=False
    )


def test_logging_success(LOGGING_FIXTURE: logging.Handler):

    # Generate `str` test(s)
    LOGGING_FIXTURE.write_header(
        header='Examples: `str`'
    )
    LOGGING_FIXTURE.write(
        content='This is a critical error string',
        level='CRITICAL'
    )
    LOGGING_FIXTURE.write(
        content=''.join([
            'This is an error string that exceeds the',
            ' line-length limit set for the log-file.'
        ]),
        level='ERROR'
    )
    LOGGING_FIXTURE.write(
        content='This is a warning string.',
        level='WARNING'
    )
    LOGGING_FIXTURE.write(
        content='This is a debug string.',
        level='DEBUG'
    )
    LOGGING_FIXTURE.write(
        content=''.join([
            'This is a boring short story.'
            ' The quick brown fox jumped over the lazy dog.'
            ' The end.'
        ]),
        level='INFO'
    )
    LOGGING_FIXTURE.write(
        content='This is an unset string.'
    )

    # Generate `list` test(s)
    LOGGING_FIXTURE.write_header(
        header='Examples: `list`',
        divider=True
    )
    LOGGING_FIXTURE.write(
        content='This is a list output.'
    )
    LOGGING_FIXTURE.write(
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
    LOGGING_FIXTURE.write_header(
        header='Examples: `dict`',
        divider=True
    )
    LOGGING_FIXTURE.write(
        content='This is a dictionary output.'
    )
    LOGGING_FIXTURE.write(
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
    LOGGING_FIXTURE.write_header(
        header='Examples: `pd.DataFrame`',
        divider=True
    )
    LOGGING_FIXTURE.write(
        content='This is a dataframe output.'
    )
    LOGGING_FIXTURE.write(
        content=pd.DataFrame(
            {
                "Calories": [420, 380, 390],
                "Duration": [50, 40, 45],
                "Day": ['Monday', 'Tuesday', 'Wednesday']
            }
        )
    )

    # Close
    LOGGING_FIXTURE.close()

    # Iterate and compare logs
    test = open(os.path.join(PATH, 'example.log'), 'r')
    compare = open(os.path.join(PATH, 'compare.log'), 'r')

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
        _ = logging.Handler(
            path=os.path.join(
                os.path.dirname(__file__),
                'path-does-not-exist'
            ),
        )


def test_init_filenotfounderror():
    with pytest.raises(FileNotFoundError):
        _ = logging.Handler(
            path=PATH,
            file_name='file-not-found.log',
            create=False
        )


def test_write_header_valueerror():
    with pytest.raises(ValueError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            create=True
        )

        Logging.write_header(
            header='X'*(logging.LINE_LENGTH-logging.INDENT+1)
        )


def test_write_header_typeerror():
    with pytest.raises(TypeError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            create=True
        )

        Logging.write_header(
            header=1
        )


def test_write_typeerror():
    with pytest.raises(TypeError):

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            create=True
        )

        Logging.write(
            content=('A', 1)
        )


def test_debug_console(caplog: pytest.LogCaptureFixture):
    caplog.set_level(clogging.DEBUG)

    # Initialize logging
    Logging = logging.Handler(
        path=os.path.join(
            os.path.dirname(__file__),
            'resources'
        ),
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

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
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

    # Initialize logging
    Logging = logging.Handler(
        path=os.path.join(
            os.path.dirname(__file__),
            'resources'
        ),
        file_name='closes-on-exception-success.log',
        description=''.join([
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

        # Initialize logging
        Logging = logging.Handler(
            path=PATH,
            file_name='closes-on-exception.log',
            description=''.join([
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
