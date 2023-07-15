"""
Tests for the ApplicationProperties class
"""

import argparse
import json
import os
import sys
import tempfile
from test.pytest_helpers import TestHelpers
from typing import List, Optional

from tomli import TOMLDecodeError

from application_properties import ApplicationProperties
from application_properties.application_properties_utilities import (
    ApplicationPropertiesUtilities,
)


def test_utilities_pyproject_config_absent() -> None:
    """
    Test to make sure that the absence of the pyproject.toml file does not change things.
    """

    # Arrange
    application_properties = ApplicationProperties()
    previous_properties = application_properties.property_names

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        python_config_file_path = os.path.join(tmp_dir_path, "pyproject.toml")
        assert not os.path.exists(python_config_file_path)

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            ApplicationPropertiesUtilities.process_standard_python_configuration_files(
                application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert not captured_error_text
    assert not captured_error_exception
    current_properties = application_properties.property_names
    assert previous_properties == current_properties


def test_utilities_pyproject_config_present() -> None:
    """
    Test to make sure that the presence of the pyproject.toml file is processed properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    expected_properties = ["log.file"]

    supplied_configuration = """
[tool.pymarkdown]
log.file = 2
"""

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        python_config_file_path = os.path.join(tmp_dir_path, "pyproject.toml")
        TestHelpers.write_temporary_configuration(
            supplied_configuration, python_config_file_path
        )
        assert os.path.exists(python_config_file_path)

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            ApplicationPropertiesUtilities.process_standard_python_configuration_files(
                application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert not captured_error_text
    assert not captured_error_exception
    assert expected_properties == application_properties.property_names


def test_utilities_pyproject_config_error() -> None:
    """
    Test to make sure that the presence of the pyproject.toml file with any errors is reported properly.
    """

    # Arrange
    application_properties = ApplicationProperties()
    supplied_configuration = """[plugins]
.tools.bar = "fred"
"""

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        python_config_file_path = os.path.join(tmp_dir_path, "pyproject.toml")
        TestHelpers.write_temporary_configuration(
            supplied_configuration, python_config_file_path
        )
        assert os.path.exists(python_config_file_path)

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            ApplicationPropertiesUtilities.process_standard_python_configuration_files(
                application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    if sys.platform == "darwin":
        assert captured_error_text.startswith("Specified configuration file '")
        assert captured_error_text.endswith(
            "' is not a valid TOML file: Invalid statement (at line 2, column 1)."
        )
    else:
        assert (
            captured_error_text
            == f"Specified configuration file '{python_config_file_path}' is not a valid TOML file: Invalid statement (at line 2, column 1)."
        )
    assert isinstance(captured_error_exception, TOMLDecodeError)
    assert str(captured_error_exception) == "Invalid statement (at line 2, column 1)"


def test_utilities_command_none() -> None:
    """
    Test to make sure that we can handle no command line arguments or default files.
    """

    # Arrange
    application_properties = ApplicationProperties()
    direct_args: List[str] = []
    default_file_name = "my_config.json"
    expected_properties: List[str] = []

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        python_config_file_path = os.path.join(tmp_dir_path, default_file_name)
        assert not os.path.exists(python_config_file_path)

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            parser = argparse.ArgumentParser()
            ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
            parse_arguments = parser.parse_args(args=direct_args)
            ApplicationPropertiesUtilities.process_project_specific_json_configuration(
                default_file_name, parse_arguments, application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert not captured_error_text
    assert not captured_error_exception
    assert expected_properties == application_properties.property_names


def test_utilities_command_default_only() -> None:
    """
    Test to make sure that we can handle parsing only having a default configuration present.
    """

    # Arrange
    application_properties = ApplicationProperties()
    direct_args: List[str] = []
    default_file_name = "my_config.json"
    default_configuration = {"plugins": {"md999": {"test_value": 2}}}
    expected_properties = ["plugins.md999.test_value"]

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        python_config_file_path = TestHelpers.write_temporary_configuration(
            default_configuration, default_file_name, tmp_dir_path
        )
        assert os.path.exists(python_config_file_path)

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            parser = argparse.ArgumentParser()
            ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
            parse_arguments = parser.parse_args(args=direct_args)
            ApplicationPropertiesUtilities.process_project_specific_json_configuration(
                default_file_name, parse_arguments, application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert not captured_error_text
    assert not captured_error_exception
    assert expected_properties == application_properties.property_names


def test_utilities_command_default_only_with_error() -> None:
    """
    Test to make sure that we can handle parsing only having an error-filled default configuration present.
    """

    # Arrange
    application_properties = ApplicationProperties()
    direct_args: List[str] = []
    default_file_name = "my_config.json"
    default_configuration = "I am not a JSON file."

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        python_config_file_path = TestHelpers.write_temporary_configuration(
            default_configuration, default_file_name, tmp_dir_path
        )
        assert os.path.exists(python_config_file_path)

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            parser = argparse.ArgumentParser()
            ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
            parse_arguments = parser.parse_args(args=direct_args)
            ApplicationPropertiesUtilities.process_project_specific_json_configuration(
                default_file_name, parse_arguments, application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    if sys.platform == "darwin":
        assert captured_error_text.startswith("Specified configuration file '")
        assert captured_error_text.endswith(
            "' is not a valid JSON file: Expecting value: line 1 column 1 (char 0)."
        )
    else:
        assert (
            captured_error_text
            == f"Specified configuration file '{python_config_file_path}' is not a valid JSON file: Expecting value: line 1 column 1 (char 0)."
        )
    assert isinstance(captured_error_exception, json.decoder.JSONDecodeError)
    assert str(captured_error_exception) == "Expecting value: line 1 column 1 (char 0)"


def test_utilities_command_specified_only() -> None:
    """
    Test to make sure that we can handle parsing only having a specified configuration present.
    """

    # Arrange
    application_properties = ApplicationProperties()
    default_file_name = "my_config.json"
    specified_file_name = "local_config.json"
    specified_configuration = {"plugins": {"md999": {"test_value": 2}}}
    expected_properties = ["plugins.md999.test_value"]
    direct_args = ["--config", specified_file_name]

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        python_config_file_path = TestHelpers.write_temporary_configuration(
            specified_configuration, specified_file_name, tmp_dir_path
        )
        assert os.path.exists(python_config_file_path)

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            parser = argparse.ArgumentParser()
            ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
            parse_arguments = parser.parse_args(args=direct_args)
            ApplicationPropertiesUtilities.process_project_specific_json_configuration(
                default_file_name, parse_arguments, application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert not captured_error_text
    assert not captured_error_exception
    assert expected_properties == application_properties.property_names


def test_utilities_command_specified_only_with_error() -> None:
    """
    Test to make sure that we can handle parsing only having a specified configuration present, though with errors.
    """

    # Arrange
    application_properties = ApplicationProperties()
    default_file_name = "my_config.json"
    specified_file_name = "local_config.json"
    specified_configuration = "I am not a JSON file."
    direct_args = ["--config", specified_file_name]

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        python_config_file_path = TestHelpers.write_temporary_configuration(
            specified_configuration, specified_file_name, tmp_dir_path
        )
        assert os.path.exists(python_config_file_path)

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            parser = argparse.ArgumentParser()
            ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
            parse_arguments = parser.parse_args(args=direct_args)
            ApplicationPropertiesUtilities.process_project_specific_json_configuration(
                default_file_name, parse_arguments, application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert (
        captured_error_text
        == f"Specified configuration file '{specified_file_name}' is not a valid JSON file: Expecting value: line 1 column 1 (char 0)."
    )
    assert isinstance(captured_error_exception, json.decoder.JSONDecodeError)
    assert str(captured_error_exception) == "Expecting value: line 1 column 1 (char 0)"


def test_utilities_command_manual_only() -> None:
    """
    Test to make sure that we can handle parsing only having a manual config provided.
    """

    # Arrange
    application_properties = ApplicationProperties()
    default_file_name = "my_config.json"
    expected_properties = ["plugins.md999.test_value"]
    direct_args = ["--set", "plugins.md999.test_value=1"]

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            parser = argparse.ArgumentParser()
            ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
            parse_arguments = parser.parse_args(args=direct_args)
            ApplicationPropertiesUtilities.process_project_specific_json_configuration(
                default_file_name, parse_arguments, application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert not captured_error_text
    assert not captured_error_exception
    assert expected_properties == application_properties.property_names


def test_utilities_command_default_and_specified() -> None:
    """
    Test to make sure that we can handle parsing both a default configuration and a specified configuration present,
    with the proper setting.
    """

    # Arrange
    application_properties = ApplicationProperties()
    default_file_name = "my_config.json"
    specified_file_name = "local_config.json"
    default_configuration = {"plugins": {"md999": {"test_value": 2, "test_one": "1"}}}
    specified_configuration = {"plugins": {"md999": {"test_value": 3, "test_two": "1"}}}
    expected_properties = [
        "plugins.md999.test_value",
        "plugins.md999.test_one",
        "plugins.md999.test_two",
    ]
    direct_args = ["--config", specified_file_name]

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        TestHelpers.write_temporary_configuration(
            default_configuration, default_file_name, tmp_dir_path
        )
        TestHelpers.write_temporary_configuration(
            specified_configuration, specified_file_name, tmp_dir_path
        )

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            parser = argparse.ArgumentParser()
            ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
            parse_arguments = parser.parse_args(args=direct_args)
            ApplicationPropertiesUtilities.process_project_specific_json_configuration(
                default_file_name, parse_arguments, application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert not captured_error_text
    assert not captured_error_exception
    assert expected_properties == application_properties.property_names
    assert application_properties.get_integer_property("plugins.md999.test_value") == 3
    assert application_properties.get_string_property("plugins.md999.test_one") == "1"
    assert application_properties.get_string_property("plugins.md999.test_two") == "1"


def test_utilities_command_default_and_manual() -> None:
    """
    Test to make sure that we can handle parsing both a default configuration and a specified configuration present,
    with the proper setting.
    """

    # Arrange
    application_properties = ApplicationProperties()
    default_file_name = "my_config.json"
    default_configuration = {"plugins": {"md999": {"test_value": 2, "test_one": "1"}}}
    expected_properties = [
        "plugins.md999.test_value",
        "plugins.md999.test_one",
        "plugins.md999.test_two",
    ]
    direct_args = [
        "--set",
        "plugins.md999.test_value=$#1",
        "--set",
        "plugins.md999.test_two=2",
    ]

    captured_error_text = None
    captured_error_exception = None

    def handle_error(error_text: str, error_exception: Optional[Exception]) -> None:
        nonlocal captured_error_text
        nonlocal captured_error_exception
        captured_error_text = error_text
        captured_error_exception = error_exception

    with tempfile.TemporaryDirectory() as tmp_dir_path:
        TestHelpers.write_temporary_configuration(
            default_configuration, default_file_name, tmp_dir_path
        )

        # Act
        old_dir = os.getcwd()
        try:
            os.chdir(tmp_dir_path)

            parser = argparse.ArgumentParser()
            ApplicationPropertiesUtilities.add_default_command_line_arguments(parser)
            parse_arguments = parser.parse_args(args=direct_args)
            ApplicationPropertiesUtilities.process_project_specific_json_configuration(
                default_file_name, parse_arguments, application_properties, handle_error
            )
        finally:
            os.chdir(old_dir)

    # Assert
    assert not captured_error_text
    assert not captured_error_exception
    assert expected_properties == application_properties.property_names
    assert application_properties.get_integer_property("plugins.md999.test_value") == 1
    assert application_properties.get_string_property("plugins.md999.test_one") == "1"
