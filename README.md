# application_properties

Put **Badges** here

The `application_properties` package was born out of necessity.
During the creation of the [PyMarkdown](https://github.com/jackdewinter/pymarkdown) project,
there was a distinct need for a configuration subsystem that was able to handle more
complex configuration schemas.

The `application_properties` library has the following advnatages:

- Thoroughly tested
  - The project currently has over 65 tests and coverage percentages over 99%.
- Simple... With Examples
  - The package was created with the intention of being as easy to use as possbile.
  - To that extent, there are 4 basic usage examples and over 10 advanced usage examples.
- Complex When Required
  - xxx
- Hierarchically Aware
  - By default, uses the `.` in the key names to define levels of hierarchy, which can then
    be used to find only properties that exist under a given key.
  - If desired, the `ApplicationPropertiesFacade` object can restrict access to only those
    properties that exist under a given hierarchy.
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

### A Word On The Examples

This section on `How To Use This Package` provides easy to follow Python code snippets.
Each snippet is available as a complete Python script file in the project's
[examples directory](dd).  To ensure the integrity of each Python script,
the following three lines are present at the start of each Python file:

```Python
import os
import sys
sys.path.insert(0, os.path.abspath(os.getcwd()))  # isort:skip
```

This prefix allows our team to frequently execute these samples from the project's base
directory, on the watch for any changes in behavior.

For the sake of brevity, as those three lines are at the start of every
example file, their use is documented here and will remain absent from any
Python examples presented in the following sections.

### Example 01 - Get A String Property From An Empty Property Instance

The Python script for [Example 01](dd) illustrates the basics of using
the `application_properties` package.  This example imports the `ApplicationProperties`
class from the `application_properties` package, and then creates a new instance of
that class and assigns it to the `properties` variable.  Next, the examples prints
the result of calling the `get_string_property` for that new instance of the class,
requesting the value for the property named `my_property`.

```Python
from application_properties import ApplicationProperties

properties = ApplicationProperties()
print(properties.get_string_property("my_property"))
```

As there are no properties present in the instance, the output is predictably:

```text
None
```

## Example 02 - Get A String Property After Loading Json Data Into The Property Instance

For the purposes of this example, the [example data file](dd), `example_data.json`, contains
the following JSON object:

```json
{
    "my_property" : "test data"
}
```

The Python script for [Example 02](dd), takes the previous script and includes the
import for the `ApplicationPropertiesJsonLoader` loader. Then, after the declaration
and assignment of the `properties` instance, it calls the loader's `load_and_set`
function to load the data file into the `properties` instance:

```Python
from application_properties import ApplicationProperties, ApplicationPropertiesJsonLoader

properties = ApplicationProperties()
ApplicationPropertiesJsonLoader.load_and_set(
    properties, os.path.join(os.path.dirname(__file__), "example_data.json")
)
print(properties.get_string_property("my_property"))
```

As the data file contains a single key `my_property`, with the string value of
`test data` assigned to it.

```text
test data
```

However, `02a`  `my_other_property` to `my_other_property`.

```text
None
```

as the property name no longer matches the one property present in the data file.

## Example 03 - Get A String Property With A Default Value

Keeping with the theme of gradual changes to the examples, for
[Example 03](dd), the only change that was made to Example 02a was that
the call to `get_string_property` was modified to include a default value:

```Python
from application_properties import ApplicationProperties, ApplicationPropertiesJsonLoader

properties = ApplicationProperties()
ApplicationPropertiesJsonLoader.load_and_set(
    properties, os.path.join(os.path.dirname(__file__), "example_data.json")
)
print(properties.get_string_property("my_other_property", default="default value"))
```

This time, when the example is executed, no value is found for the property `my_other_property`,
but the `default` parameter allows the function to return something other than `None`:

```text
default value
```

## Example 04 - Property File Loader

TBD

## Advanced Examples

While the bulk of normal property file operations can be accomplished using information
from the above basic examples, more advanced examples are
[located here](dd).

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

Instructions For Contributing

Developer notes on various topics are kept in the the
[Developer Notes document](docs\developer.md).

If you attempting to contribute something to this project, please follow the steps outlined
in the [CONTRIBUTING.md file](CONTRIBUTING.md).
