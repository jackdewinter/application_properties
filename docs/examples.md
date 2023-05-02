# Examples

The examples in this section focus specifically on the simple secnarios, with more
examples for the other scenarios being available in the
[Advanced Examples document](https://github.com/jackdewinter/application_properties/blob/main/docs/advanced_examples.md).

## A Word On The Examples

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

## Example 01 - Get A String Property From An Empty Property Instance

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

## Example 02 - Get A String Property After Loading Json Data Into The Property Instance

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

## Example 03 - Get A String Property With A Default Value

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

## Example 04 - Simple Property File Loader

TBD

## Advanced Examples

As mentioned before, while the bulk of property accessing and loading operations
can be accomplished using information from the above basic examples, more advanced
examples are available in the
[Advanced Examples document](https://github.com/jackdewinter/application_properties/blob/main/docs/advanced_examples.md).
