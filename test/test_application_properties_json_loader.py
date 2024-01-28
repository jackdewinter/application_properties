"""
Tests for the ApplicationProperties class
"""

import io
import json
import os
import sys
from test.pytest_helpers import TestHelpers
from typing import Any, List, Optional

from application_properties import (
    ApplicationProperties,
    ApplicationPropertiesJsonLoader,
)


def test_json_loader_config_not_present() -> None:
    """
    Test to make sure that we do not try and load a configuration file that is not present.
    """

    # Arrange
    configuration_file = "does-not-exist"
    configuration_file = os.path.abspath(configuration_file)
    assert not os.path.exists(configuration_file)
    application_properties = ApplicationProperties()

    expected_did_apply = False
    expected_did_error = False
    expected_value = -1

    # Act
    actual_did_apply, actual_did_error = ApplicationPropertiesJsonLoader.load_and_set(
        application_properties, configuration_file, None, True, True
    )
    actual_value = application_properties.get_integer_property(
        "plugins.md999.test_value", -1
    )

    # Assert
    assert expected_value == actual_value
    assert expected_did_error == actual_did_error
    assert expected_did_apply == actual_did_apply


def test_json_loader_valid_json() -> None:
    """
    Test to make sure that we can load a valid Json file.
    """

    # Arrange
    supplied_configuration = {"plugins": {"md999": {"test_value": 2}}}
    expected_value = 2
    expected_did_apply = True
    expected_did_error = False

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties, configuration_file
        )
        actual_value = application_properties.get_integer_property(
            "plugins.md999.test_value", -1, None
        )

        # Assert
        assert expected_value == actual_value
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_valid_json_but_wrong_get_property_type() -> None:
    """
    Test to make sure that we can load a valid Json file, even if the property
    we are looking for is of the wrong type.  The load should succeed, even
    if the get fails.
    """

    # Arrange
    supplied_configuration = {"plugins": {"md999": {"test_value": "2"}}}
    expected_error = (
        "The value for property 'plugins.md999.test_value' must be of type 'int'."
    )
    expected_did_apply = True
    expected_did_error = False

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        # Act
        captured_exception = None
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties, configuration_file
        )
        try:
            application_properties.get_integer_property(
                "plugins.md999.test_value", -1, None, strict_mode=True
            )
        except ValueError as this_exception:
            captured_exception = this_exception

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert not application_properties.convert_untyped_if_possible
        assert captured_exception is not None
        assert str(captured_exception) == expected_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_valid_json_but_wrong_get_property_type_with_untyped_conversion() -> (
    None
):
    """
    Test to make sure that we can load a valid Json file, even if the property
    we are looking for is of the wrong type.  The load should succeed, even
    if the get fails.  The get should still fail as JSON is a typed source.
    """

    # Arrange
    supplied_configuration = {"plugins": {"md999": {"test_value": "2"}}}
    expected_error = (
        "The value for property 'plugins.md999.test_value' must be of type 'int'."
    )
    expected_did_apply = True
    expected_did_error = False

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(convert_untyped_if_possible=True)

        # Act
        captured_exception = None
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties, configuration_file
        )
        try:
            application_properties.get_integer_property(
                "plugins.md999.test_value", -1, None, strict_mode=True
            )
        except ValueError as this_exception:
            captured_exception = this_exception

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert application_properties.convert_untyped_if_possible
        assert captured_exception is not None
        assert str(captured_exception) == expected_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_invalid_json() -> None:
    """
    Test to make sure that we cannot load an invalid Json file.
    """

    # Arrange
    supplied_configuration = "this is not a json file"
    expected_did_apply = False
    expected_did_error = True

    handled_error_parameters: List[Any] = []

    def inner_func(formatted_error: str, this_exception: Optional[Exception]) -> None:
        handled_error_parameters.append(formatted_error)
        handled_error_parameters.append(this_exception)

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties, configuration_file, handle_error_fn=inner_func
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert handled_error_parameters
        assert handled_error_parameters[0].startswith("Specified configuration file ")
        assert (
            "' is not a valid JSON file: Expecting value: line 1 column 1 (char 0)."
            in handled_error_parameters[0]
        )
        assert isinstance(handled_error_parameters[1], json.decoder.JSONDecodeError)
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_missing_file() -> None:
    """
    Test to make sure that we fail to load a file that isn't there.
    """

    # Arrange
    expected_did_apply = False
    expected_did_error = True
    handled_error_parameters: List[Any] = []

    def inner_func(formatted_error: str, this_exception: Optional[Exception]) -> None:
        handled_error_parameters.append(formatted_error)
        handled_error_parameters.append(this_exception)

    configuration_file = "missing_file_name.other"
    assert not os.path.exists(configuration_file)
    application_properties = ApplicationProperties()

    # Act
    actual_did_apply, actual_did_error = ApplicationPropertiesJsonLoader.load_and_set(
        application_properties,
        configuration_file,
        handle_error_fn=inner_func,
        check_for_file_presence=False,
    )

    # Assert
    assert expected_did_apply == actual_did_apply
    assert expected_did_error == actual_did_error
    assert handled_error_parameters
    assert handled_error_parameters[0].startswith(
        "Specified configuration file 'missing_file_name.other' was not loaded: "
    )
    assert isinstance(handled_error_parameters[1], FileNotFoundError)


def test_json_loader_valid_json_but_invalid_key() -> None:
    """
    Test to make sure that we can load a valid Json file, but fail when there is an invalid key.
    """

    # Arrange
    supplied_configuration = {"plugins": {"md999": {"test.value": 2}}}
    expected_did_apply = False
    expected_did_error = True

    handled_error_parameters: List[Any] = []

    def inner_func(formatted_error: str, this_exception: Optional[Exception]) -> None:
        handled_error_parameters.append(formatted_error)
        handled_error_parameters.append(this_exception)

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties, configuration_file, inner_func
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert handled_error_parameters
        assert handled_error_parameters[0].startswith("Specified configuration file '")
        assert (
            "' is not valid: Key strings cannot contain a whitespace character, a '=' character, or a '.' character."
            in handled_error_parameters[0]
        )
        assert isinstance(handled_error_parameters[1], ValueError)
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_valid_json_but_invalid_key_with_stdin_capture() -> None:
    """
    Test to make sure that we can load a valid Json file, but fail when there is an invalid key.
    """

    # Arrange
    supplied_configuration = {"plugins": {"md999": {"test.value": 2}}}
    expected_did_apply = False
    expected_did_error = True

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        # Act
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        new_stdout = io.StringIO()
        new_stderr = io.StringIO()
        try:
            sys.stdout = new_stdout
            sys.stderr = new_stderr

            (
                actual_did_apply,
                actual_did_error,
            ) = ApplicationPropertiesJsonLoader.load_and_set(
                application_properties, configuration_file
            )
        finally:
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert new_stdout.getvalue().startswith("Specified configuration file '")
        assert (
            "' is not valid: Key strings cannot contain a whitespace character, a '=' character, or a '.' character."
            in new_stdout.getvalue()
        )
        assert not new_stderr.getvalue()
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_json_loader_pair_valid_json() -> None:
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
        configuration_file_first = TestHelpers.write_temporary_configuration(
            supplied_configuration_first
        )
        configuration_file_second = TestHelpers.write_temporary_configuration(
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
