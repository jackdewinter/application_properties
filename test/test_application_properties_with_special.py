"""
Module to provide tests across the various loaders.
"""

import os
from test.patches.patch_builtin_open import path_builtin_open_with_binary_content
from test.pytest_helpers import ErrorResults, TestHelpers

from application_properties.application_properties import ApplicationProperties
from application_properties.application_properties_json_loader import (
    ApplicationPropertiesJsonLoader,
)
from application_properties.application_properties_toml_loader import (
    ApplicationPropertiesTomlLoader,
)
from application_properties.application_properties_yaml_loader import (
    ApplicationPropertiesYamlLoader,
)
from application_properties.multisource_configuration_loader import (
    MultisourceConfigurationLoader,
)

# pylint: disable=too-many-lines


def test_config_special_toml_loader_key_with_empty() -> None:
    """
    Test to make sure that
    """

    # Arrange
    section_header = None
    supplied_configuration = ""
    results = ErrorResults()

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = False
        expected_value = None
        expected_error = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "lint.per-file-ignores.'my_proj/logger.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert results.reported_error == expected_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_key_with_almost_empty() -> None:
    """
    Test to make sure that
    """

    # Arrange
    section_header = None
    supplied_configuration = """[tool.ruff]
[tool.other_empty_section]
"""
    results = ErrorResults()

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = True
        expected_did_error = False
        expected_value = None
        expected_error = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "lint.per-file-ignores.'my_proj/logger.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert results.reported_error == expected_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_key_with_quoted_separator_with_disabled() -> None:
    """
    Test to make sure that by default we error out when loading a toml file that contains
    a key with a quoted separator. While the TOML format requires periods in keys to be
    quoted the core does not allow it unless specifically enabled.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[tool.ruff]

lint.per-file-ignores."my_proj/logger.py" = "1"
"""
    results = ErrorResults()

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = True
        expected_value = None
        expected_error = f"Specified configuration file '{configuration_file}' contains invalidly formatted data: Key string `my_proj/logger.py` cannot contain a whitespace character, a '=' character, or a '.' character."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "lint.per-file-ignores.'my_proj/logger.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert results.reported_error == expected_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_key_with_quoted_separator_with_enabled() -> None:
    """
    Test to make sure that if configured we properly load a toml file that contains a key
    with a quoted separator. The TOML format requires periods in keys to be quoted and
    in this case, the core specifically allows the separator to be present.
    """

    # Arrange
    section_header = "tool.ruff"
    supplied_configuration = """[tool.ruff]

lint.per-file-ignores."my_proj/logger.py" = "1"
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = True
        expected_did_error = False
        expected_value = "1"
        expected_error = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "lint.per-file-ignores.'my_proj/logger.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_key_with_unquoted_separator_and_slash() -> None:
    """
    Test to make sure that the same data from `test_toml_loader_key_with_quoted_separator`
    without the quotes causes an error, as TOML does not allow unquoted periods and slashes in keys.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[tool.ruff]

lint.per-file-ignores.my_proj/logger.py = "1"
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        expected_did_apply = False
        expected_did_error = True
        expected_error = f"Specified configuration file '{configuration_file}' is not a valid TOML file: Expected '=' after a key in a key/value pair (at line 3, column 30)."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_error == results.reported_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_key_with_unquoted_space() -> None:
    """
    Test to make sure that the same data from `test_toml_loader_key_with_quoted_separator`
    without the quotes causes an error, as TOML does not allow unquoted spaces in keys.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[tool.ruff]

lint.per-file-ignores.my_proj logger = "1"
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        expected_did_apply = False
        expected_did_error = True
        expected_error = f"Specified configuration file '{configuration_file}' is not a valid TOML file: Expected '=' after a key in a key/value pair (at line 3, column 31)."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_error == results.reported_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_key_with_quoted_separator_and_slash_but_not_supported_type_with_disabled() -> (
    None
):
    """
    Test to make sure that by default we error out when loading a toml file that contains
    a key with a quoted separator. While the TOML format requires periods in keys to be
    quoted the core does not allow it unless specifically enabled.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[tool.ruff]

