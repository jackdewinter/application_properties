# Heavy Lifting [TBD]

These two classes represent the majority of the `application_properties` package.
[tbd fill out a bit]

An instance of
the `MultisourceConfigurationLoader` class is called once for each type of data
source to load.
When the `process` call is made on that instance, each data source is loaded in
order and
its contents are added to an in-memory dictionary of configuration items. If the
key for
a configuration item is already present, its value is overridden with the new value.
Once
all data sources have been loaded, the `MultisourceConfigurationLoader` instance
loads that
dictionary of configuration items to the provided instance of the `ApplicationProperties`
instance. At that point, the calling application is free to call any of the methods
on that
instance.

**NOTE:** [tbd] links to api docs where possible, auto-generated

## The `MultisourceConfigurationLoader` Class

The [`MultisourceConfigurationLoader`](/api/application_properties/#application_properties.MultisourceConfigurationLoader)
class
is the built-in [Configuration Loader](./basic-concepts.md#configuration-loader).
Its sole responsibility
is to accept registrations for one or more [Configuration Data Sources](./basic-concepts.md#configuration-data-sources),
loading
data from each source, in order, once the `process` method is called.

**NOTE:** The information on this page is complimented by the
[Quick Start: Configuration Loaders](./quick-starts/loaders.md) page.

add_local_pyproject_toml_file
add_local_project_configuration_file
add_specified_configuration_file
add_manually_set_properties
add_custom_source

process

## The `ApplicationProperties` Class

The [`ApplicationProperties`](/api/application_properties/#application_properties.ApplicationProperties)
class.

### Ctor

        strict_mode: bool = False,
        convert_untyped_if_possible: bool = False,
        allow_separator_in_keys: bool = False,

clear
load_from_dict
set_manual_property

get_boolean_property
get_integer_property
get_string_property
get_string_list_property

verify_full_part_form
verify_full_key_form
verify_manual_property_form

separator
number_of_properties
property_names
property_names_under

strict_mode
enable_strict_mode

convert_untyped_if_possible
enable_convert_untyped_if_possible

[2](./quick-starts/getters.md)

[7](./quick-starts/validation.md)
