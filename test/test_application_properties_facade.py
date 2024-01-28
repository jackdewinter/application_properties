"""
Tests for the ApplicationPropertiesFacade class
"""

from typing import Any, Dict, List

from application_properties import ApplicationProperties, ApplicationPropertiesFacade


def test_properties_facade_base_not_properties_object() -> None:
    """
    Test setting up a facade with properties object that is not a properties object.
    """

    # Arrange

    # Act
    raised_exception = None
    try:
        ApplicationPropertiesFacade(1, 1)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The base_properties of the facade must be an ApplicationProperties instance."
    ), "Expected message was not present in exception."


def test_properties_facade_prefix_not_string() -> None:
    """
    Test setting up a facade with a prefix that is not a string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        ApplicationPropertiesFacade(application_properties, 1)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The property_prefix argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_facade_prefix_not_terminated_with_separator() -> None:
    """
    Test setting up a facade with a prefix that is not terminated with the separator.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        ApplicationPropertiesFacade(application_properties, "my")
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The property_prefix argument must end with the separator character '.'."
    ), "Expected message was not present in exception."


def test_properties_facade_get_with_found_value() -> None:
    """
    Test fetching through a configuration facade for a property that is present.
    """

    # Arrange
    config_map = {"upper": {"property": 1.2}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = 1.2

    # Act
    actual_value = facade.get_property("property", float)

    # Assert
    assert expected_value == actual_value


def test_properties_facade_get_boolean_with_found_value() -> None:
    """
    Test fetching through a configuration facade for a boolean property that is present.
    """

    # Arrange
    config_map = {"upper": {"property": True}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = True

    # Act
    actual_value = facade.get_boolean_property("property")

    # Assert
    assert expected_value == actual_value


def test_properties_facade_get_integer_with_found_value() -> None:
    """
    Test fetching through a configuration facade for an integer property that is present.
    """

    # Arrange
    config_map = {"upper": {"property": 2}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = 2

    # Act
    actual_value = facade.get_integer_property("property")

    # Assert
    assert expected_value == actual_value


def test_properties_facade_get_string_with_found_value() -> None:
    """
    Test fetching through a configuration facade for a string property that is present.
    """

    # Arrange
    config_map = {"upper": {"property": "2"}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = "2"

    # Act
    actual_value = facade.get_string_property("property")

    # Assert
    assert expected_value == actual_value


def test_properties_facade_get_property_names_with_one_value() -> None:
    """
    Test fetching through a configuration facade the property names for a single property value.
    """

    # Arrange
    config_map = {"upper": {"property": "2"}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")
    expected_value = ["property"]

    # Act
    actual_value = facade.property_names

    # Assert
    print(type(expected_value))
    print(type(actual_value))
    assert expected_value == actual_value


def test_properties_facade_get_property_names_with_no_values() -> None:
    """
    Test fetching through a configuration facade the property names without a single property value.
    """

    # Arrange
    config_map: Dict[str, Dict[str, Any]] = {"upper": {"property": "2"}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "uppers.")
    expected_value: List[str] = []

    # Act
    actual_value = facade.property_names

    # Assert
    print(type(expected_value))
    print(type(actual_value))
    assert expected_value == actual_value


def test_properties_facade_get_properties_under_at_top_level_partial() -> None:
    """
    Test calling the `property_names_under` function specifying only part of the top level.
    """

    # Arrange
    config_map: Dict[str, Dict[str, Any]] = {
        "upper": {
            "feature": {"enabled": True},
            "other_feature": {"enabled": False, "other": 1},
        }
    }
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")

    # Act
    found_names = facade.property_names_under("other_feature")

    # Assert
    assert len(found_names) == len(config_map["upper"]["other_feature"])
    assert "other_feature.enabled" in found_names
    assert "other_feature.other" in found_names


def test_properties_facade_get_properties_under_at_top_level_none() -> None:
    """
    Test calling the `property_names_under` function specifying none of the top level.
    """

    # Arrange
    config_map: Dict[str, Dict[str, Any]] = {
        "upper": {
            "feature": {"enabled": True},
            "other_feature": {"enabled": False, "other": 1},
        }
    }
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")

    # Act
    found_names = facade.property_names_under("missing_feature")

    # Assert
    assert not found_names
    assert "missing_feature" not in config_map["upper"]


def test_properties_facade_get_properties_under_at_sub_level() -> None:
    """
    Test calling the `property_names_under` function specifying none of the top level.
    """

    # Arrange
    config_map: Dict[str, Dict[str, Dict[str, Any]]] = {
        "upper": {
            "new_top_level": {
                "feature": {"enabled": True},
                "other_feature": {"enabled": False, "other": 1},
            }
        }
    }
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "upper.")

    # Act
    found_names = facade.property_names_under("new_top_level.feature")

    # Assert
    assert len(found_names) == len(config_map["upper"]["new_top_level"]["feature"])
    assert "new_top_level.feature.enabled" in found_names