lint.per-file-ignores."my_proj/logger.py" = [
  "ANN001", # No type check of logging functions needed
]
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = True
        expected_value = -1
        expected_error = f"Specified configuration file '{configuration_file}' contains invalidly formatted data: Key string `my_proj/logger.py` cannot contain a whitespace character, a '=' character, or a '.' character."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_integer_property(
            "lint.per-file-ignores.'my_proj/logger.py'", -1
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_key_with_quoted_separator_and_slash_but_not_supported_type_with_enabled() -> (
    None
):
    """
    Test to make sure that we can still load a key with a quoted separator and slash,
    but that the type is not supported for conversion, thus returning the default value.
    """

    # Arrange
    section_header = "tool.ruff"
    supplied_configuration = """[tool.ruff]

lint.per-file-ignores."my_proj/logger.py" = [
  "ANN001", # No type check of logging functions needed
]
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = True
        expected_did_error = False
        expected_value = -1
        expected_error = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_integer_property(
            "lint.per-file-ignores.'my_proj/logger.py'", -1
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_bad_format_with_unquoted_key_with_leading_period() -> (
    None
):
    """
    Test to make sure that a header that starts with a period is an error.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[tool.ruff]

.lint.per-file-ignores.something = "zz"
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = False
        expected_did_error = True
        expected_error = f"Specified configuration file '{configuration_file}' is not a valid TOML file: Invalid statement (at line 3, column 1)."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_error == results.reported_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_bad_format_with_quoted_key_with_leading_period_with_disabled() -> (
    None
):
    """
    Test to make sure that a header that starts with a period is an error.
    """

    # Arrange
    section_header = None
    supplied_configuration = """[tool.ruff]

'.lint'.per-file-ignores.something = "zz"
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = True
        expected_value = None
        expected_error = f"Specified configuration file '{configuration_file}' contains invalidly formatted data: Key string `.lint` cannot contain a whitespace character, a '=' character, or a '.' character."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "'.lint'.per-file-ignores.something"
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_bad_format_with_quoted_key_with_leading_period_with_enabled() -> (
    None
):
    """
    Test to make sure that a header that starts with a period is an error.
    """

    # Arrange
    section_header = "tool.ruff"
    supplied_configuration = """[tool.ruff]

'.lint'.per-file-ignores.something = "zz"
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = True
        expected_did_error = False
        expected_error = None
        expected_value = "zz"

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesTomlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "'.lint'.per-file-ignores.something"
        )

        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_toml_loader_load_toml_implicitly_from_pyproject_with_disabled() -> (
    None
):
    """
    Test to make sure that we can load a toml file from an implied pyproject.toml file.
    """

    # Arrange
    results = ErrorResults()
    __pyproject_section_header = "tool.pymarkdown"
    supplied_configuration = """[tool.pymarkdown]

system.per-file-ignores."my_proj/logger.py" = "ABC"
"""
    pyproject_toml_path = os.path.abspath("pyproject.toml")

    expected_value = None
    expected_error = f"Specified configuration file '{pyproject_toml_path}' contains invalidly formatted data: Key string `my_proj/logger.py` cannot contain a whitespace character, a '=' character, or a '.' character."

    application_properties = ApplicationProperties(allow_separator_in_keys=False)

    # Act
    with path_builtin_open_with_binary_content(
        pyproject_toml_path, supplied_configuration.encode("utf-8")
    ):
        loader = MultisourceConfigurationLoader()
        loader.add_local_pyproject_toml_file(__pyproject_section_header)
        loader.process(application_properties, results.keep_error)

    actual_value = application_properties.get_string_property(
        "system.per-file-ignores.'my_proj/logger.py'", None
    )

    # Assert
    assert expected_value == actual_value
    assert expected_error == results.reported_error


