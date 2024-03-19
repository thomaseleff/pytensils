"""
Information
---------------------------------------------------------------------
Name        : config.py
Location    : ~/
Author      : Tom Eleff
Published   : 2024-03-19
Revised on  : .

Description
---------------------------------------------------------------------
Contains the `class` methods for managing configuration.
"""

import os
import json


class Handler():

    def __init__(
        self,
        path: str,
        file_name: str
    ):
        """ Initializes an instance of the configuration-handler class.

        Parameters
        ----------
        path : `str`
            Directory path to the folder that contains the `file_name` of the
                '.json' config-file.
        file_name : `str`
            File name of the '.json' config-file.
        """

        # Validate the file-path
        if os.path.isdir(path):
            self.path = path
        else:
            raise OSError(
                '{~/%s} does not exist.' % (path)
            )

        # Validate the file-name
        if os.path.isfile(
            os.path.join(path, file_name)
        ):
            self.file_name = file_name
        else:
            raise FileNotFoundError(
                '{%s} does not exist within {~/%s}.' % (
                    file_name,
                    path
                )
            )

    def read(self) -> dict:
        """ Reads a '.json' config-file and returns the contents as a `dict`
        object.
        """
        with open(
            os.path.join(
                self.path,
                self.file_name
            ),
            mode='r'
        ) as file:
            try:
                return json.load(file)
            except json.decoder.JSONDecodeError:
                raise IOError(
                    "{~/%s} is not a valid '.json' config-file." % (
                        os.path.basename(
                            self.file_name
                        )
                    )
                )

    def write(
        self,
        config: dict
    ):
        """ Writes a '.json' config-file with the contents of `config`.

        Parameters
        ----------
        config : `dict`
            Dictionary object that contains the parameters essential to the
                application.
        """
        with open(
            os.path.join(
                self.path,
                self.file_name
            ),
            mode='w+'
        ) as file:
            json.dump(
                config,
                file,
                indent=4
            )


def validate(
    config: dict,
    dtype: dict
):
    """ Validates `config` against the dtypes in `dtype`.

    Parameters
    ----------
    config : `dict`
        Dictionary object that contains the parameters essential to the
            application.
    dtype : `dict`
        Dictionary object that contains the expected `config` value dtypes.
    """

    config_errors = {}
    error = False

    for section in config.keys():
        if section not in dtype.keys():
            dtype[section] = {}
            config_errors[section] = {}
        else:
            config_errors[section] = {}

        for key, value in config[section].items():
            if key not in dtype[section].keys():
                config_errors[section][key] = (
                    'No dtype found in {dtypes}.'
                )
                error = True
            else:
                if type(value).__name__ != dtype[section][key]:
                    config_errors[section][key] = (
                        'Invalid dtype. Expected <%s>.' % (
                            dtype[section][key]
                        )
                    )
                    error = True
                else:
                    pass

    len0 = max(
        [len(section) for section in config_errors.keys()]
    )

    if error:
        for section in config_errors.keys():
            if len(config_errors[section].keys()) > 0:
                print('\n')
                print(
                    '*** ERROR: The following errors occurred when' +
                    ' validating the {%s} parameters.\n' %
                    (section)
                )

                len1 = max(
                    [len(key) for key in config_errors[section].keys()]
                )
                len2 = max(
                    [
                        len(value) for value in (
                            config_errors[section].values()
                        )
                    ]
                )

                print(
                    "{:<8} {:<{len0}} {:<{len1}} {:<{len2}}".format(
                        '',
                        'Section',
                        'Key',
                        'Error',
                        len0=len0+4,
                        len1=len1+4,
                        len2=len2+4
                    )
                )
                print(
                    "{:<8} {:<{len0}} {:<{len1}} {:<{len2}}".format(
                        '',
                        '-------',
                        '---',
                        '-----',
                        len0=len0+4,
                        len1=len1+4,
                        len2=len2+4
                    )
                )

                for key, value in config_errors[section].items():
                    print(
                        ("{:<8} {:<{len0}} {:<{len1}} {:<{len2}}").format(
                            '',
                            section,
                            key,
                            value,
                            len0=len0+4,
                            len1=len1+4,
                            len2=len2+4
                        )
                    )
                print(
                    '\n'
                )
            else:
                pass
        raise TypeError(
            'Validation failed.'
        )
    else:
        return True
