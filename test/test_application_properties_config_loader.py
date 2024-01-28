"""
Tests for the ApplicationProperties class
"""

import io
import os
import sys
from test.pytest_helpers import ErrorResults, TestHelpers

from application_properties import ApplicationProperties
from application_properties.application_properties_config_loader import (
    ApplicationPropertiesConfigLoader,
)


def test_config_loader_config_not_present_check_enabled() -> None:
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
    actual_did_apply, actual_did_error = ApplicationPropertiesConfigLoader.load_and_set(
        application_properties, configuration_file, None, None, True, True
    )
    actual_value = application_properties.get_integer_property(
        "plugins.md999.test_value", -1
    )

    # Assert
    assert expected_value == actual_value
    assert expected_did_apply == actual_did_apply
    assert expected_did_error == actual_did_error


def test_config_loader_config_not_present_check_disabled() -> None:
    """
    Test to make sure that we do not try and load a configuration file that is not present.
    """

    # Arrange
    configuration_file = "does-not-exist"
    configuration_file = os.path.abspath(configuration_file)
    assert not os.path.exists(configuration_file)
    application_properties = ApplicationProperties()

    expected_did_apply = False
    expected_did_error = True
    expected_value = -1

    # Act
    actual_did_apply, actual_did_error = ApplicationPropertiesConfigLoader.load_and_set(
        application_properties, configuration_file, None, None, True, False
    )
    actual_value = application_properties.get_integer_property(
        "plugins.md999.test_value", -1
    )

    # Assert
    assert expected_value == actual_value
    assert expected_did_apply == actual_did_apply
    assert expected_did_error == actual_did_error


