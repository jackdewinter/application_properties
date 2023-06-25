"""
Tests for the get_boolean* functions of the ApplicationProperties class
"""
from application_properties import ApplicationProperties


def test_properties_get_boolean_with_found_value() -> None:
    """
    Test fetching a configuration value that is present and boolean.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = True

    # Act
    actual_value = application_properties.get_boolean_property("property", False)

    # Assert
    assert expected_value == actual_value


def test_properties_get_boolean_with_found_value_but_wrong_type() -> None:
    """
    Test fetching a configuration value that is present and not boolean.
    """

    # Arrange
    config_map = {"property": 1}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = True

    # Act
    actual_value = application_properties.get_boolean_property("property", True)

    # Assert
    assert expected_value == actual_value


def test_properties_get_boolean_with_not_found_value() -> None:
    """
    Test fetching a configuration value that is not present and boolean.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = True

    # Act
    actual_value = application_properties.get_boolean_property("other_property", True)

    # Assert
    assert expected_value == actual_value


def test_properties_get_boolean_with_not_found_value_and_no_default_value() -> None:
    """
    Test fetching a configuration value that is not present, with no default, and boolean.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    actual_value = application_properties.get_boolean_property("other_property")

    # Assert
    assert actual_value is None


def test_properties_get_boolean_with_a_bad_property_name() -> None:
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
        application_properties.get_boolean_property(1, 1)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The propertyName argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_get_boolean_with_a_bad_default() -> None:
    """
    Test fetching a configuration value with a default value that is not a boolean.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    raised_exception = None
    try:
        application_properties.get_boolean_property("property", 1)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The default value for property 'property' must either be None or a 'bool' value."
    ), "Expected message was not present in exception."
