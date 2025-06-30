# User Guide

This document is geared towards getting you and your team up and running as
quickly as possible with this library.

## Requirements

This project requires Python 3.9 or later to function.

## Installation

```sh
pip install application_properties
```

## How To Use This Package

The primary goal of this package is to provide a simple, easy to use interface
to access properties within a Python script or program.  It is our team's contention
that 80% or more of general usage of such a package will be focused on two
elements:

- loading a group of properties from configuration sources, typically one or more
  file properly formatted files
- accessing a specific property, possibly with a default, from a configuration
  manager that has loaded one or more configuration sources

Note that we try our best to provide you with examples that you can run on
your own.  If that is not the case with any of these examples, please let
us know.

## Starting with Something Simple

<!--- pyml disable-next-line no-duplicate-heading-->
### Goals

The goals for this section are to introduce:

- the `MultisourceConfigurationLoader` class used to load configuration sources
- the `get_string_property` function used to query an `ApplicationProperties` instance
  which has loaded zero or more data sources

<!--- pyml disable-next-line no-duplicate-heading-->
### Example

Starting on our journey of using the `application_properties` package,
one of the simplest practical examples can be demonstrated by creating the
file `sample.py` and adding the following Python code to that file:

```Python
from sys import stderr
from typing import Optional
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader, ConfigurationFileType

def print_error_to_stdout(formatted_error: str, thrown_exception: Optional[Exception]) -> None:
    print(formatted_error, file=stderr)

# lines to change will be after this comment

properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
did_error = loader.process(properties, print_error_to_stdout)
print(f"did_error = {did_error}")

property_value = properties.get_string_property("mode", "(None)")
print(f"property_value = {property_value}")
```

Running this example using the command line `python sample.py` produces
the following output:

```text
did_error = False
property_value = (None)
```

<!--- pyml disable-next-line no-duplicate-heading-->
### Explanation

Starting with the main block at the second half of the example, the script
creates instances of the `ApplicationProperties` and `MultisourceConfigurationLoader`
classes.  It then calls the `loader.process` function to process any registered
configuration sources.  As this is the first example, this currently does nothing
as we have not yet defined any configuration
sources to load configuration items from.  Likewise, the `properties.get_string_property`
function is called
to get a value from the configuration manager, but since nothing was loaded,
the default value supplied to the `get_string_property` function is returned.