def test_config_loader_valid_config() -> None:
    """
    Test to make sure that we can load a valid config file.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    expected_value = "2"
    expected_did_apply = True
    expected_did_error = False

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()
        with open(configuration_file, "r", encoding="utf-8") as file:
            settings = file.read()
            print(settings)

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesConfigLoader.load_and_set(
            application_properties, configuration_file, None, None, True, True
        )
        actual_value = application_properties.get_string_property(
            "plugins.md999.test_value", "bob"
        )

        # Assert
        assert expected_value == actual_value
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_valid_config_but_wrong_get_property_type() -> None:
    """
    Test to make sure that we can load a valid config file, even if the property
    we are looking for is of the wrong type.  The load should succeed, even
    if the get fails.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    expected_error = (
        "The value for property 'plugins.md999.test_value' must be of type 'int'."
    )

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        # Act
        captured_exception = None
        ApplicationPropertiesConfigLoader.load_and_set(
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


def test_config_loader_config_file_not_present_with_check() -> None:
    """
    Test to make sure that we cannot load a config file that is not there,
    and explicitly have something in place to check for that.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    expected_did_apply = False
    expected_did_error = False

    configuration_file = TestHelpers.write_temporary_configuration(
        supplied_configuration
    )
    os.remove(configuration_file)
    application_properties = ApplicationProperties()

    # Act
    actual_did_apply, actual_did_error = ApplicationPropertiesConfigLoader.load_and_set(
        application_properties, configuration_file, None, None, True, True
    )

    # Assert
    assert expected_did_apply == actual_did_apply
    assert expected_did_error == actual_did_error


def test_config_loader_config_file_not_present_without_check() -> None:
    """
    Test to make sure that we cannot load a config file that is not there,
    and explicitly do not have something in place to check for that.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    expected_did_apply = False
    expected_did_error = True

    configuration_file = TestHelpers.write_temporary_configuration(
        supplied_configuration
    )
    os.remove(configuration_file)
    application_properties = ApplicationProperties()

    # Act
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    std_output = io.StringIO()
    std_error = io.StringIO()
    try:
        sys.stdout = std_output
        sys.stderr = std_error
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesConfigLoader.load_and_set(
            application_properties, configuration_file, None, None, True, False
        )
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    # Assert
    assert expected_did_apply == actual_did_apply
    assert expected_did_error == actual_did_error
    assert (
        std_output.getvalue()
        == f"Specified configuration file '{configuration_file}' does not exist.\n"
    )
    assert std_error.getvalue() == ""


def test_config_loader_config_file_not_present_without_check_and_error_function() -> (
    None
):
    """
    Test to make sure that we cannot load a config file that is not there,
    and explicitly do not have something in place to check for that, but have
    all errors getting captured.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value = 2
"""
    results = ErrorResults()
    expected_did_apply = False
    expected_did_error = True

    configuration_file = TestHelpers.write_temporary_configuration(
        supplied_configuration
    )
    os.remove(configuration_file)
    application_properties = ApplicationProperties()

    # Act
    actual_did_apply, actual_did_error = ApplicationPropertiesConfigLoader.load_and_set(
        application_properties,
        configuration_file,
        None,
        results.keep_error,
        True,
        False,
    )

    # Assert
    assert expected_did_apply == actual_did_apply
    assert expected_did_error == actual_did_error
    assert results.reported_error is not None
    assert (
        results.reported_error
        == f"Specified configuration file '{configuration_file}' does not exist."
    )


def test_config_loader_config_file_not_valid() -> None:
    """
    Test to make sure that we error loading an invalid config file.
    """

    # Arrange
    supplied_configuration = """[plugins]
md999.test_value
"""
    expected_did_apply = False
    expected_did_error = True

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        # Act
        old_stdout = sys.stdout
        std_output = io.StringIO()
        try:
            sys.stdout = std_output
            (
                actual_did_apply,
                actual_did_error,
            ) = ApplicationPropertiesConfigLoader.load_and_set(
                application_properties, configuration_file, None, None, True, False
            )
        finally:
            sys.stdout = old_stdout

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert std_output.getvalue() is not None
        configuration_file2 = configuration_file.replace("\\", "\\\\")
        assert std_output.getvalue() == (
            f"Specified configuration file '{configuration_file}' is not a valid config file: Source contains parsing errors: '{configuration_file2}'\n\t[line  2]: 'md999.test_value\\n'.\n"
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_valid_with_no_section_header() -> None:
    """
    Test to make sure that not having a section header implies that everything in the
    file is part of the configuration.
    """

    # Arrange
    supplied_configuration = """[plugins]
tools.bar = fred
"""
    expected_did_apply = True
    expected_did_error = False
    expected_value = "fred"

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
            application_properties, configuration_file, None, None, False, False
        )
        actual_value = application_properties.get_string_property(
            "plugins.tools.bar", None, None
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_valid_with_one_word_section_header() -> None:
    """
    Test to make sure that having a having a one word section header that is
    present in the config file allows for anything under that entry to be
    processed as configuration.
    """

    # Arrange
    section_header = "plugins"
    supplied_configuration = """[plugins]
tools.bar = fred

[other-plugins]
tools.foo = fred
"""
    expected_did_apply = True
    expected_did_error = False
    expected_value = "fred"
    other_expected_value = None

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
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
        other_actual_value = application_properties.get_string_property(
            "tools.foo", None, None
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert other_expected_value == other_actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_valid_with_one_word_bad_section_header() -> None:
    """
    Test to make sure that having a one word section header that is not
    present in the config file effectively does not contribute to the
    configuration.
    """

    # Arrange
    section_header = "not-plugins"
    supplied_configuration = """[plugins]
tools.bar = fred
"""
    expected_did_apply = False
    expected_did_error = False
    expected_value = None

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
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
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_valid_with_multi_word_valid_section_header() -> None:
    """
    Test to make sure that having a having a multi word section header that points to
    an existing section is recognized.
    """

    # Arrange
    section_header = "tools.mytool"
    supplied_configuration = """[tools.mytool]
tools.bar = fred
"""
    expected_did_apply = True
    expected_did_error = False
    expected_value = "fred"

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
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
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_bad_config_format_with_repeated_section() -> None:
    """
    Test to make sure that a repeated section, in different forms, causes errors.
    """

    # Arrange
    section_header = "plugins.tools.bar"
    supplied_configuration = """[plugins.tools]
bar = fred

[plugins.tools]
bar = barney
"""
    results = ErrorResults()
    expected_did_apply = False
    expected_did_error = True

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        configuration_file2 = configuration_file.replace("\\", "\\\\")
        assert results.reported_error is not None
        assert (
            results.reported_error
            == f"Specified configuration file '{configuration_file}' is not a valid config file: While reading from '{configuration_file2}' [line  4]: section 'plugins.tools' already exists."
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_bad_config_format_with_header_with_leading_period() -> (
    None
):
    """
    Test to make sure that a header that starts with a period is an error.
    """

    # Arrange
    section_header = "plugins.tools.bar"
    supplied_configuration = """[.plugins]
tools.bar = "fred"
"""
    results = ErrorResults()
    expected_did_apply = False
    expected_did_error = True

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert results.reported_error is not None
        assert (
            results.reported_error
            == f"Configuration section name '.plugins' in file '{configuration_file}' is not a valid section name: Configuration section name must not start or end with the '.' character."
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_bad_config_format_with_item_with_leading_period() -> (
    None
):
    """
    Test to make sure that an item that starts with a period is an error.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[plugins]
.tools.bar = fred
"""
    results = ErrorResults()
    expected_did_apply = False
    expected_did_error = True

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert results.reported_error is not None
        assert (
            results.reported_error
            == f"Configuration item name '.tools.bar' in file '{configuration_file}' is not a valid section name: Configuration item name must not start or end with the '.' character."
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_bad_config_format_with_double_items_through_different_paths() -> (
    None
):
    """
    Test to make sure that an item name that is doubled, but through different paths, is caught.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[plugins]
tools.bar = fred

[plugins.tools]
bar = fred
"""
    results = ErrorResults()
    expected_did_apply = False
    expected_did_error = True

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert results.reported_error is not None
        assert (
            results.reported_error
            == f"Full configuration item name 'plugins.tools.bar' in file '{configuration_file}' occurs multiple times using different formats."
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_loader_config_file_bad_config_format_with_no_item_value() -> None:
    """
    Test to make sure that an item name that is followed by a separator, but not value, is handled.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[plugins]
tools.bar =\a\a\a\a
""".replace(
        "\a", " "
    )
    results = ErrorResults()
    expected_did_apply = False
    expected_did_error = True

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
        ) = ApplicationPropertiesConfigLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert results.reported_error is not None
        assert (
            results.reported_error
            == f"Full configuration item name 'plugins.tools.bar' in file '{configuration_file}' does not have a value assigned to it."
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