def test_config_special_toml_loader_load_toml_implicitly_from_pyproject_with_enabled() -> (
    None
):
    """
    Test to make sure that we can load a toml file from an implied pyproject.toml file.
    """

    # Arrange
    results = ErrorResults()
    __pyproject_section_header = "tool.pymarkdown"
    supplied_configuration = """[tool.pymarkdown]

system.per-file-ignores."my_proj/logger.py" = "ABC"
"""
    expected_value = "ABC"
    expected_error = None

    pyproject_toml_path = os.path.abspath("pyproject.toml")

    application_properties = ApplicationProperties(allow_separator_in_keys=True)

    # Act
    with path_builtin_open_with_binary_content(
        pyproject_toml_path, supplied_configuration.encode("utf-8")
    ):
        loader = MultisourceConfigurationLoader()
        loader.add_local_pyproject_toml_file(__pyproject_section_header)
        loader.process(application_properties, results.keep_error)

    actual_value = application_properties.get_string_property(
        "system.per-file-ignores.'my_proj/logger.py'", None
    )

    # Assert
    assert expected_value == actual_value
    assert expected_error == results.reported_error


# def test_config_special_yaml_loader_yaml_file_bad_yaml_format_with_header_with_leading_period() -> (
#     None
# ):
#     """
#     Test to make sure that a header that starts with a period is an error.
#     """

#     # Arrange
#     section_header = None
#     supplied_configuration = """.plugins:
#   tools:
#     bar: "fred"
# """
#     results = ErrorResults()
#     expected_did_apply = False
#     expected_did_error = True

#     configuration_file = None
#     try:
#         configuration_file = TestHelpers.write_temporary_configuration(
#             supplied_configuration
#         )
#         application_properties = ApplicationProperties()

#         expected_error = f"Specified configuration file '{configuration_file}' contains invalidly formatted data: Key string `.plugins` cannot contain a whitespace character, a '=' character, or a '.' character."

#         # Act
#         (
#             actual_did_apply,
#             actual_did_error,
#         ) = ApplicationPropertiesYamlLoader.load_and_set(
#             application_properties,
#             configuration_file,
#             section_header,
#             results.keep_error,
#             True,
#             False,
#         )

#         assert expected_did_apply == actual_did_apply
#         assert expected_did_error == actual_did_error
#         assert expected_error == results.reported_error
#     finally:
#         if configuration_file and os.path.exists(configuration_file):
#             os.remove(configuration_file)


# def test_config_special_yaml_loader_yaml_file_bad_yaml_format_with_item_with_leading_period() -> None:
#     """
#     Test to make sure that an item that starts with a period is an error.
#     """

#     # Arrange
#     section_header = None
#     supplied_configuration = """plugins:
#   .tools.bar: "fred"
# """
#     results = ErrorResults()
#     expected_did_apply = False
#     expected_did_error = True

#     configuration_file = None
#     try:
#         configuration_file = TestHelpers.write_temporary_configuration(
#             supplied_configuration
#         )
#         application_properties = ApplicationProperties()

#         # Act
#         (
#             actual_did_apply,
#             actual_did_error,
#         ) = ApplicationPropertiesYamlLoader.load_and_set(
#             application_properties,
#             configuration_file,
#             section_header,
#             results.keep_error,
#             True,
#             False,
#         )

#         assert expected_did_apply == actual_did_apply
#         assert expected_did_error == actual_did_error
#         assert results.reported_error is not None
#         assert (
#             results.reported_error
#             == f"Specified configuration file '{configuration_file}' contains invalidly formatted data: Key strings cannot contain a whitespace character, a '=' character, or a '.' character."
#         )
#     finally:
#         if configuration_file and os.path.exists(configuration_file):
#             os.remove(configuration_file)


