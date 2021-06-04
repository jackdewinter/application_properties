"""
Tests for the ApplicationPropertiesFacade class
"""
from application_properties.application_properties import (
    ApplicationProperties,
    ApplicationPropertiesFacade,
)


def test_properties_facade_base_not_properties_object():
    """
    Test setting up a facade with properties object that is not a properties object.
    """

    # Arrange

    # Act
    raised_exception = None
    try:
        ApplicationPropertiesFacade(1, 1)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The base_properties of the facade must be an ApplicationProperties instance."
    ), "Expected message was not present in exception."


def test_properties_facade_prefix_not_string():
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
        ApplicationPropertiesFacade(application_properties, 1)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The property_prefix argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_facade_prefix_not_terminated_with_separator():
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
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The property_prefix argument must end with the separator character '.'."
    ), "Expected message was not present in exception."


def test_properties_facade_get_with_found_value():
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


def test_properties_facade_get_boolean_with_found_value():
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


def test_properties_facade_get_integer_with_found_value():
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


def test_properties_facade_get_string_with_found_value():
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


def test_properties_facade_get_property_names_with_one_value():
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
    print(str(type(expected_value)))
    print(str(type(actual_value)))
    assert expected_value == actual_value


def test_properties_facade_get_property_names_with_no_values():
    """
    Test fetching through a configuration facade the property names without a single property value.
    """

    # Arrange
    config_map = {"upper": {"property": "2"}}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    facade = ApplicationPropertiesFacade(application_properties, "uppers.")
    expected_value = []

    # Act
    actual_value = facade.property_names

    # Assert
    print(str(type(expected_value)))
    print(str(type(actual_value)))
    assert expected_value == actual_value
