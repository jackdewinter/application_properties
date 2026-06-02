# Quick Start: Type Inference For Manual Properties

The `application_properties` package has great support for loading configuration
items from different configuration data sources and a solid collection of getter
functions
to retrieve the values contained within. And that type safety is great for configuration
data sources that support typed values, such as the JSON, TOML, and YAML formats.
But what about other formats that do not support typed values, such as passing
`key-value` pairs from the command line via the `add_manually_set_properties` function?
How does the `application_properties` package handle those values?

That is what this page in our Quick Start series addresses: inferring
configuration item types using string prefixes.

## What You Will Learn

On this page, you will master the techniques for inferring configuration types in
untyped data sources by learning to:

- **Identify** scenarios where configuration values are passed as raw strings and
  require type inference to function correctly with your application logic.
- **Define** explicit type hints by embedding specific string prefixes
  (e.g., `$$`, `$#`, `$!`) into your manual property values to force specific data
  types.
- **Configure** the `ApplicationProperties` instance to use automatic fallback translation,
  enabling the system to infer types from raw strings when explicit prefixes are
  absent.

## Prerequisites

This Quick Start guide builds upon the foundations established on the
[Quick Start: Configuration Loaders](./loaders.md),
[Quick Start: Configuration Getters](./getters.md), and
[Quick Start: Configuration Data Layering](./layering.md) pages.
If you do not feel like you have a good grasp of the information and examples provided
on that page, please take the time to go back and review that information now.

## Properly Defining the Problem

The problem itself is defined as this. While many of our configuration data sources
provide type information that guides the application in deciding which of the four
`ApplicationProperties` "getter" functions to use,
there are some that do not provide that information.

The most obvious example is the passing `key-value` pairs from the command line
into the `add_manually_set_properties` function.
That function accepts a list of zero or more strings in the `key=value` format and
is comparable to using the
`set_manual_property` of the `ApplicationsProperties` object. Since both of these
functions only deal with lists of
strings, how do we move from a plain string to a typed property?

For instance, consider a script that retrieves command-line arguments via a call
to `sys.argv`. You can pass the modified list (excluding the script path at
index 0) directly to the `add_manually_set_properties` method. As each element in
the list is a string, each value assigned to a configuration item will therefore
be a string. For the resultant property to be anything else other than a string,
some form of translation has to be performed, either
an explicitly requested translation or an implicit translation as a backup.

That is what the two options are: embedding type hints in the string to explicitly
ask for a translation, or an implicit translation if the value is not already of
the type requested by the getter function.

## Embedded Type Hints

The first of these options is for the string to contain some manner of embedded
prefix that lets the
user communicate the intended type of the property. To keep things simple, when
a string value is passed
in through the `add_manually_set_properties` method, a quick check is made to see
if that string starts
with the `$` character. If so, the function then looks at its equivalent of the
following table
to determine the inferred type:

| Prefix | Type | Examples |
| --- | --- | --- |
| `$*` (except for characters below) | Default (String) | `$abc` |
| `$$` | String | `$$abc` |
| `$#` | Integer | `$#1`, `$#-12345` |
| `$!` | Boolean | `$!True`, `$!anything-else-is-false` |

While this may seem messy, it handles the problem of communicating the type information
in a compressed manner.
With only two extra characters added to a string, that string can now indicate that
it should be handled as
an integer type or as a boolean type.

### Examples

Following the `log` section examples from our last page,
[Quick Start: Configuration Hierarchy](./hierarchy.md),
lets show how to set some of the values in that section using embedded type hints.
To make this example more
complete, we will assume that there is a boolean configuration item, `log.show-stack-trace`,
that controls
whether any stack traces will be shown if exceptions are logged.

Precisely, we will set the following values to give examples of each type in the
above table:

| Name | Type | Value | XX String |
| --- | --- | --- | --- |
| `log.level` | string | `INFO` | `log.level=INFO` |
| `log.rotate-length` | integer | `10000` | `log.rotate-length=$#10000` |
| `log.show-stack-trace` | boolean | `True` | `log.show-stack-trace=$!True` |

After obtaining these values, usually by having them present on the command line,
they still have to
be loaded.  This is the job of the `add_manually_set_properties` method from the
`MultisourceConfigurationLoader` class.
This method accepts an optional list of strings, with each string being its own
`key=value` entry.

