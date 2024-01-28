"""
Tests for the set_manual_property related functions of the ApplicationProperties class
"""

from typing import List

from application_properties import ApplicationProperties


def test_properties_set_manual_property_with_non_string() -> None:
    """
    Test to make sure that a manual property with a non-string is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_string = 1

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property form must either be a string or an iterable of strings."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_no_equals() -> None:
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
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property key and value must be separated by the '=' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_single_part_string() -> None:
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


def test_properties_set_manual_property_shows_up_in_property_names() -> None:
    """
    Test to make sure that a full key specifying an string without any format shows
    up properly in the properrt names list.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = ["a"]
    full_string = f"{full_property_key}={property_value}"

    # Act
    application_properties.set_manual_property(full_string)

    # Assert
    actual_value = application_properties.property_names
    assert property_value == actual_value


def test_properties_set_manual_property_with_only_format_indicator() -> None:
    """
    Test to make sure that a full key specifying an string format but with no
    format character following is handled properly.
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


def test_properties_set_manual_property_with_string_indicator() -> None:
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


def test_properties_set_manual_property_with_integer_indicator() -> None:
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


def test_properties_set_manual_property_with_integer_indicator_and_bad_integer() -> (
    None
):
    """
    Test to make sure that a full key specifying a bad integer is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    # sourcery skip: inline-variable, remove-unnecessary-cast, simplify-fstring-formatting
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}a"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Manual property value '$#123a' cannot be translated into an integer."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_boolean_indicator() -> None:
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


def test_properties_set_manual_property_with_uncased_boolean_indicator() -> None:
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


def test_properties_set_manual_property_with_multiples() -> None:
    """
    Test to make sure that a list of full keys is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}=$!{property_value}"
    full_string_in_array: List[str] = [full_string]

    # Act
    application_properties.set_manual_property(full_string_in_array)  # type: ignore

    # Assert
    actual_value = application_properties.get_boolean_property(full_property_key)
    assert property_value == actual_value


def test_properties_set_manual_property_with_bad_key_start() -> None:
    """
    Test to make sure that a full key starting with the key separator character is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = ".a"
    # sourcery skip: inline-variable, simplify-fstring-formatting
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key must not start or end with the '.' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_bad_key_end() -> None:
    """
    Test to make sure that a full key ending with the key separator character is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a."
    # sourcery skip: inline-variable, simplify-fstring-formatting
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key must not start or end with the '.' character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_empty_key_middle() -> None:
    """
    Test to make sure that an empty key part for the full key is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a..a"
    # sourcery skip: inline-variable, simplify-fstring-formatting
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Full property key cannot contain multiples of the . without any text between them."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_empty_key() -> None:
    """
    Test to make sure that a key with an empty key part is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = ""
    # sourcery skip: inline-variable, simplify-fstring-formatting
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Each part of the property key must contain at least one character."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_with_whitespace_key() -> None:
    """
    Test to make sure that a key with whitespace is handled properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    full_property_key = "a a"
    # sourcery skip: inline-variable, simplify-fstring-formatting
    property_value = 123
    full_string = f"{full_property_key}=$#{property_value}"

    # Act
    raised_exception = None
    try:
        application_properties.set_manual_property(full_string)
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception)
        == "Each part of the property key cannot contain a whitespace character, a '=' character, or a '.' character."
    ), "Expected message was not present in exception."


def test_properties_verify_manual_property_form_with_non_string() -> None:
    """
    Test to make sure that if we try and test the verification form function
    with a non-string, it fails predictably.
    """

    # Arrange
    full_string = 1

    # Act
    raised_exception = None
    try:
        ApplicationProperties.verify_manual_property_form(full_string)  # type: ignore
        raise AssertionError("Should have raised an exception by now.")
    except ValueError as this_exception:
        raised_exception = this_exception

    # Assert
    assert raised_exception, "Expected exception was not raised."
    assert (
        str(raised_exception) == "Manual property form must be a string."
    ), "Expected message was not present in exception."


