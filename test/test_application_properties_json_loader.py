"""
Tests for the ApplicationProperties class
"""
import io
import json
import os
import sys
import tempfile

from application_properties import (
    ApplicationProperties,
    ApplicationPropertiesJsonLoader,
)


def write_temporary_configuration(supplied_configuration):
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


def test_json_loader_valid_json():
    """
    Test to make sure that we can load a valid Json file.
    """

    # Arrange
    supplied_configuration = {"plugins": {"md999": {"test_value": 2}}}
    expected_value = 2

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        ApplicationPropertiesJsonLoader.load_and_set(
            application_properties, configuration_file, None
        )
        actual_value = application_properties.get_integer_property(
            "plugins.md999.test_value", -1
        )

        # Assert
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_invalid_json():
    """
    Test to make sure that we cannot load an invalid Json file.
    """

    # Arrange
    supplied_configuration = "this is not a json file"

    handled_error_parameters = []

    def inner_func(formatted_error, this_exception):
        handled_error_parameters.append(formatted_error)
        handled_error_parameters.append(this_exception)

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        ApplicationPropertiesJsonLoader.load_and_set(
            application_properties, configuration_file, handle_error_fn=inner_func
        )

        # Assert
        assert handled_error_parameters
        assert handled_error_parameters[0].startswith("Specified configuration file ")
        assert (
            "' is not a valid JSON file (Expecting value: line 1 column 1 (char 0))."
            in handled_error_parameters[0]
        )
        assert isinstance(handled_error_parameters[1], json.decoder.JSONDecodeError)
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_missing_file():
    """
    Test to make sure that we fail to load a file that isn't there.
    """

    # Arrange
    handled_error_parameters = []

    def inner_func(formatted_error, this_exception):
        handled_error_parameters.append(formatted_error)
        handled_error_parameters.append(this_exception)

    configuration_file = "missing_file_name.other"
    assert not os.path.exists(configuration_file)
    application_properties = ApplicationProperties()

    # Act
    ApplicationPropertiesJsonLoader.load_and_set(
        application_properties, configuration_file, handle_error_fn=inner_func
    )

    # Assert
    assert handled_error_parameters
    assert handled_error_parameters[0].startswith(
        "Specified configuration file 'missing_file_name.other' was not loaded"
    )
    assert isinstance(handled_error_parameters[1], FileNotFoundError)


def test_json_loader_valid_json_but_invalid_key():
    """
    Test to make sure that we can load a valid Json file, but fail when there is an invalid key.
    """

    # Arrange
    supplied_configuration = {"plugins": {"md999": {"test.value": 2}}}

    handled_error_parameters = []

    def inner_func(formatted_error, this_exception):
        handled_error_parameters.append(formatted_error)
        handled_error_parameters.append(this_exception)

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        ApplicationPropertiesJsonLoader.load_and_set(
            application_properties, configuration_file, inner_func
        )

        # Assert
        assert handled_error_parameters
        assert handled_error_parameters[0].startswith("Specified configuration file '")
        assert (
            "' is not valid (Keys strings cannot contain the separator character '.'.)."
            in handled_error_parameters[0]
        )
        assert isinstance(handled_error_parameters[1], ValueError)
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_valid_json_but_invalid_key_xx():
    """
    Test to make sure that we can load a valid Json file, but fail when there is an invalid key.
    """

    # Arrange
    supplied_configuration = {"plugins": {"md999": {"test.value": 2}}}

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        new_stdout = io.StringIO()
        new_stderr = io.StringIO()
        try:
            sys.stdout = new_stdout
            sys.stderr = new_stderr

            ApplicationPropertiesJsonLoader.load_and_set(
                application_properties, configuration_file
            )
        finally:
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        # Assert
        assert new_stdout.getvalue().startswith("Specified configuration file '")
        assert (
            "' is not valid (Keys strings cannot contain the separator character '.'.)."
            in new_stdout.getvalue()
        )
        assert not new_stderr.getvalue()
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_pair_valid_json():
    """
    Test to make sure that we can load more than one configuration file and not have
    the configurations stomp on each other in an unpredictable manner.
    """

    # Arrange
    supplied_configuration_first = {
        "plugins": {"md999": {"test_value_a": 2, "test_value_b": 3}}
    }
    supplied_configuration_second = {
        "plugins": {"md999": {"test_value_b": 4, "test_value_c": 5}}
    }
    expected_value_a = 2
    expected_value_b = 4
    expected_value_c = 5

    configuration_file_first = None
    try:
        configuration_file_first = write_temporary_configuration(
            supplied_configuration_first
        )
        configuration_file_second = write_temporary_configuration(
            supplied_configuration_second
        )
        application_properties = ApplicationProperties()

        # Act
        ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            configuration_file_first,
            None,
            clear_property_map=False,
        )
        ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            configuration_file_second,
            None,
            clear_property_map=False,
        )
        actual_value_a = application_properties.get_integer_property(
            "plugins.md999.test_value_a", -1
        )
        actual_value_b = application_properties.get_integer_property(
            "plugins.md999.test_value_b", -1
        )
        actual_value_c = application_properties.get_integer_property(
            "plugins.md999.test_value_c", -1
        )

        # Assert
        assert expected_value_a == actual_value_a
        assert expected_value_b == actual_value_b
        assert expected_value_c == actual_value_c
    finally:
        if configuration_file_first and os.path.exists(configuration_file_first):
            os.remove(configuration_file_first)
        if configuration_file_second and os.path.exists(configuration_file_second):
            os.remove(configuration_file_second)
