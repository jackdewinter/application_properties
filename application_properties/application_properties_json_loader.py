"""
Module to provide for a manner to load an ApplicationProperties object from a JSON file.
"""
import json
from typing import Any, Callable, Dict, Optional

from application_properties.application_properties import ApplicationProperties


# pylint: disable=too-few-public-methods
class ApplicationPropertiesJsonLoader:
    """
    Class to provide for a manner to load an ApplicationProperties object from a JSON file.
    """

    @staticmethod
    def load_and_set(
        properties_object: ApplicationProperties,
        configuration_file: str,
        handle_error_fn: Optional[Callable[[str, Exception], None]] = None,
        clear_property_map: bool = True,
    ) -> bool:
        """
        Load the specified file and set it into the given properties object.
        """

        if not handle_error_fn:

            def print_error_to_stdout(
                formatted_error: str, thrown_exception: Exception
            ) -> None:
                _ = thrown_exception
                print(formatted_error)

            handle_error_fn = print_error_to_stdout

        configuration_map: Dict[Any, Any] = {}
        try:
            with open(configuration_file, encoding="utf-8") as infile:
                configuration_map = json.load(infile)
        except json.decoder.JSONDecodeError as this_exception:
            formatted_error = (
                f"Specified configuration file '{configuration_file}' "
                + f"is not a valid JSON file: {str(this_exception)}."
            )
            handle_error_fn(formatted_error, this_exception)
        except IOError as this_exception:
            formatted_error = (
                f"Specified configuration file '{configuration_file}' "
                + f"was not loaded: {str(this_exception)}."
            )
            handle_error_fn(formatted_error, this_exception)

        did_apply_map = False
        if configuration_map:
            try:
                properties_object.load_from_dict(
                    configuration_map, clear_map=clear_property_map
                )
                did_apply_map = True
            except ValueError as this_exception:
                formatted_error = (
                    f"Specified configuration file '{configuration_file}' "
                    + f"is not valid: {str(this_exception)}"
                )
                handle_error_fn(formatted_error, this_exception)
        return did_apply_map


# pylint: enable=too-few-public-methods
