"""
Information
---------------------------------------------------------------------
Name        : logging.py
Location    : ~/
Author      : Tom Eleff
Published   : 2024-03-21
Revised on  : .

Description
---------------------------------------------------------------------
Contains the `class` methods for managing 'pretty' user-logging.
"""

import os
import textwrap
import tabulate
import inspect
import datetime as dt
import pytz
import logging as clogging
import pandas as pd
from typing import Union, Callable
from pytensils import config

# Static variable(s)
INDENT = 4
LINE_LENGTH = 79
TIMEZONE = 'America/New_York'

# Setup CPython logging
clogging.basicConfig(
    level=clogging.DEBUG,
    format='[DEBUG] %(message)s'
)

# Setup tabulate
tabulate.PRESERVE_WHITESPACE = True


class Handler():

    def __init__(
        self,
        path: str,
        job_information: str,
        file_name: str = 'python.log',
        parameters: dict = {},
        create: bool = True,
        debug_console: bool = False
    ):
        """ Initializes an instance of the logger-handler class.

        Parameters
        ----------
        path : `str`
            Directory path to the folder that contains the `file_name` of the
                log-file.
        file_name : `str`
            File name of the log-file.
        create: `bool`
            `True` or `False`, creates an empty log-file, `file_name`
                within `path` when `True`.
        debug_console: `bool`
            `True` or `False`, outputs the logging content to the console
                output when `True` using `logging.debug()`.
        """

        # Assign class variables
        self.path = path
        self.file_name = file_name
        self.debug_console = debug_console
        self.start_time = dt.datetime.now(tz=pytz.timezone(TIMEZONE))

        # Validate the file-path
        if not os.path.isdir(path):
            raise OSError(
                '{~/%s} does not exist.' % (path)
            )

        # Create the file-name
        if create:
            if os.path.isfile(
                os.path.join(path, file_name)
            ):
                # Remove the log-file if it exists
                os.remove(os.path.join(path, file_name))

            # Re-create the log-file
            with open(os.path.join(path, file_name), 'w'):
                pass

            # Initialize the content of the log-file
            self.write_header(
                header='Run information',
                divider=False
            )

            # Write parameters
            if parameters:
                tuples = [(k, v) for k, v in parameters.items()]
                tuples.insert(
                    0,
                    (
                        'Start time',
                        self.start_time.strftime('%Y-%m-%d %H:%M:%S')
                    )
                )
                parameters = dict(tuples)
            else:
                parameters = {
                    'Start time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
                }

            # Write job-information
            self.write(
                content=job_information
            )

            # Write parameters
            self.write(
                content=parameters
            )

        # Validate the file-name
        else:
            if not os.path.isfile(
                os.path.join(path, file_name)
            ):
                raise FileNotFoundError(
                    '{%s} does not exist within {~/%s}.' % (
                        file_name,
                        path
                    )
                )

    def write_header(
        self,
        header: str,
        divider: bool = True
    ):
        """ Writes `header` to the log-file.

        Parameters
        ----------
        header : `str`
            String to output as a header
        divider : `bool`
            `True` or `False`, writes a divider when `True`.
        """

        # Write
        with open(os.path.join(self.path, self.file_name), 'a+') as log:

            if isinstance(header, str):

                # Validate header
                if not len(header) > (LINE_LENGTH-INDENT):
                    log.write(
                        self._pretty_header(
                            header=header,
                            divider=divider
                        )
                    )
                else:
                    raise ValueError(
                        ''.join([
                            'The header value exceeds the',
                            ' maximum line length {%s}.' % (
                                LINE_LENGTH-INDENT
                            )
                        ])
                    )

            else:
                raise NameError(
                    'Invalid header datatype {%s}.' % (
                        type(header).__name__
                    )
                )

    def write(
        self,
        content: Union[str, list, dict, pd.DataFrame],
        level: str = 'NOTSET'
    ):
        """ Writes `content` to the log-file with the `level` scope.

        Parameters
        ----------
        content : [`str`, `list`, `dict`, `pd.DataFrame`]
            The object to be written to the log-file.
        level : `str`
            Any level available by `logging`.

                e.g., [
                    'CRITICAL',
                    'ERROR',
                    'WARNING',
                    'INFO',
                    'DEBUG',
                    'NOTSET'
                ]
        """

        # Validate level
        _validate_level(level=level)

        # Retrive level substring
        substring = _return_level_substring(level=level)

        # Write
        with open(os.path.join(self.path, self.file_name), 'a+') as log:

            # `str`
            if isinstance(content, str):
                log.write(
                    self._pretty_str(
                        string=''.join([
                            substring,
                            content
                        ]),
                        level=level,
                        wrap=True
                    )
                )

            # `list`
            elif isinstance(content, list):
                log.write(
                    self._pretty_list(
                        list_object=content
                    )
                )

            # `dict`
            elif isinstance(content, dict):
                log.write(
                    self._pretty_dict(
                        dict_object=content
                    )
                )

            # `pd.DataFrame`
            elif isinstance(content, pd.DataFrame):
                log.write(
                    self._pretty_df(
                        df=content
                    )
                )

            else:
                raise NameError(
                    'Invalid content datatype {%s}.' % (
                        type(content).__name__
                    )
                )

    def close(
        self
    ):
        """ Closes the log, writing run-time information about the job.
        """

        # Write header
        self.write_header(
            header='Run time',
            divider=True
        )

        # Write context
        self.write(
            content='Run-time performance summary.'
        )

        # Write run-time parameters
        end_time = dt.datetime.now(tz=pytz.timezone(TIMEZONE))
        self.write(
            content={
                'Start time': self.start_time.strftime('%H:%M:%S.%f'),
                'End time': end_time.strftime('%H:%M:%S.%f'),
                'Run time': str(end_time-self.start_time).zfill(15),
            }
        )

        # Write final divider
        self.write(content='')
        self.write(
            content=''.join(['-'*(LINE_LENGTH-INDENT-1), '\n'])
        )

    def close_on_exception(
        self,
        func: Callable
    ) -> Callable:
        """ Logs any unhandled exception raised by the {func} passed.

        Parameters
        ----------
        func : `Callable`
            Function object.
        """

        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:

                self.write_header(
                    header='Unhandled exception'
                )
                self.write(
                    content=(
                        'The process failed due to an unhandled exception.'
                    ),
                    level='CRITICAL'
                )
                self.write(content='')
                self.write(
                    content=''.join([
                        '>'*(INDENT-1),
                        ' ',
                        type(e).__name__,
                        ': ',
                        str(e)
                    ])
                )
                self.write(
                    content={
                        'Filename': inspect.trace()[-1][1],
                        'Line Number': 'Line %s' % inspect.trace()[-1][2],
                        'Function': '%s()' % inspect.trace()[-1][3],
                        'Exception': type(e).__name__
                    }
                )
                self.close()
                raise e
            return result
        return wrapper

    def _pretty_header(
        self,
        header: str,
        divider: bool = True
    ) -> str:
        """ Returns a 'pretty' formatted header.

        Parameters
        ----------
        header : `str`
            String to `pretty` format.
        divider : `bool`
            `True` or `False`, writes a divider when `True`.
        """

        # Prettify header
        if divider:
            return ''.join(
                [
                    self._pretty_str(
                        string=''
                    ),
                    self._pretty_str(
                        string='-'*(LINE_LENGTH-INDENT-1)
                    ),
                    self._pretty_str(
                        string=''
                    ),
                    self._pretty_str(
                        string=header
                    ),
                    self._pretty_str(
                        string='-'*len(header)
                    ),
                    self._pretty_str(
                        string=''
                    )
                ]
            )
        else:
            return ''.join(
                [
                    self._pretty_str(
                        string=header
                    ),
                    self._pretty_str(
                        string='-'*len(header)
                    ),
                    self._pretty_str(
                        string=''
                    )
                ]
            )

    def _pretty_str(
        self,
        string: str,
        level: str = 'NOTSET',
        wrap: bool = False
    ) -> str:
        """ Returns a 'pretty' formatted string.

        Parameters
        ----------
        string : `str`
            String to `pretty` format.
        level : `str`
            Any level available by `logging`.

                e.g., [
                    'CRITICAL',
                    'ERROR',
                    'WARNING',
                    'INFO',
                    'DEBUG',
                    'NOTSET'
                ]
        wrap : `bool`
            `True` or `False`, wraps the string based on `logging.LINE_LENGTH`
                when `True`.
        """

        # Cleanse string
        string = string.replace('\n', '').replace('\r', '')

        # Wrap string
        if wrap:
            strings = textwrap.wrap(
                text=string,
                width=LINE_LENGTH-INDENT-1,
                subsequent_indent=' '*INDENT
            )
        else:
            strings = [string]

        # Prettify string
        if level in ['CRITICAL', 'ERROR', 'WARNING']:
            string = '\n'.join(
                [
                    ''.join(
                        ['*'*(INDENT-1), ' ', string]
                    ) for string in strings[0:1]
                ]
                + [
                    ''.join(
                        [' '*INDENT, string]
                    ) for string in strings[1:]
                ]
            )
        else:
            string = '\n'.join(
                [''.join(
                    [' '*INDENT, string]
                ) for string in strings]
            )

        # Debug
        if self.debug_console:
            clogging.debug(string.replace('\n', '\n[DEBUG] '))

        return ''.join([string, '\n'])

    def _pretty_list(
        self,
        list_object: list
    ) -> str:
        """ Returns a 'pretty' formatted list.

        Parameters
        ----------
        list_object : `list`
            List to `pretty` format.
        """

        # Prettify list
        return ''.join(
            [
                self._pretty_str(
                    string=''
                )
            ]
            + [
                self._pretty_str(
                    string=''.join([
                        ' '*INDENT,
                        '- ',
                        textwrap.shorten(
                            text=str(item),
                            width=(
                                LINE_LENGTH
                                - INDENT
                                - INDENT
                                - 3
                            ),
                            break_long_words=True
                        )
                    ])
                ) for item in list_object
            ]
        )

    def _pretty_dict(
        self,
        dict_object: dict
    ) -> str:
        """ Returns a 'pretty' formatted dict.

        Parameters
        ----------
        dict_object : `dict`
            Dictionary to `pretty` format.
        """

        # Prettify dictionary
        if config._return_dictionary_depth(dict_object=dict_object) == 1:

            # Retain the maximum key length
            max_key_length = max([len(i) for i in list(dict_object.keys())])

            return ''.join(
                [
                    self._pretty_str(
                        string=''
                    )
                ]
                + [
                    self._pretty_str(
                        string=''.join([
                            ' '*INDENT,
                            key,
                            ' '*(max_key_length-len(key)+INDENT),
                            ': ',
                            textwrap.shorten(
                                str(dict_object[key]),
                                width=(
                                    LINE_LENGTH
                                    - INDENT
                                    - INDENT
                                    - max_key_length
                                    - INDENT
                                    - 3
                                ),
                                break_long_words=True
                            )
                        ])
                    ) for key in list(dict_object.keys())
                ]
            )
        else:
            raise ValueError(
                'The dictionary object depth exceeds the maximum depth of 1.'
            )

    def _pretty_df(
        self,
        df: pd.DataFrame
    ) -> str:
        """ Writes a 'pretty' formatted dataframe.

        Parameters
        ----------
        df : `pd.DataFrame`
            Dataframe to 'pretty' format.
        """

        # Prettify dataframe
        return ''.join(
            [
                self._pretty_str(
                    string=''
                )
            ]
            + [
                self._pretty_str(
                    string=''.join([
                        ' '*INDENT,
                        line
                    ])
                ) for line in tabulate.tabulate(
                    df,
                    headers='keys',
                    tablefmt='simple',
                    showindex=False,
                    floatfmt=',.2f',
                    intfmt=','
                ).split('\n')
            ]
        )


def _validate_level(level: str):
    """ Validates the `level` scope for logging.

    Parameters
    ----------
    level: `str`
        Any level available by `logging`.

            e.g., [
                'CRITICAL',
                'ERROR',
                'WARNING',
                'INFO',
                'DEBUG',
                'NOTSET'
            ]
    """
    try:
        clogging._checkLevel(level=level)
    except ValueError:
        raise ValueError(
            'Invalid level {%s}.' % (level)
        )


def _return_level_substring(level: str):
    """ Returns the substring corresponding to level.

    Parameters
    ----------
    level: `str`
        Any level available by `logging`.

            e.g., [
                'CRITICAL',
                'ERROR',
                'WARNING',
                'INFO',
                'DEBUG',
                'NOTSET'
            ]
    """
    if level == 'NOTSET':
        return ''
    else:
        return '%s: ' % (level)
