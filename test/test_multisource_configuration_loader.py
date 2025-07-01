"""
Moduole for tests of the multisource configuration loader.  

NOTE:   These tests are for the configuration loader, not to test the correctness of any
        of the individual loaders themselves.
"""

import os
from test.pytest_helpers import ErrorResults, TestHelpers
from typing import cast

from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import (
    BaseConfigurationSource,
    ConfigurationFileType,
    LocalProjectConfigurationFile,
    LocalPyprojectTomlFile,
    ManuallySetProperties,
    MultisourceConfigurationLoader,
    MultisourceConfigurationLoaderOptions,
    SpecifiedConfigurationFile,
)

# pylint: disable=too-many-lines


def test_multisource_raw_project_toml_does_not_exist() -> None:
    """
    Test that the LocalPyprojectTomlFile class handles a pyproject.toml file that is not there.
    """

    # Arrange
    pyproject_loader = LocalPyprojectTomlFile("tool.utility")
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath("pyproject.toml")
        assert not os.path.isfile(project_configuration_file)

        # Act
        did_apply, did_error = pyproject_loader.apply_configuration(
            options, application_properties, results.keep_error
        )

    # Assert
    assert not did_apply
    assert not did_error
    assert len(application_properties.property_names) == 0


def test_multisource_raw_project_toml_exists() -> None:
    """
    Test that the LocalPyprojectTomlFile class handles a pyproject.toml file with a valid section.
    """

    # Arrange
    pyproject_loader = LocalPyprojectTomlFile("tool.utility")
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    supplied_configuration = """[tool.utility]
some.thing = 1
"""

    with TestHelpers.change_to_temporary_directory():
        TestHelpers.write_temporary_configuration(
            supplied_configuration, "pyproject.toml"
        )

        # Act
        did_apply, did_error = pyproject_loader.apply_configuration(
            options, application_properties, results.keep_error
        )

    # Assert
    assert did_apply
    assert not did_error
    assert len(application_properties.property_names) == 1


