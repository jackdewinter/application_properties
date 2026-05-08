"""
Tests for the get_string_list* functions of the ApplicationProperties class
"""

from typing import Any, Dict, List

from application_properties import ApplicationProperties


def test_properties_get_string_list_with_found_string_value_single() -> None:
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": "me"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["me"]

    # Act
    actual_value = application_properties.get_string_list_property("property", ",")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_list_value_single() -> None:
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": ["me", "myself"]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["me", "myself"]

    # Act
    actual_value = application_properties.get_string_list_property("property", ",")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_string_value_multiple() -> None:
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": "me,you"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["me", "you"]

    # Act
    actual_value = application_properties.get_string_list_property("property", ",")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_string_value_multiple_with_whitespace() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": " me , you "}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["me", "you"]

    # Act
    actual_value = application_properties.get_string_list_property("property", ",")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_list_value_multiple() -> None:
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": ["me", "you"]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["me", "you"]

    # Act
    actual_value = application_properties.get_string_list_property("property", ",")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_list_value_multiple_with_whitespace() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": [" me ", " you ", " and them "]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["me", "you", "and them"]

    # Act
    actual_value = application_properties.get_string_list_property("property", ",")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_string_value_multiple_with_empty_strict_mode_on() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": "me,,you"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(
            "property", ",", strict_mode=True
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Configuration item 'property' contains at least one empty element."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_found_string_value_multiple_with_empty_strict_mode_off() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": "me,,you"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = None

    # Act
    actual_value = application_properties.get_string_list_property(
        "property", ",", strict_mode=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_string_value_multiple_with_only_ws_strict_mode_on() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": "me, ,you"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(
            "property", ",", strict_mode=True
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Configuration item 'property' contains at least one empty element."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_found_string_value_multiple_with_only_ws_strict_mode_off() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": "me, ,you"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = None

    # Act
    actual_value = application_properties.get_string_list_property(
        "property", ",", strict_mode=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_list_value_multiple_with_empty_strict_mode_on() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": ["me", "", "you"]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(
            "property", ",", strict_mode=True
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Configuration item 'property' contains at least one empty element."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_found_list_value_multiple_with_empty_strict_mode_off() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": ["me", "", "you"]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = None

    # Act
    actual_value = application_properties.get_string_list_property(
        "property", ",", strict_mode=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_list_value_multiple_with_only_ws_strict_mode_on() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": ["me", " ", "you"]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(
            "property", ",", strict_mode=True
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Configuration item 'property' contains at least one empty element."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_found_list_value_multiple_with_only_ws_strict_mode_off() -> (
    None
):
    """
    Test fetching a configuration value that is present and a simple string.
    """

    # Arrange
    config_map = {"property": ["me", " ", "you"]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = None

    # Act
    actual_value = application_properties.get_string_list_property(
        "property", ",", strict_mode=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_value_but_wrong_type_strict_mode_on() -> (
    None
):
    """
    Test fetching a configuration value that is present and not a string.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(
            "property", ",", strict_mode=True
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' must be of type 'str' or type 'List[str]'."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_found_value_but_wrong_type_strict_mode_off() -> (
    None
):
    """
    Test fetching a configuration value that is present and not a string.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = None

    # Act
    actual_value = application_properties.get_string_list_property(
        "property", ",", strict_mode=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_list_but_contains_wrong_type_strict_mode_on() -> (
    None
):
    """
    Test fetching a configuration value that is present and not a string.
    """

    # Arrange
    config_map: Dict[str, Any] = {"property": ["1", True]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(
            "property", ",", strict_mode=True
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Configuration item 'property' contains at least one non-string element: True."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_found_list_but_contains_wrong_type_strict_mode_off() -> (
    None
):
    """
    Test fetching a configuration value that is present and not a string.
    """

    # Arrange
    config_map: Dict[str, Any] = {"property": ["1", True]}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = None

    # Act
    actual_value = application_properties.get_string_list_property(
        "property", ",", strict_mode=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_not_found_and_no_default_value() -> None:
    """
    Test fetching a configuration value that is not present and a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = None

    # Act
    actual_value = application_properties.get_string_list_property(
        "other_property", ","
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_not_found_value_and_default_value() -> None:
    """
    Test fetching a configuration value that is not present and a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["me"]

    # Act
    actual_value = application_properties.get_string_list_property(
        "other_property", ",", ["me"]
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_not_found_and_required() -> None:
    """
    Test fetching a configuration value that is not present and a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(
            "other_property", ",", is_required=True
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "A value for property 'other_property' must be provided."
    ), "Expected message was not present in exception."


def _get_string_list_with_found_value_validated_function(
    property_value: List[str],
) -> Any:
    """
    Simple string validation that throws an error if not "1" or "2".
    """
    for i in property_value:
        if i not in ["1", "2"]:
            raise ValueError(f"Value '{i}' in list is not '1' or '2'")


def test_properties_get_string_list_with_found_value_valid() -> None:
    """
    Test fetching a configuration value that is present and adheres to the validation function.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["2"]

    # Act
    actual_value = application_properties.get_string_list_property(
        "property", ",", ["-"], _get_string_list_with_found_value_validated_function
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_value_not_valid_strict_mode_off() -> (
    None
):
    """
    Test fetching a configuration value that is present and does not adhere to the validation function.
    """

    # Arrange
    config_map = {"property": "3"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["-"]

    # Act
    actual_value = application_properties.get_string_list_property(
        "property",
        ",",
        ["-"],
        _get_string_list_with_found_value_validated_function,
        strict_mode=False,
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_found_value_not_valid_strict_mode_on() -> None:
    """
    Test fetching a configuration value that is present and does not adhere to the validation function.
    """

    # Arrange
    config_map = {"property": "3"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(
            "property",
            ",",
            ["-"],
            _get_string_list_with_found_value_validated_function,
            strict_mode=True,
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' is not valid: Value '3' in list is not '1' or '2'"
    ), "Expected message was not present in exception."


# pylint: disable=broad-exception-raised
def bad_validation_function(property_value: List[str]) -> Any:
    """
    Test validation function that always throws an exception.
    """
    # sourcery skip: raise-specific-error
    raise Exception(f"huh? {property_value}")


# pylint: enable=broad-exception-raised


def test_properties_get_string_list_with_found_value_validation_raises_error() -> None:
    """
    Test fetching a configuration value that is present and the validation function raises an error.
    """

    # Arrange
    config_map = {"property": "1"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ["-"]

    # Act
    actual_value = application_properties.get_string_list_property(
        "property", ",", ["-"], bad_validation_function
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_list_with_a_bad_property_name() -> None:
    """
    Test fetching a configuration value with a bad property name.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property(1, ",", ["3"])  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The propertyName argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_a_bad_separator() -> None:
    """
    Test fetching a configuration value with a default value that is not a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property("property", True)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value_separator_if_string argument must be a non-empty string."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_an_empty_separator() -> None:
    """
    Test fetching a configuration value with a default value that is not a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property("property", "")
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value_separator_if_string argument must be a non-empty string."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_a_bad_default_type() -> None:
    """
    Test fetching a configuration value with a default value that is not a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property("property", ",", True)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The default value for property 'property' must either be None or a list of 'str' values."
    ), "Expected message was not present in exception."


def test_properties_get_string_list_with_a_bad_default_bad_element_type() -> None:
    """
    Test fetching a configuration value with a default value that is not a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_string_list_property("property", ",", [1])  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The default value for property 'property' must either be None or a list of 'str' values."
    ), "Expected message was not present in exception."
