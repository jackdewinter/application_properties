# application_properties

[![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/application_properties)](https://github.com/jackdewinter/application_properties)
![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)
[![Python Versions](https://img.shields.io/pypi/pyversions/application_properties.svg)](https://pypi.org/project/application_properties)
[![Version](https://img.shields.io/pypi/v/application_properties.svg)](https://pypi.org/project/application_properties)

<!--
[![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/jackdewinter/application_properties/Main)](https://github.com/jackdewinter/application_properties/actions/workflows/main.yml)
[![Codecov](https://img.shields.io/codecov/c/github/jackdewinter/application_properties)](https://app.codecov.io/gh/jackdewinter/application_properties)
-->
![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/black/master)
![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/flake8/master)
![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/pylint/master)
[![Stars](https://img.shields.io/github/stars/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/stargazers)
[![Downloads](https://img.shields.io/pypi/dm/xxxx.svg)](https://pypistats.org/packages/xxxx)

[![Issues](https://img.shields.io/github/issues/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/issues)
[![License](https://img.shields.io/github/license/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/blob/main/LICENSE.txt)
[![Contributors](https://img.shields.io/github/contributors/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/network/members)

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=555)](https://www.linkedin.com/in/jackdewinter/)

The `application_properties` package was born out of necessity.
During the creation of the [PyMarkdown](https://github.com/jackdewinter/pymarkdown) project,
there was a distinct need for a configuration subsystem that was able to handle more
complex configuration scenarios.

The `application_properties` library has the following advnatages:

- Thoroughly tested
  - The project currently has over 65 tests and coverage percentages over 99%.
- Simple... With Examples
  - The package was created with the intention of being as easy to use as possbile.
  - To that extent, there are 4 basic usage examples and over 10 advanced usage examples.
- Complex When Required
  - The default is simplicity, but the package can step up when required to do so.
  - Any actions outside of the simple scenario of getting an optional string value should
    be relatively easy to request of the package API.
- Hierarchically Aware
  - By default, uses the `.` character in the property names to define levels of hierarchy.
  - Hierarchy levels can be used to find only those properties that exist under a
    given hierarchy.
  - If desired, the `ApplicationPropertiesFacade` object can be used to restrict access
    to only those properties that exist under a given hierarchy.
- Command Line Aware
  - The `set_manual_property` function allows for one or more individual properties to be
    supplied by the command line.
- Extensible
  - The loading of the properties is separate from access to the values for those properties.
  - Due to the separation of the loading and accessing parts of the library, custom loading
    classes can be added with ease.
    - Current loading classes include loaders for Json files, with Simple Property files right
      around the corner

## Requirements

This project required Python 3.8 or later to function.

## Installation

```sh
pip install app_prop
```

## How To Use This Package

The primary goal of this package is to provide a simple, easy to use interface
to access properties within a Python script or program.  It is our contention
that 80% or more of general usage of such a package will be focused on two
elements:

- loading a group of properties from a file that is properly formatted
  for a given format
- accessing a specific string property, possibly with a default, from the that
  property store

The examples in this section focus specifically on those elements, with more
examples for the other scenarios being available in the
[Advanced Examples document](https://github.com/jackdewinter/application_properties/blob/main/docs/advanced_examples.md).

### A Word On The Examples

This section on `How To Use This Package` provides easy to follow Python code snippets.
Each snippet is available as a complete Python script file in the project's
[examples directory](https://github.com/jackdewinter/application_properties/tree/main/examples).
To ensure the integrity of each Python script, the following lines are present at
the start of each Python file:

```Python
import os
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()))  # isort:skip
```

This prefix allows our team to frequently execute these samples from the project's base
directory, on the watch for any changes in behavior.

For the sake of brevity, as those lines are at the start of every
example file, their use is documented here and will remain absent from any
Python examples presented in the following sections.

### Example 01 - Get A String Property From An Empty Property Instance

The Python script for
[Example 01](https://github.com/jackdewinter/application_properties/blob/main/examples/example_01.py)
illustrates the basics of using
the `application_properties` package.  This example imports the `ApplicationProperties`
class from the `application_properties` package, then creating a new instance of
that class and assigning it to the `properties` variable.  Next, the example prints
the result of calling the `get_string_property` for that new instance of the class,
having requested the value for the property named `my_property`.

```Python
from application_properties import ApplicationProperties

properties = ApplicationProperties()
print(properties.get_string_property("my_property"))
```

As there are no properties present in the instance, the output is predictably:

```text
None
```

### Example 02 - Get A String Property After Loading Json Data Into The Property Instance

For the purposes of this example, the
[example data file](https://github.com/jackdewinter/application_properties/blob/main/examples/example_data.json),
`example_data.json`, contains the following JSON object:

```json
{
    "my_property" : "test data"
}
```

The Python script for
[Example 02](https://github.com/jackdewinter/application_properties/blob/main/examples/example_02.py),
takes the previous script and includes the
import for the `ApplicationPropertiesJsonLoader` loader class. Then, after the declaration
and assignment of the `properties` instance, as was done in the previous example, the script
then calls the `load_and_set` function of the `ApplicationPropertiesJsonLoader` loader class
to load the data file into the `properties` instance:

```Python
from application_properties import ApplicationProperties, ApplicationPropertiesJsonLoader

properties = ApplicationProperties()
ApplicationPropertiesJsonLoader.load_and_set(
    properties, os.path.join(os.path.dirname(__file__), "example_data.json")
)
print(properties.get_string_property("my_property"))
```

As the data file contains a single value with the name `my_property`, with the string value of
`test data` assigned to it.

```text
test data
```

However, that example only shows what happens if the value is present.  The
sibiling example,
[Example 02A](https://github.com/jackdewinter/application_properties/blob/main/examples/example_02a.py),
is the same script with the exception of changing the line:

```Python
print(properties.get_string_property("my_property"))
```

to:

```Python
print(properties.get_string_property("my_other_property"))
```

In this case, there are valid properties loaded, but none of those properties
have the name `my_other_property`. As such, the result that is printed is:

```text
None
```

### Example 03 - Get A String Property With A Default Value

Keeping with the theme of introducing gradual changes as the examples progress,
the only change that was made from
[Example 02A](https://github.com/jackdewinter/application_properties/blob/main/examples/example_02a.py)
to
[Example 03](https://github.com/jackdewinter/application_properties/blob/main/examples/example_03.py)
was that the call to `get_string_property` was modified to include a default
value parameter:

```Python
from application_properties import ApplicationProperties, ApplicationPropertiesJsonLoader

properties = ApplicationProperties()
ApplicationPropertiesJsonLoader.load_and_set(
    properties, os.path.join(os.path.dirname(__file__), "example_data.json")
)
print(properties.get_string_property("my_other_property", default="default value"))
```

When the example is executed, no value is found for the property `my_other_property`,
the same as before.  However, due to the the `default` parameter,  the function has
been instructed to return something other than `None` if nothing was found.  Therefore,
the result that is printed is:

```text
default value
```

### Example 04 - Simple Property File Loader

TBD

### Advanced Examples

As mentioned before, while the bulk of property accessing and loading operations can be
accomplished using information from the above basic examples, more advanced
examples are available in the
[Advanced Examples document](https://github.com/jackdewinter/application_properties/blob/main/docs/advanced_examples.md).

## Finding Issues

If you find any issues, please report them using the standard GitHub issues process. When
our team looks at your issue and triages it, we will assign it a priority and try our best
to make that priority transparent within the project's repository.

## When Did Things Change?

The changelog for this project is maintained [at this location](changelog.md).

## Still Have Questions?

If you still have questions, please consult our [Frequently Asked Questions document](docs\faq.md).

## Contact Information

If you would like to report an issue with the library or its documentation, please
file an issue [using GitHub](https://github.com/jackdewinter/application_properties/issues).

If you would like to us to implement a feature that you believe is important, please
file an issue [using GitHub](https://github.com/jackdewinter/application_properties/issues)
that includes what you want to add, why you want to add it, and why it is important.
Please note that the filing of your issue will usually be the start of a conversation,
and be ready for more questions.

If you would like to contribute to the project in a more substantial manner, please contact me
at jack.de.winter at outlook.com.

## Instructions For Contributing

Developer notes on various topics are kept in the the
[Developer Notes document](docs\developer.md).

If you attempting to contribute something to this project, please follow the steps outlined
in the [CONTRIBUTING.md file](CONTRIBUTING.md).