def test_properties_set_manual_property_bool_wrong_type_convert_disabled_strict_enabled() -> (
    None
):
    """
    Test to make sure that asking for a boolean with only a string present, strict
    mode on and covert mode off results in an exception.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=True, convert_untyped_if_possible=False
    )
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_error = "The value for property 'a' must be of type 'bool'."

    # Act
    application_properties.set_manual_property(full_string)
    caught_exception = None
    try:
        application_properties.get_boolean_property(
            full_property_key, default_value=False
        )
    except ValueError as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception is not None
    assert str(caught_exception) == expected_error


def test_properties_set_manual_property_bool_wrong_type_convert_disabled_strict_disabled() -> (
    None
):
    """
    Test to make sure that asking for a boolean with only a string present, strict
    mode off and covert mode off results in an exception.  As strict mode is off, the
    default value takes precedence over reporting an error.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=False, convert_untyped_if_possible=False
    )
    full_property_key = "a"
    property_value = True
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = False

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_boolean_property(
        full_property_key, default_value=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_bool_wrong_type_convert_enabled_strict_enabled_with_valid() -> (
    None
):
    """
    Test to make sure that asking for a boolean with only a string present, strict
    mode on and covert mode on with a valid string that can be translated into a boolean.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=True, convert_untyped_if_possible=True
    )
    full_property_key = "a"
    property_value = "True"
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = True

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_boolean_property(
        full_property_key, default_value=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_bool_wrong_type_convert_enabled_strict_enabled_with_invalid() -> (
    None
):
    """
    Test to make sure that asking for a boolean with only a string present, strict
    mode on and covert mode off with an invalid (i.e. non-"true") boolean value. This happens
    because any string that is not "true" (case insensitive) is assumed to be False. As such,
    strict mode is never triggered as it always has a valid value.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=True, convert_untyped_if_possible=True
    )
    full_property_key = "a"
    property_value = "Truex"
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = False

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_boolean_property(
        full_property_key, default_value=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_bool_wrong_type_convert_enabled_strict_disabled_with_valid() -> (
    None
):
    """
    Test to make sure that asking for a boolean with only a string present, strict
    mode off and covert mode on with a valid string that can be translated into a boolean.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=False, convert_untyped_if_possible=True
    )
    full_property_key = "a"
    property_value = "True"
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = True

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_boolean_property(
        full_property_key, default_value=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_bool_wrong_type_convert_enabled_strict_disabled_with_invalid() -> (
    None
):
    """
    Test to make sure that asking for a boolean with only a string present, strict
    mode off and covert mode off with an invalid (i.e. non-"true") boolean value. This happens
    because any string that is not "true" (case insensitive) is assumed to be False. As such,
    strict mode is never triggered as it always has a valid value.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=False, convert_untyped_if_possible=True
    )
    full_property_key = "a"
    property_value = "Truex"
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = False

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_boolean_property(
        full_property_key, default_value=False
    )

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_integer_wrong_type_convert_disabled_strict_enabled() -> (
    None
):
    """
    Test to make sure that asking for a integer with only a string present, strict
    mode on and covert mode off results in an exception.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=True, convert_untyped_if_possible=False
    )
    full_property_key = "a"
    property_value = 123
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_error = "The value for property 'a' must be of type 'int'."

    # Act
    application_properties.set_manual_property(full_string)
    caught_exception = None
    try:
        application_properties.get_integer_property(full_property_key, default_value=-1)
    except ValueError as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception is not None
    assert str(caught_exception) == expected_error


def test_properties_set_manual_property_integer_wrong_type_convert_disabled_strict_disabled() -> (
    None
):
    """
    Test to make sure that asking for a integer with only a string present, strict
    mode off and covert mode off results in an exception.  As strict mode is off, the
    default value takes precedence over reporting an error.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=False, convert_untyped_if_possible=False
    )
    full_property_key = "a"
    property_value = 123
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = -1

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_integer_property(
        full_property_key, default_value=-1
    )

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_integer_wrong_type_convert_enabled_strict_enabled_with_valid() -> (
    None
):
    """
    Test to make sure that asking for a integer with only a string present, strict
    mode on and covert mode on with a valid string that can be translated into an integer.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=True, convert_untyped_if_possible=True
    )
    full_property_key = "a"
    property_value = "123"
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = 123

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_integer_property(
        full_property_key, default_value=-1
    )

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_integer_wrong_type_convert_enabled_strict_enabled_with_invalid() -> (
    None
):
    """
    Test to make sure that asking for a integer with only a string present, strict
    mode on and covert mode off with an invalid integer value.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=True, convert_untyped_if_possible=True
    )
    full_property_key = "a"
    property_value = "123x"
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_error = "The value for property 'a' must be of type 'int'."

    # Act
    application_properties.set_manual_property(full_string)
    caught_exception = None
    try:
        application_properties.get_integer_property(full_property_key, default_value=-1)
    except ValueError as this_exception:
        caught_exception = this_exception

    # Assert
    assert caught_exception is not None
    assert str(caught_exception) == expected_error


def test_properties_set_manual_property_integer_wrong_type_convert_enabled_strict_disabled_with_valid() -> (
    None
):
    """
    Test to make sure that asking for a integer with only a string present, strict
    mode off and covert mode on with a valid string that can be translated into a integer.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=False, convert_untyped_if_possible=True
    )
    full_property_key = "a"
    property_value = "123"
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = 123

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_integer_property(
        full_property_key, default_value=-1
    )

    # Assert
    assert expected_value == actual_value


def test_properties_set_manual_property_integer_wrong_type_convert_enabled_strict_disabled_with_invalid() -> (
    None
):
    """
    Test to make sure that asking for a integer with only a string present, strict
    mode off and covert mode off with an invalid integer value.
    """

    # Arrange
    application_properties = ApplicationProperties(
        strict_mode=False, convert_untyped_if_possible=True
    )
    full_property_key = "a"
    property_value = "123x"
    full_string = f"{full_property_key}={str(property_value).lower()}"

    expected_value = -1

    # Act
    application_properties.set_manual_property(full_string)
    actual_value = application_properties.get_integer_property(
        full_property_key, default_value=-1
    )

    # Assert
    assert expected_value == actual_value