def test_config_special_yaml_loader_valid_yaml_empty() -> None:
    """
    Test to make sure that
    """

    # Arrange
    supplied_configuration = ""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = False
        expected_did_error = False
        expected_value = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            None,
            results.keep_error,
            True,
            True,
        )
        actual_value = application_properties.get_integer_property(
            "plugins.'md999.test_value'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_yaml_loader_valid_yaml_almost_empty() -> None:
    """
    Test to make sure that
    """

    # Arrange
    supplied_configuration = """plugins:
tests:
values:
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = True
        expected_did_error = False
        expected_value = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            None,
            results.keep_error,
            True,
            True,
        )
        actual_value = application_properties.get_integer_property(
            "plugins.'md999.test_value'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_yaml_loader_valid_yaml_short_form_key_with_enabled() -> None:
    """
    Test to make sure that we can load a valid yaml file with an "abbreviated" key
    with the separators enabled.  This is because it is read as a single key and
    not split into parts.
    """

    # Arrange
    supplied_configuration = """plugins:
  md999.test_value: 2
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = True
        expected_did_error = False
        expected_value = 2

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            None,
            results.keep_error,
            True,
            True,
        )
        actual_value = application_properties.get_integer_property(
            "plugins.'md999.test_value'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_yaml_loader_valid_yaml_key_with_spaces() -> None:
    """
    Test to make sure that we can load a valid yaml file that contains spaces as parts of the keys.
    This should fail regardless.
    """

    # Arrange
    supplied_configuration = """plugins:
  md999 test_value: 2
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        expected_did_apply = False
        expected_did_error = True
        expected_error = f"Specified configuration file '{configuration_file}' contains invalidly formatted data: Key string `md999 test_value` cannot contain a whitespace character, a '=' character, or a '.' character."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            None,
            results.keep_error,
            True,
            True,
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_error == results.reported_error
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_yaml_loader_key_with_unquoted_wildcard() -> None:
    """
    Test to make sure that we error when loading a yaml file that contains a key with a
    unquoted wildcard. This is because the YAML format will not allow unquoted wildcards
    in keys, causing the parsing error.
    """

    # Arrange
    section_header = None
    supplied_configuration = """system:
  per-line-ignores:
    **/__init__.py : Md001
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties()

        expected_did_apply = False
        expected_did_error = True
        expected_error = f"""Specified configuration file '{configuration_file}' is not a valid YAML file: while scanning an alias
  in "{configuration_file}", line 3, column 5
expected alphabetic or numeric character, but found '*'
  in "{configuration_file}", line 3, column 6."""

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert results.reported_error == expected_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_yaml_loader_key_with_unquoted_separator_with_disabled() -> None:
    """
    Test to make sure that we error when loading a yaml file that contains a key with a
    unquoted separator.

    NOTE: While the file is loaded and the `__init__.py` is parsed properly from the
          YAML file, the key `system.per-line-ignores.'__init__.py'` requires the `'`
          character around that part of the key to ensure that it can fetch the proper
          key's value.
    """

    # Arrange
    section_header = None
    supplied_configuration = """system:
  per-line-ignores:
    __init__.py : Md001
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = True
        expected_value = None
        expected_error = f"Specified configuration file '{configuration_file}' contains invalidly formatted data: Key string `__init__.py` cannot contain a whitespace character, a '=' character, or a '.' character."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_yaml_loader_key_with_unquoted_separator_with_enabled() -> None:
    """
    Test to make sure that we error when loading a yaml file that contains a key with a
    unquoted separator.

    NOTE: While the file is loaded and the `__init__.py` is parsed properly from the
          YAML file, the key `system.per-line-ignores.'__init__.py'` requires the `'`
          character around that part of the key to ensure that it can fetch the proper
          key's value.
    """

    # Arrange
    section_header = None
    supplied_configuration = """system:
  per-line-ignores:
    __init__.py : Md001
"""
    results = ErrorResults()
    expected_did_apply = True
    expected_did_error = False
    expected_value = "Md001"

    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert actual_value == expected_value

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_yaml_loader_key_with_quoted_separator_and_wildcard_disabled() -> (
    None
):
    """
    Test to make sure that we can load a yaml file that contains a key with a quoted
    wildcard and separator.

    NOTE: The file is loaded and the `**/__init__.py` is parsed as a quoted key
          and passed into the application properties map.  Therefore, the key
          `system.per-line-ignores.'**/__init__.py'` with the `'` character around
          that part of the key is required to ensure it fetches the correct value.
    """

    # Arrange
    section_header = None
    supplied_configuration = """system:
  per-line-ignores:
    "**/__init__.py" : Md001
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = True
        expected_value = None
        expected_error = f"Specified configuration file '{configuration_file}' contains invalidly formatted data: Key string `**/__init__.py` cannot contain a whitespace character, a '=' character, or a '.' character."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'**/__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_yaml_loader_key_with_quoted_separator_and_wildcard_enabled() -> (
    None
):
    """
    Test to make sure that we can load a yaml file that contains a key with a quoted
    wildcard and separator.

    NOTE: The file is loaded and the `**/__init__.py` is parsed as a quoted key
          and passed into the application properties map.  Therefore, the key
          `system.per-line-ignores.'**/__init__.py'` with the `'` character around
          that part of the key is required to ensure it fetches the correct value.
    """

    # Arrange
    section_header = None
    supplied_configuration = """system:
  per-line-ignores:
    "**/__init__.py" : Md001
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = True
        expected_did_error = False
        expected_value = "Md001"

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesYamlLoader.load_and_set(
            application_properties,
            configuration_file,
            section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'**/__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_json_loader_valid_json_empty_normal() -> None:
    """
    Test to make sure that
    """

    # Arrange
    supplied_configuration = ""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = False
        expected_value = None
        expected_error = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            configuration_file,
            # section_header,
            results.keep_error,
            True,
            load_as_json5_file=False,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'**/__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_json_loader_valid_json_empty_json5() -> None:
    """
    Test to make sure that
    """

    # Arrange
    supplied_configuration = ""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = False
        expected_value = None
        expected_error = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            configuration_file,
            # section_header,
            results.keep_error,
            True,
            load_as_json5_file=True,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'**/__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_json_loader_valid_json_almost_empty() -> None:
    """
    Test to make sure that
    """

    # Arrange
    supplied_configuration = """{ "system" : { }}"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = True
        expected_did_error = False
        expected_value = None
        expected_error = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            configuration_file,
            # section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'**/__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_json_loader_key_with_quoted_separator_and_wildcard_disabled() -> (
    None
):
    """
    Test to make sure that we can load a yaml file that contains a key with a quoted
    wildcard and separator.
    """

    # Arrange
    supplied_configuration = (
        """{ "system" : { "per-line-ignores" : { "**/__init__.py" : "Md001" }}}"""
    )
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=False)

        expected_did_apply = False
        expected_did_error = True
        expected_value = None
        expected_error = f"Specified configuration file '{configuration_file}' is not valid: Key string `**/__init__.py` cannot contain a whitespace character, a '=' character, or a '.' character."

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            configuration_file,
            # section_header,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'**/__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


def test_config_special_json_loader_key_with_quoted_separator_and_wildcard_enabled() -> (
    None
):
    """
    Test to make sure that we can load a yaml file that contains a key with a quoted
    wildcard and separator.
    """

    # Arrange
    supplied_configuration = """{ "system" : { "per-line-ignores" : { "**/__init__.py" : "Md001" }}}
"""
    results = ErrorResults()
    configuration_file = None
    try:
        configuration_file = TestHelpers.write_temporary_configuration(
            supplied_configuration
        )
        application_properties = ApplicationProperties(allow_separator_in_keys=True)

        expected_did_apply = True
        expected_did_error = False
        expected_value = "Md001"
        expected_error = None

        # Act
        (
            actual_did_apply,
            actual_did_error,
        ) = ApplicationPropertiesJsonLoader.load_and_set(
            application_properties,
            configuration_file,
            results.keep_error,
            True,
            False,
        )
        actual_value = application_properties.get_string_property(
            "system.per-line-ignores.'**/__init__.py'"
        )

        # Assert
        assert expected_did_apply == actual_did_apply
        assert expected_did_error == actual_did_error
        assert expected_value == actual_value
        assert expected_error == results.reported_error

    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
