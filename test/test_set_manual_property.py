"""
Tests for the set_manual_property related functions of the ApplicationProperties class
"""
from application_properties.application_properties import ApplicationProperties


def test_properties_set_manual_property_with_non_string():
    """
    Test to make sure that a manual property with a non-string is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_string = 1

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property form must either be a string or an iterable of strings."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_no_equals():
    """
    Test to make sure that a full key with no value part is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_string = "a_property"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property key and value must be separated by the '=' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_single_part_string():
    """
    Test to make sure that a full key specifying an string without any format is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = "123"
    full_string = f"{full_property_key}={property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_string_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_only_format_indicator():
    """
    Test to make sure that a full key specifying an string format but with no format character following is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = "$123"
    full_string = f"{full_property_key}={property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_string_property(full_property_key)
    assert property_value[1:] == actual_value


def test_properties_set_manual_property_with_string_indicator():
    """
    Test to make sure that a full key specifying an string is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = "$$123"
    full_string = f"{full_property_key}={property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_string_property(full_property_key)
    assert property_value[2:] == actual_value


def test_properties_set_manual_property_with_integer_indicator():
    """
    Test to make sure that a full key specifying an integer is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_integer_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_integer_indicator_and_bad_integer():
    """
    Test to make sure that a full key specifying a bad integer is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}a"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property value '$#123a' cannot be translated into an integer."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_boolean_indicator():
    """
    Test to make sure that a full key specifying a True boolean is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}=$!{property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_boolean_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_uncased_boolean_indicator():
    """
    Test to make sure that a full key specifying a True boolean in lower case is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}=$!{str(property_value).lower()}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.get_boolean_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_multiples():
    """
    Test to make sure that a list of full keys is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}=$!{property_value}"

    # Act
    application_properties.set_manual_property([full_string])

    # Assert
    actual_value = application_properties.get_boolean_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_bad_key_start():
    """
    Test to make sure that a full key starting with the key separator character is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = ".a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key must not start or end with the '.' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_bad_key_end():
    """
    Test to make sure that a full key ending with the key separator character is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a."
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key must not start or end with the '.' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_empty_key_middle():
    """
    Test to make sure that an empty key part for the full key is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a..a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key cannot contain multiples of the . without any text between them."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_empty_key():
    """
    Test to make sure that a key with an empty key part is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = ""
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Each part of the property key must contain at least one character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_whitespace_key():
    """
    Test to make sure that a key with whitespace is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a a"
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Each part of the property key must not contain a whitespace character or the '.' character."
    ), "Expected message was not present in exception."


def test_properties_verify_manual_property_form_with_non_string():
    """
    Test to make sure that if we try and test the verification form function
    with a non-string, it fails predictably.
    """

    # Arrange
    full_string = 1

    # Act
    raised_exception = None
    try:
        ApplicationProperties.verify_manual_property_form(full_string)
        assert False, "Should have raised an exception by now."
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "Manual property form must be a string."
    ), "Expected message was not present in exception."
