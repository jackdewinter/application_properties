"""
Tests for the ApplicationProperties class
"""

from typing import Any, Dict

from application_properties import ApplicationProperties


def test_property_name_separator() -> None:
    """
    Test to make sure that the property name separator is as expected.
    """

    # Arrange
    application_properties = ApplicationProperties()
    expected_separator = "."

    # Act
    actual_separator = application_properties.separator

    # Assert
    assert actual_separator == expected_separator


def test_properties_with_object() -> None:
    """
    Test to make sure that a default application properties object has no properties.
    """

    # Arrange
    application_properties = ApplicationProperties()
    expected_property_count = 0

    # Act
    actual_property_count = application_properties.number_of_properties

    # Assert
    assert actual_property_count == expected_property_count


def test_properties_with_single_property() -> None:
    """
    Test a configuration map with a single property, and how that property looks.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {"enabled": True}
    expected_property_count = 1

    # Act
    application_properties.load_from_dict(config_map)
    actual_property_count = application_properties.number_of_properties
    found_names = application_properties.property_names

    # Assert
    assert actual_property_count == expected_property_count
    assert len(found_names) == expected_property_count
    assert "enabled" in found_names


def test_properties_with_single_nested_property() -> None:
    """
    Test a configuration map with a single nested property, and how that property looks.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {"feature": {"enabled": True}}
    expected_property_count = 1

    # Act
    application_properties.load_from_dict(config_map)
    actual_property_count = application_properties.number_of_properties
    found_names = application_properties.property_names

    # Assert
    assert actual_property_count == expected_property_count
    assert len(found_names) == expected_property_count
    assert "feature.enabled" in found_names


def test_properties_with_mixed_properties() -> None:
    """
    Test a configuration map with properties at different levels, and how those properties look.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {
        "feature": {"enabled": True},
        "other_feature": {"enabled": False, "other": 1},
    }
    expected_property_count = 3

    # Act
    application_properties.load_from_dict(config_map)
    actual_property_count = application_properties.number_of_properties
    found_names = application_properties.property_names

    # Assert
    assert actual_property_count == expected_property_count
    assert len(found_names) == expected_property_count
    assert "feature.enabled" in found_names
    assert "other_feature.enabled" in found_names
    assert "other_feature.other" in found_names


def test_get_properties_under_at_top_level_partial() -> None:
    """
    Test calling the `property_names_under` function specifying only part of the top level.
    """

    # Arrange
    config_map: Dict[str, Dict[str, Any]] = {
        "feature": {"enabled": True},
        "other_feature": {"enabled": False, "other": 1},
    }
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    found_names = application_properties.property_names_under("other_feature")

    # Assert
    assert len(found_names) == len(config_map["other_feature"])
    assert "other_feature.enabled" in found_names
    assert "other_feature.other" in found_names


def test_get_properties_under_at_top_level_none() -> None:
    """
    Test calling the `property_names_under` function specifying none of the top level.
    """

    # Arrange
    config_map: Dict[str, Dict[str, Any]] = {
        "feature": {"enabled": True},
        "other_feature": {"enabled": False, "other": 1},
    }
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    found_names = application_properties.property_names_under("missing_feature")

    # Assert
    assert not found_names
    assert "missing_feature" not in config_map


def test_get_properties_under_at_sub_level() -> None:
    """
    Test calling the `property_names_under` function specifying none of the top level.
    """

    # Arrange
    config_map = {
        "new_top_level": {
            "feature": {"enabled": True},
            "other_feature": {"enabled": False, "other": 1},
        }
    }
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    found_names = application_properties.property_names_under("new_top_level.feature")

    # Assert
    assert len(found_names) == 1
    assert "new_top_level.feature.enabled" in found_names


def test_properties_load_from_non_dictionary() -> None:
    """
    Test a loading a configuration map that is not a dictionary.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = [{"feature": True}]

    # Act
    raised_exception = None
    try:
        application_properties.load_from_dict(config_map)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "Specified parameter was not a dictionary."
    ), "Expected message was not present in exception."


def test_properties_load_with_non_string_key() -> None:
    """
    Test a loading a configuration map that contains a key that is not a string.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {1: True}

    # Act
    raised_exception = None
    try:
        application_properties.load_from_dict(config_map)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "All keys in the main dictionary and nested dictionaries must be strings."
    ), "Expected message was not present in exception."


def test_properties_load_with_key_containing_dot() -> None:
    """
    Test a loading a configuration map that contains a key with a '.' character.
    """

    # Arrange
    application_properties = ApplicationProperties()
    config_map = {"my.property": True}

    # Act
    raised_exception = None
    try:
        application_properties.load_from_dict(config_map)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Key strings cannot contain a whitespace character, a '=' character, or a '.' character."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_bad_type() -> None:
    """
    Test a fetching a configuration value where the generic function is
    used and the type and the default are confused.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property("property", False)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The property_type argument for 'property' must be a type."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_required_and_found() -> None:
    """
    Test a fetching a configuration value where the value is required and present.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = True

    # Act
    actual_value = application_properties.get_property(
        "property", bool, is_required=True
    )

    # Assert
    assert actual_value == expected_value


def test_properties_get_generic_with_required_and_not_found() -> None:
    """
    Test a fetching a configuration value where the value is required and not present.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property("other_property", bool, is_required=True)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "A value for property 'other_property' must be provided."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_strict_mode_and_bad_type() -> None:
    """
    Test a fetching a configuration value where strict mode is on and the type is not correct.
    """

    # Arrange
    config_map = {"property": 1}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property("property", str, strict_mode=True)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' must be of type 'str'."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_global_strict_mode_and_bad_type() -> None:
    """
    Test a fetching a configuration value where strict mode is on and the type is not correct.
    """

    # Arrange
    config_map = {"property": 1}
    application_properties = ApplicationProperties(strict_mode=True)
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property("property", str)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert application_properties.strict_mode
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' must be of type 'str'."
    ), "Expected message was not present in exception."


def test_properties_get_generic_with_delayed_global_strict_mode_and_bad_type() -> None:
    """
    Test a fetching a configuration value where strict mode is on through the
    delayed mechanism and the type is not correct.
    """

    # Arrange
    config_map = {"property": 1}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    application_properties.enable_strict_mode()

    # Act
    raised_exception = None
    try:
        application_properties.get_property("property", str)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert application_properties.strict_mode
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' must be of type 'str'."
    ), "Expected message was not present in exception."


def __sample_string_validation_function(property_value: str) -> None:
    """
    Simple string validation that throws an error if not "1" or "2".
    """
    if property_value not in ["1", "2"]:
        raise ValueError(f"Value '{property_value}' is not '1' or '2'")


def test_properties_get_generic_with_strict_mode_and_bad_validity() -> None:
    """
    Test a fetching a configuration value where strict mode is on and the value is not valid.
    """

    # Arrange
    config_map = {"property": "3"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_property(
            "property",
            str,
            strict_mode=True,
            valid_value_fn=__sample_string_validation_function,
        )
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The value for property 'property' is not valid: Value '3' is not '1' or '2'"
    ), "Expected message was not present in exception."