An important thing to point out about this example is the `print_error_to_stdout`
function.  The
`process` function takes an instance of the `ApplicationProperties` class and
an optional function to use to provide information on any errors that occurred.
If no function is provided, the error is written to [standard out](https://www.howtogeek.com/435903/what-are-stdin-stdout-and-stderr-on-linux/).
In this example, instead of writing that output to standard out,
the `print_error_to_stdout` function is used to write the error information to
standard error.

This is important because our team designed the `application_properties` package
to [work by default](./getting-started.md#our-philosophy-of-work-by-default).
When errors occur, the default action is to write information about those errors
to standard out to ensure that they are visible to the user. We believe that
most applications will want to provide an alternative way to manage the error.
However, instead of trying to second guess the application, we defined a
default handler function that meets our "work by default" philosophy.

<!--- pyml disable-next-line no-duplicate-heading-->
### Things To Try

Experiment with the following to see what happens, executing the script again
when needed:

- change the key and the default value for the `get_string_property` to see what
  effect that has on the returning value `property_value`
- remove the `handle_error_fn` parameter passed into the `process` function to
  see what the default behavior is

## Adding A Configuration File

<!--- pyml disable-next-line no-duplicate-heading-->
### Goals

The goals for this section are to introduce:

- how the `MultisourceConfigurationLoader` class manages explicitly specified
  configuration files
- how the loading of a configuration file influences the configuration items and
  their retrieval

<!--- pyml disable-next-line no-duplicate-heading-->
### Example

With the basics taken care of, the next step to take on our journey involves the
handling of a single configuration file.  For this example, you need to create a
configuration file in the same directory as the example code above, with a name
of `.sample` and the content:

```json
{
    "mode" : "2",
    "some" : {
      "thing" : 3
    }
}
```

To make use of this specific configuration file, we need to change the bottom
part of the above example to:

```Python
# lines to change will be after this comment

properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_specified_configuration_file(".sample", ConfigurationFileType.JSON)

did_error = loader.process(properties, print_error_to_stdout)
print(f"did_error = {did_error}")

property_value = properties.get_string_property("mode", "(None)")
print(f"property_value = {property_value}")
```

Running the changed example with the `.sample` configuration file located in the
same directory produces the following output:

```text
did_error = False
property_value = 2
```

<!--- pyml disable-next-line no-duplicate-heading-->
### Explanation

To facilitate the loading of the configuration file `.sample`, the function
`add_specified_configuration_file` was called with the first parameter being the
relative file name of the configuration file.  The second parameter is set to `ConfigurationFileType.JSON`
to specify that the configuration file is a JSON file. During the execution of
the `process` function, the `print_error_to_stdout` will be called if the specified
configuration file is not present or if it is not parseable JSON.

With the configuration file in place and the `add_specified_configuration_file`
function telling the `MultisourceConfigurationLoader` where it is, the invoking
of the `process` function results in the `get_string_property` returning the value
`2`.  This is because the `process` function now applies the configuration source
specified as the configuration to the configuration manager instance `properties`
that is passed as its first parameter. Therefore, when the `get_string_property`
function is invoked, the configuration manager finds the `mode` property and relay
its value as `2`.

<!--- pyml disable-next-line no-duplicate-heading-->
### Things To Try

Experiment with the following to see what happens, executing the script again
when needed:

- add "garbage" characters to the end of the content of the `.sample` file to invalidate
  the JSON in the file
- temporarily change the name of the `.sample` file to something else
- try the above experiments with and without the `print_error_to_stdout`
- try the above experiments with and without the line `sys.exit(1)` at the end
  of the `print_error_to_stdout` function

## Get Property Functions

<!--- pyml disable-next-line no-duplicate-heading-->
### Goals

The goals for this section are to introduce:

- returning `None` if a default is not provided to the `get_*_property` family
  of functions
- the `get_integer_property` function and `get_boolean_property` used to query
  an `ApplicationProperties` instance

<!--- pyml disable-next-line no-duplicate-heading-->
### Example

To make use of the specific configuration file from the previous section, we need
to change the very bottom part of the previous example to:

```Python
string_property_value = properties.get_string_property("mode")
integer_property_value = properties.get_integer_property("some.thing", -1)
boolean_property_value = properties.get_boolean_property("some.switch", False)
print(f"string_property_value  = {string_property_value}")
print(f"integer_property_value = {integer_property_value}")
print(f"boolean_property_value = {boolean_property_value}")
```

Running the changed example with the `.sample` configuration file in the same directory
produces the following output:

```text
did_error = False
string_property_value  = 2
integer_property_value = 3
boolean_property_value = False
```

<!--- pyml disable-next-line no-duplicate-heading-->
### Explanation

For the retrieval of configuration item values, three changes were made.  The first
change was to remove the default value from the call to the `get_string_property`
function.  All `get_*_property` functions will return the value `None` if no default
is provided. If the value of `None` is not the desired default value, that desired
default value can simply be passed in as an argument.

The second change is the addition of the `get_integer_property` and `get_boolean_property`
functions for retrieving integer and boolean values from the configuration manager.
The supplying of a default value assures that a reasonable known value will be returned
if no configuration item is found.  To keep things simple [until later](./user-guide.md#strict-mode-and-type-conversion-when-getting-property-values),
the values presented in the configuration file are the same types as the requested
values, so no conversion is needed by the configuration manager.

Finally, the third and arguably most important change is that the `get_integer_property`
function and the `get_boolean_property` function specifies the
[hierarchical](./getting-started.md#hierarchical) key of `some.thing`.

Inside of the configuration file is this fragment:

```json
    "some" : {
      "thing" : 3
    }
```

This fragment implies that there is a key of `some` that is an object that contains
a key of `thing` that has the numeric value of `3`.  Therefore, calling the function
`get_integer_property` with the [flattened hierarchical](./getting-started.md#flattened-hierarchical)
representation of that hierarchy, the key `some.thing`, retrieves the correct value.
Similarly, when the `get_boolean_property` function is called with the key `some.switch`,
it is easy to see that there is no `switch` property under the `some` key's hierarchy.
As such, the default value is returned.  This concept of configuration items being
stored [hierarchically](./getting-started.md#hierarchical) is important, allowing
both the application and its user to understand what configuration items are logically
grouped together by the application.

<!--- pyml disable-next-line no-duplicate-heading-->
### Things To Try

Experiment with the following to see what happens, executing the script again
when needed:

- change the hierarchy keys in the `.sample` file and try to match the changes required
  in the `get_string_property` and the `get_integer_property` functions
- try adding a `some.switch` property to the `.simple` file with a value of `true`
  to determine its effect on the `get_boolean_property` and is returned value

## Project Default Configuration Files

<!--- pyml disable-next-line no-duplicate-heading-->
### Goals

The goals for this section are to introduce:

- default configuration files not specified on the command line
- configuration layers and how they interact with each other

<!--- pyml disable-next-line no-duplicate-heading-->
### Example

For this example, create a new file `pyproject.toml` in the current directory
with the content:

```toml
[tool.everywhere]
some.one = 1
```

and create a new file `project.yaml` in the current directory with the
content:

```yaml
some:
  when: 2
```

Once that is done, change the lower half of the example's content to:

```Python
# lines to change will be after this comment

properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_local_pyproject_toml_file("tool.everywhere")
loader.add_local_project_configuration_file("project.yaml", ConfigurationFileType.YAML)
loader.add_specified_configuration_file(".sample", ConfigurationFileType.JSON)
did_error = loader.process(properties, print_error_to_stdout)

some_one_value = properties.get_integer_property("some.one")
some_when_value = properties.get_integer_property("some.when")
some_thing_value = properties.get_integer_property("some.thing")
print(f"some_one_value   = {some_one_value}")
print(f"some_when_value  = {some_when_value}")
print(f"some_thing_value = {some_thing_value}")
```

Running the changed example now produces the following output:

```text
some_one_value   = 1
some_when_value  = 2
some_thing_value = 3
```

<!--- pyml disable-next-line no-duplicate-heading-->
### Explanation

The changes made to the example's `MultisourceConfigurationLoader` section add
support for including the `pyproject.toml` file and the project default configuration
file when loading configuration sources.  For the function `add_local_pyproject_toml_file`,
the parameter represents the section in the `pyproject.toml` file that we want
to load.  Since our example `pyproject.toml` file contains a `[tool.everywhere]`
section with our values, the example uses `tool.everywhere` as the parameter.
For the function the function `add_local_project_configuration_file`, the parameters
represent the configuration file to load, if it is present, and the type of configuration
file that is being provided. While the extension is usually a giveaway, this makes
it clear to the `add_local_project_configuration_file` function that the configuration
file is a YAML file.

An important concept to note is the concept of [configuration layering](./getting-started.md/#configuration-ordering-layering).
When the `process` function is called, the configuration sources are applied in the
order in which they are registered.  Starting at the top, the `pyproject.toml` file
is applied, setting configuration item `some.one` to `1`.  Then the `project.yaml`
file is applied, setting configuration item `some.when` to `2`.  Finally, the `.sample`
file is applied, setting configuration item `some.thing` to `3`.

What does this mean for users of your application? It means that configuration items
specified in the `.sample` file will override configuration items specified in the
`project.yaml` file which will override configuration items specified in the `pyproject.toml`
file.  This layering allows you to build a hierarchy of configuration layers that
you and your team feel are important and understandable to the users of your application.

A concrete application of this is visible in this documentation.  To generate this
documentation, our team uses the `mkdocs` package which uses the `markdown` package
to interpret the Markdown for these pages.  As the `markdown` package has some
peculiarities when it comes to list indents, we have this JSON snippet as part
of our configuration file:

```json
{
    "plugins": {
        "ul-indent" : {
            "enabled": false
        },
        "list-anchored-indent" : {
            "enabled": true
        }
    }
}
```

This configuration disables the standard indent rule (`ul-indent`) and enables
the rule `list-anchored-indent` specifically created to handle the `markdown` package
indent. However, at the project level, we have a configuration file:

```json
{
    "extensions": {
        "front-matter" : {
            "enabled" : true
        },
        "linter-pragmas": {
            "enabled" : true
        }
    }
}
```

This allows us to specify a group of configuration items at a project level,
combining those items with more specific configuration items based on the
needs of the tool where this documentation is being built.  We feel strongly
that this feature is very important in providing a flexible configuration
management system.

<!--- pyml disable-next-line no-duplicate-heading-->
### Things To Try

Experiment with the following to see what happens, executing the script again when
needed:

- change the names of the configuration items in all three files to `some.thing`
  and notice the change to the output
- change the names of the configuration items in all three files to `some.thing`
  and notice the change to the output when changing the ordering of the three
  `add_*` functions for the `loader` instance

## Setting Individual Properties

<!--- pyml disable-next-line no-duplicate-heading-->
### Goals

The goals for this section are to introduce:

- setting general properties from the command line
- one option for setting specific properties from the command line
- the use of special characters when specifying non-string command line properties

<!--- pyml disable-next-line no-duplicate-heading-->
### Example

For this example, change the lower half of the example's content to:

```Python
# lines to change will be after this comment

args_set_configuration = [ "some.one=me", "some.when=$#12" ]

args_set_verbosity = 3
if args_set_verbosity is not None:
    args_set_configuration.append(f"verbosity=$#{args_set_verbosity}")

properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_manually_set_properties(args_set_configuration)
did_error = loader.process(properties, print_error_to_stdout)

some_one_value = properties.get_string_property("some.one")
some_when_value = properties.get_integer_property("some.when")
verbosity_value = properties.get_integer_property("verbosity")
print(f"some_one_value   = {some_one_value}")
print(f"some_when_value  = {some_when_value}")
print(f"verbosity_value  = {verbosity_value}")
```

Running the changed example now produces the following output:

```text
some_one_value   = me
some_when_value  = 12
verbosity_value  = 3
```

<!--- pyml disable-next-line no-duplicate-heading-->
### Explanation

This example is lengthy, so it bears breaking down into distinct components.

The first part of the example deals with setting general properties from the command
line.  The setting of the `args_set_configuration` variable mimics what the `argparse`
package's `parseArgs` function would return in the `args.set_configuration`
variable if the [`add_default_command_line_arguments`](https://github.com/jackdewinter/application_properties/blob/main/application_properties/application_properties_utilities.py)
was provided to one of the `argparse` parsers.  With an action of `append` and
a destination of `set_configuration`, each command line `--set` argument appends
the string value that follows it to the `set_configuration` list of strings. Therefore,
given the command line arguments of `--set some.one=me --set some.when=$#12`,
it is reasonable to assume that the `args.set_configuration` value would be set
to `[ "some.one=me", "some.when=$#12" ]`. Passing that array of strings to
the `add_manually_set_properties` function results in the instance of the
`MultisourceConfigurationLoader` class trying to apply those general command
line settings into the configuration manager.

The second part of the example takes a simple command line argument and translates
it into a form that can then be passed with the other strings into the `add_default_command_line_arguments`
function.  In this example, the application allows for a `--verbosity` command line
argument that specifies an integer.  Behind the scenes, it is assumed that an `argparse`
argument is set up that will use `--verbose` and capture the integer value that
appears on the command line after it.  To avoid having to check both `args.verbosity`
and the `verbosity` configuration item later in the application, this example shows
how the `args_set_verbosity` value can be reformatted and appended to the list
of general configuration strings.

Finally, to make both of the above settings work, the `add_manually_set_properties`
function is called with the array of strings to interpret as configuration item
keys and values.  From the perspective of the `add_manually_set_properties` function,
it does not have any knowledge of any string specified in the array.  It simply
takes the array of string values and processes them.  While this approach may not
work for every application, we present this approach as something to consider to
reduce the complexity of your application.

And in case you are wondering about the special characters before two of the three
values, those special characters specify [configuration item types](./command-line.md/#configuration-item-types).
As command lines only deal with strings, our team needed some form of "encoding"
that would allow us to infer the type of a value from the value itself.  According
to the configuration item type table, no special `$` characters at the start of
the value leave the value's type as a string.  For the two values that start with
the `$#` sequence, that means to treat the value as an integer type.

<!--- pyml disable-next-line no-duplicate-heading-->
### Things To Try

Experiment with the following to see what happens, executing the script again
when needed:

- Remove the configuration item type indicators and see what changes.
- Change the [configuration item type](./command-line.md/#configuration-item-types)
  sequences for the values in the array and see how they work with the `get_*_property`
  functions.

## Strict Mode and Type Conversion When Getting Property Values

<!--- pyml disable-next-line no-duplicate-heading-->
### Goals

The goals for this section are to introduce:

- `strict_mode` and its effect on retrieving values
- `convert_untyped_if_possible` and its effect on retrieving values

Please note that `strict_mode` and `convert_untyped_if_possible` can both be set
at when the instance of the `ApplicationProperties` class is created.  However,
`strict_mode` may also be specified at the `get_*_property` level.

<!--- pyml disable-next-line no-duplicate-heading-->
### Example

For this example, create a new python file and set its content to:

```Python
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader

args_set_configuration = [ "some.one=me", "some.when=tomorrow", "some.number=$#1", "some.other-number=1" ]
properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_manually_set_properties(args_set_configuration)
loader.process(properties)

try:
    some_where_value = properties.get_string_property("some.where", "default", strict_mode=True)
    print(f"some_where_value = {some_where_value}")
except ValueError as this_exception:
    print(f"some_where_value = Exception({this_exception})")

try:
    some_where_value = properties.get_string_property("some.number", "default", strict_mode=True)
    print(f"some_where_value = {some_where_value}")
except ValueError as this_exception:
    print(f"some_where_value = Exception({this_exception})")

try:
    some_where_value = properties.get_string_property("some.number", "default", strict_mode=False)
    print(f"some_where_value = {some_where_value}")
except ValueError as this_exception:
    print(f"some_where_value = Exception({this_exception})")

try:
    some_where_value = properties.get_integer_property("some.other-number", -1, strict_mode=True)
    print(f"other_value = {some_where_value}")
except ValueError as this_exception:
    print(f"other_value = Exception({this_exception})")

args_set_configuration = [ "some.other-number=1" ]
properties = ApplicationProperties(strict_mode=True, convert_untyped_if_possible=True)
loader = MultisourceConfigurationLoader()
loader.add_manually_set_properties(args_set_configuration)
loader.process(properties)

try:
    some_where_value = properties.get_integer_property("some.other-number", -1, strict_mode=True)
    print(f"other_value = {some_where_value}")
except ValueError as this_exception:
    print(f"other_value = Exception({this_exception})")
```

Running the example now produces the following output:

```text
some_where_value = default
some_where_value = Exception(The value for property 'some.number' must be of type 'str'.)
some_where_value = default
other_value = Exception(The value for property 'some.other-number' must be of type 'int'.)
other_value = 1
```

<!--- pyml disable-next-line no-duplicate-heading-->
### Explanation

When getting the value to return from any of the `get_*_property` functions, most
of the validation logic is the shared.  The `property_name` and `property_type`
parameters are validated and a `default_value` parameter that is non-`None` is
validated to ensure it is the same type as the type of requested property.  Failures
on any of these validations raise a `ValueError`.  Then, if the value is present
in the configuration manager, the configuration item value is retrieved and checked
to see if it is the same type as the requested type. (Note that validation functions
and the impact of `strict_mode` on them are covered in the
[next section](./user-guide.md#required-properties-and-validation-functions) ).

Given that background, the output from the first example is the string `default`
as expected as the key `some.where` is not present in the configuration manager.
This is different than the output from the second example, which shows the result
of requesting a configuration item where the configuration item is present and `strict_mode`
is enabled: an exception is generated. This is not the case when the third example
is called, as `strict_mode` is disabled, and the default value is returned. Therefore,
one of two reasons that `strict_mode` exists is to ensure that if your application
wants to ask for a configuration item and expects it to be a specific type, that
it will behave in one of three ways: return the default value if the configuration
item is not present, raise an exception if the configuration item is present but
of the wrong type, or return the configuration item's value.

Needing a way to address certain combinations where a type can be interpreted as
another type, the `convert_untyped_if_possible` mode was created. The `convert_untyped_if_possible`
parameter provides a bridge between non-strict and strict modes. Set at a global
level, this flag allows for configuration items with a string type to be automatically
translated into either a boolean type or an integer type. The reason this is done
at a global level is that our survey of applications seemed to indicate that these
types of conversions were either always supported or never supported, with no middle
ground.  As such, we decided to reflect the results of those surveys in our approach
to converting types.

The best example of these kinds of conversions are the old types of configuration
files which were of the form `key:{optional whitespace}value`.  In those situations,
an application may want to allow the value `1` from `my.key: 1` to be kept as a
string or to be converted to an integer at the applications request.  Our hope is
that our `convert_untyped_if_possible` mode will allow for this to happen, becoming
more flexible and responsive the needs of applications... while allowing `strict_mode`
to be used at the same time.

<!--- pyml disable-next-line no-duplicate-heading-->
### Things To Try

Experiment with the following to see what happens, executing the script again when
needed:

- strict mode and its effects on how you think about retrieving configuration items
  and their values
- how strings are converted into integers and booleans, and how it matches your
  expectations

## Required Properties and Validation Functions

<!--- pyml disable-next-line no-duplicate-heading-->
### Goals

The goals for this section are to introduce:

- required properties for the `get_*_property` functions
- validation functions for the `get_string_property` and `get_integer_property` functions

<!--- pyml disable-next-line no-duplicate-heading-->
### Example

For this example, create a new python file and set its content to:

```Python
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader

args_set_configuration = [ "some.one=me", "some.when=tomorrow", "some.number=$#1" ]
properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_manually_set_properties(args_set_configuration)
loader.process(properties)

def my_get_string(config_name, is_required = False, strict_mode = False, valid_value_fn = None):
    modified_name = config_name.replace(".", "_")
    try:
        retrieved_value = properties.get_string_property(config_name, is_required=is_required,
            strict_mode=strict_mode, valid_value_fn = valid_value_fn)
        print(f"{modified_name}_value = {retrieved_value}")
    except ValueError as this_exception:
        print(f"{modified_name}_value = Exception({this_exception})")

my_get_string("some.where", is_required=True)
my_get_string("some.number", is_required=True)

def some_one_validation_function(property_value: str) -> None:
    if property_value not in ["me", "you", "them"]:
        raise ValueError(f"Value '{property_value}' is not 'me', 'you' or 'them'")

my_get_string("some.one", valid_value_fn=some_one_validation_function)
my_get_string("some.when", valid_value_fn=some_one_validation_function)
my_get_string("some.when", valid_value_fn=some_one_validation_function, strict_mode=True)
```

Running the example produces the following output:

```text
some_where_value = Exception(A value for property 'some.where' must be provided.)
some_number_value = None
some_one_value = me
some_when_value = None
some_when_value = Exception(The value for property 'some.when' is not valid: Value 'tomorrow' is not 'me', 'you' or 'them')
```

<!--- pyml disable-next-line no-duplicate-heading-->
### Explanation

The first example shows a request to the configuration manager for the value of
`some.where` which is not one of the configuration items set in the `args_set_configuration`
variable in the first block of code.  When the function `get_string_property` is
called with the property name set to `some.where` and the parameter `is_required`
set to `True`, a `ValueError` exception is raised providing the details that configuration
item is not present.  The second example is similar but tries to call `get_string_property`
for an existing configuration item `some.number` that has an integer type.  This
succeeds from a `is_required` point of view because the `is_required` flag validation
on checks to see if the configuration item exists, nothing else.

The third, fourth and fifth examples are all variations on a theme, using the `get_string_property`
function with a validation function.  In the third example, the value being validated
passes and is therefore returned to the caller. The fourth and fifth examples are
similar exception for the `strict_mode` parameter. As a default, the code behind
the `get_*_property` functions only sets the return value if every validation passes,
as shown in the `None` output for the fourth example.  This follows our team's
[work by default](./getting-started.md#our-philosophy-of-work-by-default) philosophy
as we generally expect application to pass in default values that are reasonable
for their application.  If the configuration is not set properly and they have not
turned on `strict_mode` in some form, we believe the reasonable thing to do is to
return that default value.  However, if the application is a stickler for values
(as our team is), setting `strict_mode` at either a local or global level changes
the response to what is returned in
the fifth example.

It is important to remember that the `valid_value_fn` function is that it is always
the last validation executed before the property's value is changed from its default
value to the value located in the configuration item. By the time the `get_*_property`
function executes, any errors have either been raised as exceptions or noted internally
to prevent the setting of the value.  If a type conversion was required, it has
already been performed.  What we are trying to say is that the `valid_value_fn`
function should only worry about one thing: checking to see if the value passed
in, which is already correctly typed, is valid for the scenario in question.

<!--- pyml disable-next-line no-duplicate-heading-->
### Things To Try

Experiment with the following to see what happens, executing the script again when
needed:

- write your own version of the above example, playing around with parameters and
  configuration item values

## Future Documentation

We ran out of time before the current release to cover everything that
we want to.  Our team will try to find time in the upcoming weeks to
provide user guide documentation on the following items.

Please note that if what you are looking for is in this list, there is
always the option of looking at the source code for the `application_properties`
package on [GitHub](https://github.com/jackdewinter/application_properties) and
working it out for yourself.

- MultisourceConfigurationLoader
    - MultisourceConfigurationLoaderOptions to load JSON5 (with comments)
- add_local_project_configuration_file
    - behavior if file not found with alternate_extension_types
- add_specified_configuration_file
    - config_file_type = None and auto-detect, why dangerous
- add_custom_source
- ApplicationPropertiesFacade
- app_prop
    - get*_property with strict mode
    - property_names
    - enable_strict_mode
    - enable_convert_untyped_if_possible
    - load_from_dict
    - verify_full_part_form and verify_full_key_form
    - verify_manual_property_form
    - set_manual_property