def test_multisource_project_toml_does_not_exist() -> None:
    """
    Test that the add_local_pyproject_toml_file functions handles a pyproject.toml file that is not there.
    """

    # Arrange
    loader = MultisourceConfigurationLoader().add_local_pyproject_toml_file(
        "tool.utility"
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath("pyproject.toml")
        assert not os.path.isfile(project_configuration_file)

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 0


def test_multisource_project_toml_exists() -> None:
    """
    Test that the add_local_pyproject_toml_file functions handles a pyproject.toml file with a valid section.
    """

    # Arrange
    loader = MultisourceConfigurationLoader().add_local_pyproject_toml_file(
        "tool.utility"
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """[tool.utility]
some.thing = 1
"""

    with TestHelpers.change_to_temporary_directory():
        TestHelpers.write_temporary_configuration(
            supplied_configuration, "pyproject.toml"
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_raw_local_configuration_file_does_not_exist() -> None:
    """
    Test that the LocalProjectConfigurationFile class handles a default project configuration file that is not present.
    """

    # Arrange
    configuration_file_name = ".utility"

    pyproject_loader = LocalProjectConfigurationFile(
        configuration_file_name, ConfigurationFileType.JSON
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        assert not os.path.isfile(project_configuration_file)

        # Act
        did_apply, did_error = pyproject_loader.apply_configuration(
            options, application_properties, results.keep_error
        )

    # Assert
    assert not did_apply
    assert not did_error
    assert len(application_properties.property_names) == 0


def test_multisource_raw_local_configuration_file_with_specified_json_file() -> None:
    """
    Test that the LocalProjectConfigurationFile class handles a default JSON project configuration file.
    """

    # Arrange
    configuration_file_name = ".utility"

    pyproject_loader = LocalProjectConfigurationFile(
        configuration_file_name, ConfigurationFileType.JSON
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    supplied_configuration = """{ "some" : { "thing" : 1 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_apply, did_error = pyproject_loader.apply_configuration(
            options, application_properties, results.keep_error
        )

    # Assert
    assert did_apply
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_local_configuration_file_none_file_type() -> None:
    """
    Test that the add_local_project_configuration_file function handles a configuration file type of None.
    """

    # Arrange
    configuration_file_name = ".utility"

    # Act
    try:
        MultisourceConfigurationLoader().add_local_project_configuration_file(
            configuration_file_name, ConfigurationFileType.NONE
        )

        # Assert
        raise AssertionError("Should have thrown by now.")
    except ValueError as this_exception:
        assert (
            str(this_exception)
            == "Project configuration file must have a non-NONE file type set."
        )


def test_multisource_local_configuration_file_does_not_exist() -> None:
    """
    Test that the add_local_project_configuration_file function handles a configuration file that is not there.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_local_project_configuration_file(
        configuration_file_name, ConfigurationFileType.JSON
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        assert not os.path.isfile(project_configuration_file)

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 0


def test_multisource_local_configuration_file_with_specified_json_file() -> None:
    """
    Test that the add_local_project_configuration_file function handles a configuration file that is explicitly set to be a JSON configuration file.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_local_project_configuration_file(
        configuration_file_name, ConfigurationFileType.JSON
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """{ "some" : { "thing" : 1 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_local_configuration_file_with_specified_yaml_file_and_json_backup() -> (
    None
):
    """
    Test that the add_local_project_configuration_file function handles a configuration file that
    is explicitly set to be a YAML configuration file, is not present, while a `.json` file with
    the same file name prefix is present.
    """

    # Arrange
    configuration_file_name = ".utility"
    secondary_file_name = configuration_file_name + ".json"

    loader = MultisourceConfigurationLoader().add_local_project_configuration_file(
        configuration_file_name,
        ConfigurationFileType.YAML,
        [ConfigurationFileType.JSON],
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """{ "some" : { "thing" : 1 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(secondary_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_local_configuration_file_with_typed_specified_yaml_file_and_json_backup() -> (
    None
):
    """
    Test that the add_local_project_configuration_file function handles a configuration file that
    has a `.yaml` extension and is explicitly set to be a YAML configuration file, is not present,
    while a `.json` file with the same file name prefix is present.
    """

    # Arrange
    base_file_name = ".utility"
    configuration_file_name = f"{base_file_name}.yaml"
    secondary_file_name = base_file_name + ".json"

    loader = MultisourceConfigurationLoader().add_local_project_configuration_file(
        configuration_file_name,
        ConfigurationFileType.YAML,
        [ConfigurationFileType.JSON],
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """{ "some" : { "thing" : 1 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(secondary_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_raw_specified_configuration_file_does_not_exist() -> None:
    """
    Test that the SpecifiedConfigurationFile class handles a default project configuration file that is not present.
    """

    # Arrange
    configuration_file_name = ".utility"

    pyproject_loader = SpecifiedConfigurationFile(
        configuration_file_name, ConfigurationFileType.JSON
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        assert not os.path.isfile(project_configuration_file)

        # Act
        did_apply, did_error = pyproject_loader.apply_configuration(
            options, application_properties, results.keep_error
        )

    # Assert
    assert not did_apply
    assert did_error
    assert (
        results.reported_error
        == "Specified configuration file `.utility` does not exist."
    )


def test_multisource_raw_specified_configuration_file_with_specified_json_file() -> (
    None
):
    """
    Test that the SpecifiedConfigurationFile class handles a default JSON project configuration file that is not present.
    """

    # Arrange
    configuration_file_name = ".utility"

    pyproject_loader = SpecifiedConfigurationFile(
        configuration_file_name, ConfigurationFileType.JSON
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    supplied_configuration = """{ "some" : { "thing" : 1 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_apply, did_error = pyproject_loader.apply_configuration(
            options, application_properties, results.keep_error
        )

    # Assert
    assert did_apply
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_raw_specified_configuration_file_with_unspecified_json5_file_no_option() -> (
    None
):
    """
    Test that the SpecifiedConfigurationFile class handles a default JSON5 project configuration file that includes
    a comment, but without the json5 option enabled.
    """

    # Arrange
    configuration_file_name = ".utility"

    pyproject_loader = SpecifiedConfigurationFile(
        configuration_file_name, ConfigurationFileType.NONE
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    supplied_configuration = """
// Some comment
{ "some" : { "thing" : 1 }}
"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_apply, did_error = pyproject_loader.apply_configuration(
            options, application_properties, results.keep_error
        )

    # Assert
    assert not did_apply
    assert did_error
    assert (
        results.reported_error
        == f"Specified configuration file '{configuration_file_name}' was not parseable as a JSON, YAML, or TOML file."
    )


def test_multisource_raw_specified_configuration_file_with_unspecified_json5_file_option() -> (
    None
):
    """
    Test that the SpecifiedConfigurationFile class handles a default JSON5 project configuration file that includes
    a comment with the json5 option enabled.
    """

    # Arrange
    configuration_file_name = ".utility"

    pyproject_loader = SpecifiedConfigurationFile(
        configuration_file_name, ConfigurationFileType.NONE
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions(load_json_files_as_json5=True)

    supplied_configuration = """
// Some comment
{ "some" : { "thing" : 1 }}
"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_apply, did_error = pyproject_loader.apply_configuration(
            options, application_properties, results.keep_error
        )

    # Assert
    assert did_apply
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1

def test_multisource_specified_configuration_file_does_not_specified() -> None:
    """
    Test that the add_specified_configuration_file function handles a configuration file that is not specified.
    This can be the case if the argparse library is used and the configuration file was not specified.
    """

    # Arrange
    configuration_file_name = ""

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    with TestHelpers.change_to_temporary_directory():

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error


def test_multisource_specified_configuration_file_does_not_exist() -> None:
    """
    Test that the add_specified_configuration_file function handles a configuration file that is not there.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        assert not os.path.isfile(project_configuration_file)

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert did_error
    assert (
        results.reported_error
        == "Specified configuration file `.utility` does not exist."
    )


def test_multisource_specified_configuration_file_with_specified_json_file() -> None:
    """
    Test that the add_specified_configuration_file function handles a configuration file that is explicitly set to be a JSON configuration file.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name, ConfigurationFileType.JSON
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """{ "some" : { "thing" : 1 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_specified_configuration_file_with_detected_json_file_by_extension() -> (
    None
):
    """
    Test that the add_specified_configuration_file function handles a configuration file that
    is not specified with an explicit file type, but uses the file extension to detect that it
    is dealing with a JSON configuration file.
    """

    # Arrange
    configuration_file_name = ".utility.json"

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name, ConfigurationFileType.NONE
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """{ "some" : { "thing" : 1 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_specified_configuration_file_with_detected_bad_extension_reads_file_as_json() -> (
    None
):
    """
    Test that the add_specified_configuration_file function handles a configuration file with no explicit
    type and no matching configuration extension, but is detected as a JSON file.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name, ConfigurationFileType.NONE
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """{ "some" : { "thing" : 1 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_specified_configuration_file_with_detected_bad_extension_reads_file_as_yaml() -> (
    None
):
    """
    Test that the add_specified_configuration_file function handles a configuration file with no explicit
    type and no matching configuration extension, but is detected as a YAML file.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name, ConfigurationFileType.NONE
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """some:
  thing: 1
"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_specified_configuration_file_with_detected_bad_extension_reads_file_as_toml() -> (
    None
):
    """
    Test that the add_specified_configuration_file function handles a configuration file with no explicit
    type and no matching configuration extension, but is detected as a TOML file.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name, ConfigurationFileType.NONE
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """[some]
thing = 1
"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_specified_configuration_file_with_detected_bad_extension_should_read_as_non_configuration() -> (
    None
):
    """
    Test that the add_specified_configuration_file function handles a configuration file with no explicit
    type and no matching configuration extension, and is not detected as a valid configuration file.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name, ConfigurationFileType.NONE
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = "not a json file"

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert did_error
    assert (
        results.reported_error
        == "Specified configuration file '.utility' is not a valid YAML file."
    )


def test_multisource_specified_configuration_file_with_detected_bad_extension_reads_as_non_configuration() -> (
    None
):
    """
    Test that the add_specified_configuration_file function handles a configuration file with no explicit
    type and no matching configuration extension, and is not detected as a valid configuration file.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = MultisourceConfigurationLoader().add_specified_configuration_file(
        configuration_file_name, ConfigurationFileType.NONE
    )
    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """hallo: 1
bye
"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert did_error
    assert (
        results.reported_error
        == "Specified configuration file '.utility' was not parseable as a JSON, YAML, or TOML file."
    )


def test_multisource_raw_manually_set_properties_with_none() -> None:
    """
    Test that the ManuallySetProperties class handles a None list of manually specified properties.
    """

    # Arrange
    pyproject_loader = ManuallySetProperties(None)
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    # Act
    did_apply, did_error = pyproject_loader.apply_configuration(
        options, application_properties, results.keep_error
    )

    # Assert
    assert not did_apply
    assert not did_error


def test_multisource_raw_manually_set_properties_with_empty_list() -> None:
    """
    Test that the ManuallySetProperties class handles an empty list of manually specified properties.
    """

    # Arrange
    pyproject_loader = ManuallySetProperties([])
    application_properties = ApplicationProperties()
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    # Act
    did_apply, did_error = pyproject_loader.apply_configuration(
        options, application_properties, results.keep_error
    )

    # Assert
    assert not did_apply
    assert not did_error


def test_multisource_raw_manually_set_properties_with_simple() -> None:
    """
    Test that the ManuallySetProperties class handles a simple list of manually specified properties.
    """

    # Arrange
    pyproject_loader = ManuallySetProperties(["some.thing=1"])
    application_properties = ApplicationProperties(convert_untyped_if_possible=True)
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    # Act
    did_apply, did_error = pyproject_loader.apply_configuration(
        options, application_properties, results.keep_error
    )

    # Assert
    assert did_apply
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_raw_manually_set_properties_with_bad() -> None:
    """
    Test that the ManuallySetProperties class handles a bad list of manually specified properties.
    For this test, we use a property key that does not have an `=` sign or following value.
    """

    # Arrange
    pyproject_loader = ManuallySetProperties(["some.thing"])
    application_properties = ApplicationProperties(convert_untyped_if_possible=True)
    results = ErrorResults()
    options = MultisourceConfigurationLoaderOptions()

    # Act
    did_apply, did_error = pyproject_loader.apply_configuration(
        options, application_properties, results.keep_error
    )

    # Assert
    assert not did_apply
    assert did_error
    assert (
        results.reported_error
        == "Manually set property 'some.thing' was not validly formed: Manual property key and value must be separated by the '=' character."
    )


def test_multisource_manually_set_properties_with_none() -> None:
    """
    Test that the add_manually_set_properties function handles a None value.
    """

    # Arrange
    loader = MultisourceConfigurationLoader().add_manually_set_properties(None)
    application_properties = ApplicationProperties()
    results = ErrorResults()

    # Act
    did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 0


def test_multisource_manually_set_properties_with_empty() -> None:
    """
    Test that the add_manually_set_properties function handles an empty value.
    """

    # Arrange
    loader = MultisourceConfigurationLoader().add_manually_set_properties([])
    application_properties = ApplicationProperties()
    results = ErrorResults()

    # Act
    did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 0


def test_multisource_manually_set_properties_with_simple() -> None:
    """
    Test that the add_manually_set_properties function handles a simple list of manually specified properties.
    """

    # Arrange
    loader = MultisourceConfigurationLoader().add_manually_set_properties(
        ["some.thing=1"]
    )
    application_properties = ApplicationProperties(convert_untyped_if_possible=True)
    results = ErrorResults()

    # Act
    did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_order_manual_specified() -> None:
    """
    Test the ordering of the configuration sources.  Because the manual properties
    are added first, their value should be overwritten by the configuration file
    properties, which was added after the first.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = (
        MultisourceConfigurationLoader()
        .add_manually_set_properties(["some.thing=1"])
        .add_specified_configuration_file(
            configuration_file_name, ConfigurationFileType.JSON
        )
    )

    application_properties = ApplicationProperties(convert_untyped_if_possible=True)
    results = ErrorResults()

    supplied_configuration = """{ "some" : { "thing" : 2 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 2


def test_multisource_manual_order_specified() -> None:
    """
    Test the ordering of the configuration sources.  Because the manual properties
    are added first, their value should be overwritten by the configuration file
    properties, which was added after the first.
    """

    # Arrange
    configuration_file_name = ".utility"

    loader = (
        MultisourceConfigurationLoader()
        .add_specified_configuration_file(
            configuration_file_name, ConfigurationFileType.JSON
        )
        .add_manually_set_properties(["some.thing=1"])
    )

    application_properties = ApplicationProperties(convert_untyped_if_possible=True)
    results = ErrorResults()

    supplied_configuration = """{ "some" : { "thing" : 2 }}"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_raw_source_valid() -> None:
    """
    Test providing an "external" configuration source that is legitimate.
    """

    # Arrange
    external_source = ManuallySetProperties(["some.thing=1"])

    application_properties = ApplicationProperties(convert_untyped_if_possible=True)
    results = ErrorResults()

    # Act
    did_error = (
        MultisourceConfigurationLoader()
        .add_custom_source(external_source)
        .process(application_properties, results.keep_error)
    )

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1


def test_multisource_raw_source_invalid() -> None:
    """
    Test providing an "external" configuration source that is legitimate.
    """

    # Arrange
    external_source = cast(BaseConfigurationSource, "some object")

    # Act
    try:
        MultisourceConfigurationLoader().add_custom_source(external_source)

        # Assert
        raise AssertionError("Should have thrown by now.")
    except ValueError as this_exception:
        assert (
            str(this_exception)
            == "Added source 'some object' is not a valid configuration source."
        )


def test_multisource_load_json_with_comments_no_json5() -> None:
    """
    Test loading a json configuration file with comments, but with no json5 specified.
    """

    # Arrange
    configuration_file_name = ".utility.json"

    options = MultisourceConfigurationLoaderOptions(load_json_files_as_json5=False)
    loader = MultisourceConfigurationLoader(
        options
    ).add_local_project_configuration_file(
        configuration_file_name, ConfigurationFileType.JSON
    )

    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """
// This is an example.
{ "some" : { "thing" : 1 }}
"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert did_error
    assert (
        results.reported_error
        == f"Specified configuration file '{project_configuration_file}' is not a valid JSON file: Expecting value: line 2 column 1 (char 1)."
    )


def test_multisource_load_json_with_comments_with_json5() -> None:
    """
    Test loading a json configuration file with comments, with json5 specified.
    """

    # Arrange
    configuration_file_name = ".utility.json"

    options = MultisourceConfigurationLoaderOptions(load_json_files_as_json5=True)
    loader = MultisourceConfigurationLoader(
        options
    ).add_local_project_configuration_file(
        configuration_file_name, ConfigurationFileType.JSON
    )

    application_properties = ApplicationProperties()
    results = ErrorResults()

    supplied_configuration = """
// This is an example.
{ "some" : { "thing" : 1 }}
"""

    with TestHelpers.change_to_temporary_directory():
        project_configuration_file = os.path.abspath(configuration_file_name)
        TestHelpers.write_temporary_configuration(
            supplied_configuration, project_configuration_file
        )

        # Act
        did_error = loader.process(application_properties, results.keep_error)

    # Assert
    assert not did_error
    assert len(application_properties.property_names) == 1
    assert application_properties.get_integer_property("some.thing") == 1
