"""
Tests for the ApplicationProperties class
"""
import io
import json
import os
import sys
import tempfile

from application_properties import ApplicationProperties
from application_properties.application_properties_toml_loader import (
    ApplicationPropertiesTomlLoader,
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


def test_toml_loader_valid_toml():
    """
    Test to make sure that we can load a valid toml file.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    expected_value = 2
    expected_did_apply = True

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties, configuration_file, None, None, True, True
        )
        actual_value = application_properties.get_integer_property(
            "plugins.md999.test_value", -1
        )

        # Assert
        assert expected_value == actual_value
        assert expected_did_apply == actual_did_apply
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_valid_toml_but_wrong_get_property_type():
    """
    Test to make sure that we can load a valid toml file, even if the property
    we are looking for is of the wrong type.  The load should succeed, even
    if the get fails.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = "2"
"""
    expected_error = (
        "The value for property 'plugins.md999.test_value' must be of type 'int'."
    )

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        captured_exception = None
        ApplicationPropertiesTomlLoader.load_and_set(
            application_properties, configuration_file
        )
        try:
            application_properties.get_integer_property(
                "plugins.md999.test_value", -1, None, strict_mode=True
            )
        except ValueError as this_exception:
            captured_exception = this_exception

        # Assert
        assert not application_properties.convert_untyped_if_possible
        assert captured_exception is not None
        assert str(captured_exception) == expected_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_valid_toml_but_wrong_get_property_type_with_untyped_conversion():
    """
    Test to make sure that we can load a valid toml file, even if the property
    we are looking for is of the wrong type.  The load should succeed, even
    if the get fails.  The get should still fail as TOML is a typed source.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = "2"
"""
    expected_error = (
        "The value for property 'plugins.md999.test_value' must be of type 'int'."
    )

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()
        application_properties.enable_convert_untyped_if_possible()

        # Act
        captured_exception = None
        ApplicationPropertiesTomlLoader.load_and_set(
            application_properties, configuration_file
        )
        try:
            application_properties.get_integer_property(
                "plugins.md999.test_value", -1, None, strict_mode=True
            )
        except ValueError as this_exception:
            captured_exception = this_exception

        # Assert
        assert application_properties.convert_untyped_if_possible
        assert captured_exception is not None
        assert str(captured_exception) == expected_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_not_present_with_check():
    """
    Test to make sure that we cannot load a toml file that is not there,
    and explicitly have something in place to check for that.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    expected_did_apply = False

    configuration_file = write_temporary_configuration(supplied_configuration)
    os.remove(configuration_file)
    application_properties = ApplicationProperties()

    # Act
    actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
        application_properties, configuration_file, None, None, True, True
    )

    # Assert
    assert expected_did_apply == actual_did_apply


def test_toml_loader_toml_file_not_present_without_check():
    """
    Test to make sure that we cannot load a toml file that is not there,
    and explicitly do not have something in place to check for that.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    expected_did_apply = False

    configuration_file = write_temporary_configuration(supplied_configuration)
    os.remove(configuration_file)
    application_properties = ApplicationProperties()

    # Act
    old_stdout = sys.stdout
    std_output = io.StringIO()
    try:
        sys.stdout = std_output
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties, configuration_file, None, None, True, False
        )
    finally:
        sys.stdout = old_stdout

    # Assert
    assert expected_did_apply == actual_did_apply
    assert std_output is not None
    assert std_output.getvalue() is not None
    assert std_output.getvalue().startswith(
        f"Specified configuration file '{configuration_file}' was not loaded: "
    )


def test_toml_loader_toml_file_not_present_without_check_and_error_function():
    """
    Test to make sure that we cannot load a toml file that is not there,
    and explicitly do not have something in place to check for that, but have
    all errors getting captured.
    """

    # pylint: disable=too-few-public-methods
    class ErrorResults:
        """
        Class to collect the error results.
        """

        reported_error = None

        @staticmethod
        def keep_error(formatted_error: str, thrown_exception: Exception) -> None:
            """
            Deal with the error by keeping a record of it to compare.
            """
            _ = thrown_exception
            ErrorResults.reported_error = formatted_error

    # pylint: enable=too-few-public-methods

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    expected_did_apply = False

    configuration_file = write_temporary_configuration(supplied_configuration)
    os.remove(configuration_file)
    application_properties = ApplicationProperties()

    # Act
    actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
        application_properties,
        configuration_file,
        None,
        ErrorResults.keep_error,
        True,
        False,
    )

    # Assert
    assert expected_did_apply == actual_did_apply
    assert ErrorResults.reported_error is not None
    assert ErrorResults.reported_error.startswith(
        f"Specified configuration file '{configuration_file}' was not loaded: "
    )


def test_toml_loader_toml_file_not_valid():
    """
    Test to make sure that we error loading an invalid toml file.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value
"""
    expected_did_apply = False

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        old_stdout = sys.stdout
        std_output = io.StringIO()
        try:
            sys.stdout = std_output
            actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
                application_properties, configuration_file, None, None, True, False
            )
        finally:
            sys.stdout = old_stdout

        assert expected_did_apply == actual_did_apply
        assert std_output is not None
        assert std_output.getvalue() is not None
        assert std_output.getvalue().startswith(
            f"Specified configuration file '{configuration_file}' is not a valid TOML file: Expected '=' after a key in a key/value pair (at line 2, column 17).\n"
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_valid_with_no_section_header():
    """
    Test to make sure that not having a section header implies that everything in the
    file is part of the configuration.
    """

    # Arrange
    supplied_configuration = """[plugins]
