"""
Module to provide helper methods for tests.
"""
import json
import tempfile
from typing import Any, Optional, Union


# pylint: disable=too-few-public-methods
class TestHelpers:
    """
    Class to provide helper methods for tests.
    """

    @staticmethod
    def write_temporary_configuration(supplied_configuration: Union[str, Any]) -> str:
        """
        Write the configuration as a temporary file that is kept around.
        """
        try:
            with tempfile.NamedTemporaryFile("wt", delete=False) as outfile:
                if isinstance(supplied_configuration, str):
                    outfile.write(supplied_configuration)
                else:
                    json.dump(supplied_configuration, outfile)
                return outfile.name
        except IOError as ex:
            raise AssertionError(
                f"Test configuration file was not written ({str(ex)})."
            ) from ex


# pylint: enable=too-few-public-methods


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