To demonstrate this, we build upon the basic setup established in the
[Configuration Loaders guide](./loaders.md#the-recommended-approach)

<!-- pyml disable-num-lines 2 no-inline-html-->
<details>
<summary>Click to see the Base Setup (from previous guide)</summary>

```python title="loaders_multisource.py" linenums="1"
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader, ConfigurationFileType

properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_specified_configuration_file(
    "sample.yaml",
    ConfigurationFileType.YAML,
)
if loader.process(properties):
    raise ValueError("Configuration loading failed")
```

</details>

and replace the other `loader.add_` calls with a single `add_manually_set_properties`
call to arrive at the following script:

```python title="manual_embedded.py" linenums="1"
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader, ConfigurationFileType

properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_manually_set_properties([
    'log.level=INFO',
    'log.rotate-length=$#10000',
    'log.show-stack-trace=$!True',
    ])
if loader.process(properties):
    raise ValueError("Configuration loading failed")

print(f"log.level               = {properties.get_string_property('log.level')}")
print(f"log.rotate-length       = {properties.get_integer_property('log.rotate-length')}")
print(f"log.show-stack-trace    = {properties.get_boolean_property('log.show-stack-trace')}")
```

When executed, it produces the following output:

```text title="standard output"
log.level               = INFO
log.rotate-length       = 10000
log.show-stack-trace    = True
```

This shows that while the values being passed into the `add_manually_set_properties`
call are strings,
they are successfully translated into values that can be accessed by the usual getter
methods.

> NOTE: In that example, we fed those values in directly to the `add_manually_set_properties`
> method. If you are retrieving these values from the command line, you must carefully
> handle the encasing of your command line values in single quotes (`'`) or
> double quotes (`"`), escaping any necessary values.

Embedded type hints require you to modify the input strings themselves. This works
perfectly for command-line arguments or data you generate within your application.
However, if you are integrating with a **legacy system**, a **third-party API**,
or a **database** that returns raw strings which you **cannot modify**, you cannot
add the `$#` or `$!` prefixes.

In these scenarios, embedded hints are impossible to use. Instead, you need a way
to tell the `ApplicationProperties` instance: *'I don't control the input format,
but I trust that most of these strings can be converted to their correct types.'*
This is exactly what Getter Function Translation provides.

### Getter Function Translation

The second option is to allow the getter functions to translate the values when
a type mismatch occurs. This is enabled by setting the
`convert_untyped_if_possible` parameter to `True` when passed during initialization
to the `ApplicationProperties` instance. This setting acts as a **fallback** mechanism
for any configuration source that does not provide explicit type information (such
as standard YAML or JSON files). It does not override types that are already explicitly
defined in your configuration data.

<!-- pyml disable-next-line no-emphasis-as-heading-->
> **Important: Precedence Rules**
>
> When both methods are available, **embedded type hints always take precedence**
> over the `convert_untyped_if_possible` fallback.
>
> - If a value contains a prefix (e.g., `$#10000`), that prefix is parsed first.
> - The fallback translation is only triggered if **no** prefix is present AND the
>   retrieved string type does not match the requested getter type.

Using the
previous `manual_embedded.py` as a template, we can create the file `manual_translation.py`
and change the lines in the middle to:

```python title="manual_translation.py" linenums="1"
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader, ConfigurationFileType

properties = ApplicationProperties(convert_untyped_if_possible=True)
loader = MultisourceConfigurationLoader()
loader.add_manually_set_properties([
    'log.level=INFO',
    'log.rotate-length=10000',
    'log.show-stack-trace=True',
    ])
if loader.process(properties):
    raise ValueError("Configuration loading failed")

print(f"log.level               = {properties.get_string_property('log.level')}")
print(f"log.rotate-length       = {properties.get_integer_property('log.rotate-length')}")
print(f"log.show-stack-trace    = {properties.get_boolean_property('log.show-stack-trace')}")
```

> Note that unlike embedded type hints which apply only to individual values, `convert_untyped_if_possible`
> is an instance-level setting. Once enabled, it applies to all property retrievals
> on this `ApplicationProperties` object for its lifetime.

When executed, it produces the following output, just like the previous example:

```text title="standard output"
log.level               = INFO
log.rotate-length       = 10000
log.show-stack-trace    = True
```

But why isn't this on by default? It is because setting that flag to `True` introduces
complexity.

By having each getter method only render the property if the types match, the
getter methods are kept simple and predictable: if you want a property to be retrieved
as an integer,
it must be specified as an integer. Even though the input method changes from configuration
files
to a Python list of strings, that statement still holds for strings passed to the
`add_manually_set_properties`
method with embedded type hints.

However small, that logic changes if you enable getter function translation with
the `convert_untyped_if_possible` parameter.
That one property can now be set as an integer (`10000`) or a string (`'10000'`).
True, it is a small
difference, but it does introduce more complexity.

## Next Steps

**Prerequisites For Going On:** If you followed along with the information in the
Quick Start guide, you have:

- **Identify** the specific need for type inference when manual properties are
  passed as raw strings.
- **Apply** string prefixes like `$$`, `$#`, and `$!` to explicitly enforce the
  intended data types.
- **Enable** the `convert_untyped_if_possible` option to automatically translate
  untyped values across the entire instance during runtime.
- **Recognize** that explicit embedded prefixes always take precedence over any
  automatic fallback translation of values.

**Wrap-up:**

During these Quick Start guides, we have endeavored to teach you the basics of how
to use
the `application_properties` package. We have tried to provide both solid examples
that
you can execute for yourself, wrapped with solid sections to assist you in learning
why those examples work. By performing both of these tasks together, we hope that
it
has provided you with the information you need to incorporate the `application_properties`
package into your next Python project.

**If** you need some review, select one of the items below:

<!-- pyml disable-num-lines 10 line-length-->
| Quick Start Page | Description |
| -- | -- |
| [Quick Start: Introduction](./index.md) | Understand the package's architecture and find the right learning path for your needs. |
| [Quick Start: Installation](./installation.md) | Quickly install the package and confirm your environment is ready in under five minutes. |
| [Quick Start: Configuration Loaders](./loaders.md) | Load YAML, JSON, and TOML files in just two function calls — no manual parsing needed. |
| [Quick Start: Configuration Getters](./getters.md) | Safely access properties with automatic type handling and defaults. |
| [Quick Start: Required Fields & Validation](./validation.md) | Enforce required fields and catch configuration errors at startup — before your application is impacted. |
| [Quick Start: Configuration Data Layering](./layering.md) | Merge multiple configuration sources, letting environment-specific values automatically override defaults. |
| [Quick Start: Configuration Hierarchy](./hierarchy.md) | Organize nested settings like a file system, enabling easy access via dot-path queries (e.g., `app.server.port`). |
| [Quick Start: Type Inference For Manual Properties](./manual.md) | Prevent silent bugs using strict type casting and automatic type conversion (e.g., strings to ints) for manually defined properties. |
