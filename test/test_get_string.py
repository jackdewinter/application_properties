"""
Tests for the get_string* functions of the ApplicationProperties class
"""
from application_properties import ApplicationProperties


def test_properties_get_string_with_found_value():
    """
    Test fetching a configuration value that is present and string.
    """

    # Arrange
    config_map = {"property": "me"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "me"

    # Act
    actual_value = application_properties.get_string_property("property", "")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_found_value_but_wrong_type():
    """
    Test fetching a configuration value that is present and not string.
    """

    # Arrange
    config_map = {"property": True}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = ""

    # Act
    actual_value = application_properties.get_string_property("property", "")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_not_found_value():
    """
    Test fetching a configuration value that is not present and string.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "3"

    # Act
    actual_value = application_properties.get_string_property("other_property", "3")

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_not_found_value_and_no_default_value():
    """
    Test fetching a configuration value that is not present, with no default, and integer.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)

    # Act
    actual_value = application_properties.get_string_property("other_property")

    # Assert
    assert actual_value is None


def test_properties_get_string_with_found_value_validated():
    """
    Test fetching a configuration value that is present and adheres to the validation function.
    """

    # Arrange
    config_map = {"property": "2"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "2"

    # Act
    actual_value = application_properties.get_string_property(
        "property", "-", lambda property_value: property_value in ["1", "2"]
    )

    # Assert
    assert expected_value == actual_value


def __sample_string_validation_function(property_value):
    """
    Simple string validation that throws an error if not "1" or "2".
    """
    if property_value not in ["1", "2"]:
        raise ValueError("Value '" + str(property_value) + "' is not '1' or '2'")


def test_properties_get_string_with_found_value_not_validated():
    """
    Test fetching a configuration value that is present and does not adhere to the validation function.
    """

    # Arrange
    config_map = {"property": "3"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "-"

    # Act
    actual_value = application_properties.get_string_property(
        "property", "-", __sample_string_validation_function
    )

    # Assert
    assert expected_value == actual_value


def bad_validation_function(property_value):
    """
    Test validation function that always throws an exception.
    """
    # sourcery skip: raise-specific-error
    raise Exception(f"huh? {str(property_value)}")


def test_properties_get_string_with_found_value_validation_raises_error():
    """
    Test fetching a configuration value that is present and the validation function raises an error.
    """

    # Arrange
    config_map = {"property": "1"}
    application_properties = ApplicationProperties()
    application_properties.load_from_dict(config_map)
    expected_value = "-"

    # Act
    actual_value = application_properties.get_string_property(
        "property", "-", bad_validation_function
    )

    # Assert
    assert expected_value == actual_value


def test_properties_get_string_with_a_bad_property_name():
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
        application_properties.get_string_property(1, "3")
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "The propertyName argument must be a string."
    ), "Expected message was not present in exception."


def test_properties_get_string_with_a_bad_default():
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
        application_properties.get_string_property("property", True)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "The default value for property 'property' must either be None or a 'str' value."
    ), "Expected message was not present in exception."
