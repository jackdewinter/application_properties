"""
Module to provide helper methods for tests.
"""

import json
import os
import tempfile
from contextlib import contextmanager
from typing import Any, Generator, Optional, Union


class TestHelpers:
    """
    Class to provide helper methods for tests.
    """

    @staticmethod
    def write_temporary_configuration(
        supplied_configuration: Union[str, Any],
        file_name: Optional[str] = None,
        directory: Optional[str] = None,
    ) -> str:
        """
        Write the configuration as a temporary file that is kept around.
        """
        if file_name:
            full_file_name = str(
                os.path.join(directory, file_name) if directory else file_name
            )
            with open(full_file_name, "wt", encoding="utf-8") as outfile:
                if isinstance(supplied_configuration, str):
                    outfile.write(supplied_configuration)
                else:
                    json.dump(supplied_configuration, outfile)
                return full_file_name
        else:
            try:
                with tempfile.NamedTemporaryFile(
                    "wt", delete=False, dir=directory
                ) as outfile:
                    if isinstance(supplied_configuration, str):
                        outfile.write(supplied_configuration)
                    else:
                        json.dump(supplied_configuration, outfile)
                    return outfile.name
            except IOError as ex:
                raise AssertionError(
                    f"Test configuration file was not written ({str(ex)})."
                ) from ex

    @staticmethod
    @contextmanager
    def change_to_temporary_directory() -> Generator[str, None, None]:
        """
        Context manager to temporarily change to a given directory.
        """
        old_current_working_directory = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp_dir_path:
            try:
                os.chdir(tmp_dir_path)
                yield tmp_dir_path
            finally:
                os.chdir(old_current_working_directory)


# pylint: disable=too-few-public-methods
class ErrorResults:
    """
    Class to collect the error results.
    """

    def __init__(self) -> None:
        self.reported_error: str

    def keep_error(
        self, formatted_error: str, thrown_exception: Optional[Exception]
    ) -> None:
        """
        Deal with the error by keeping a record of it to compare.
        """
        _ = thrown_exception
        self.reported_error = formatted_error


# pylint: enable=too-few-public-methods