tools.bar = "fred"
"""
    expected_did_apply = True
    expected_value = "fred"

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties, configuration_file, None, None, True, False
        )
        actual_value = application_properties.get_string_property(
            "plugins.tools.bar", None, None
        )

        assert expected_did_apply == actual_did_apply
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_valid_with_one_word_section_header():
    """
    Test to make sure that having a having a one word section header that is
    present in the TOML file allows for anything under that entry to be
    processed as configuration.
    """

    # Arrange
    section_header = "plugins"
    supplied_configuration = """[plugins]
tools.bar = "fred"
"""
    expected_did_apply = True
    expected_value = "fred"

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            None,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "tools.bar", None, None
        )

        assert expected_did_apply == actual_did_apply
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_valid_with_one_word_bad_section_header():
    """
    Test to make sure that having a one word section header that is not
    present in the TOML file effectively does not contribute to the
    configuration.
    """

    # Arrange
    section_header = "not-plugins"
    supplied_configuration = """[plugins]
tools.bar = "fred"
"""
    expected_did_apply = False
    expected_value = None

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            None,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "tools.bar", None, None
        )

        assert expected_did_apply == actual_did_apply
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_valid_with_multi_word_valid_section_header():
    """
    Test to make sure that having a having a multi word section header that points to
    an existing section is recognized.
    """

    # Arrange
    section_header = "tools.mytool"
    supplied_configuration = """[tools.mytool]
tools.bar = "fred"
"""
    expected_did_apply = True
    expected_value = "fred"

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            None,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "tools.bar", None, None
        )

        assert expected_did_apply == actual_did_apply
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_valid_with_multi_word_section_header_that_points_to_a_value():
    """
    Test to make sure that having a having a multi word section header that points
    to a specific value instead of a section does not get applied.
    """

    # Arrange
    section_header = "plugins.tools.bar"
    supplied_configuration = """[plugins]
tools.bar = "fred"
"""
    expected_did_apply = False
    expected_value = None

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            None,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "tools.bar", None, None
        )

        assert expected_did_apply == actual_did_apply
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_bad_toml_format_with_repeated_section():
    """
    Test to make sure that a repeated section, in different forms, causes errors.
    """

    # pylint: disable=too-few-public-methods
    class ErrorResults:
        """
        Class to collect the error results.
        """

        reported_error = None

        @staticmethod
        def keep_error(formatted_error: str, thrown_exception: Exception) -> None:
            """
            Deal with the error by keeping a record of it to compare.
            """
            _ = thrown_exception
            ErrorResults.reported_error = formatted_error

    # pylint: enable=too-few-public-methods

    # Arrange
    section_header = "plugins.tools.bar"
    supplied_configuration = """[plugins]
tools.bar = "fred"

[plugins.tools]
bar = "barney"
"""
    expected_did_apply = False

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            ErrorResults.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert (
            ErrorResults.reported_error
            == f"Specified configuration file '{configuration_file}' is not a valid TOML file: Cannot declare ('plugins', 'tools') twice (at line 4, column 15)."
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_bad_toml_format_with_header_with_leading_period():
    """
    Test to make sure that a header that starts with a period is an error.
    """

    # pylint: disable=too-few-public-methods
    class ErrorResults:
        """
        Class to collect the error results.
        """

        reported_error = None

        @staticmethod
        def keep_error(formatted_error: str, thrown_exception: Exception) -> None:
            """
            Deal with the error by keeping a record of it to compare.
            """
            _ = thrown_exception
            ErrorResults.reported_error = formatted_error

    # pylint: enable=too-few-public-methods

    # Arrange
    section_header = "plugins.tools.bar"
    supplied_configuration = """[.plugins]
tools.bar = "fred"
"""
    expected_did_apply = False

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            ErrorResults.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert (
            ErrorResults.reported_error
            == f"Specified configuration file '{configuration_file}' is not a valid TOML file: Invalid initial character for a key part (at line 1, column 2)."
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_toml_loader_toml_file_bad_toml_format_with_item_with_leading_period():
    """
    Test to make sure that an item that starts with a period is an error.
    """

    # pylint: disable=too-few-public-methods
    class ErrorResults:
        """
        Class to collect the error results.
        """

        reported_error = None

        @staticmethod
        def keep_error(formatted_error: str, thrown_exception: Exception) -> None:
            """
            Deal with the error by keeping a record of it to compare.
            """
            _ = thrown_exception
            ErrorResults.reported_error = formatted_error

    # pylint: enable=too-few-public-methods

    # Arrange
    section_header = "plugins.tools.bar"
    supplied_configuration = """[plugins]
.tools.bar = "fred"
"""
    expected_did_apply = False

    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        application_properties = ApplicationProperties()

        # Act
        actual_did_apply = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            ErrorResults.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert (
            ErrorResults.reported_error
            == f"Specified configuration file '{configuration_file}' is not a valid TOML file: Invalid statement (at line 2, column 1)."
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
