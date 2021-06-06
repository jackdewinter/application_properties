"""
Module to provide for a manner to load an ApplicationProperties object from a JSON file.
"""
import json


# pylint: disable=too-few-public-methods
class ApplicationPropertiesJsonLoader:
    """
    Class to provide for a manner to load an ApplicationProperties object from a JSON file.
    """

    @staticmethod
    def load_and_set(properties_object, configuration_file, handle_error_fn=None):
        """
        Load the specified file and set it into the given properties object.
        """

        if not handle_error_fn:

            def print_error_to_stdout(formatted_error, thrown_exception):
                _ = thrown_exception
                print(formatted_error)

            handle_error_fn = print_error_to_stdout

        configuration_map = None
        try:
            with open(configuration_file) as infile:
                configuration_map = json.load(infile)
        except json.decoder.JSONDecodeError as this_exception:
            formatted_error = f"Specified configuration file '{configuration_file}' is not a valid JSON file ({str(this_exception)})."
            handle_error_fn(formatted_error, this_exception)
        except IOError as this_exception:
            formatted_error = f"Specified configuration file '{configuration_file}' was not loaded ({str(this_exception)})."
            handle_error_fn(formatted_error, this_exception)

        if configuration_map:
            try:
                properties_object.load_from_dict(configuration_map)
            except ValueError as this_exception:
                formatted_error = f"Specified configuration file '{configuration_file}' is not valid ({str(this_exception)})."
                handle_error_fn(formatted_error, this_exception)


# pylint: enable=too-few-public-methods
