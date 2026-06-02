# Quick Start: Configuration Getters

In the previous guide, you loaded configuration data into the `ApplicationProperties`
object. Now, you will learn to retrieve that data using getter functions.

## What You Will Learn

On this page, you will master the foundational technique for accessing configuration
data by learning to:

- **Retrieve** properties as scalar types (strings, integers, and booleans) using
  the dedicated getter methods.
- **Validate** configuration data by checking for missing keys or type mismatches
  and applying default values to handle `None` results robustly.
- **Manage** complex configuration items by retrieving native list structures and
  comma-separated strings as Python lists.
- **Apply** format-agnostic retrieval patterns, ensuring your Python code works
  identically across YAML, JSON, and TOML configurations.

## Prerequisites

The following sections on this page build off the examples that were created on
the [Quick Start: Configuration Loaders](./loaders.md) page.
For a full understanding of the `MultisourceConfigurationLoader` class, please review
the previous page.

Code blocks titled with `.py` or `.yaml` are full files. Code blocks titled with
`snippet:` are fragments to be integrated into existing files.

## Recap

On the last page, you created the `sample.yaml` file with the following contents:

```yaml title="sample.yaml" linenums="1"
log-level: "INFO"
log-file: mylog.log
log-rotate-length: 10000
```

In addition, we explored loading data using the `MultisourceConfigurationLoader`
class using the
`loaders_multisource.py` script introduced in the previous page's
[The Recommended Approach](./loaders.md#the-recommended-approach) section.
These two items are critical. This page builds directly on this foundation.

## Using Getters To Retrieve Configuration Items

The output from the `loaders_multisource.py` script reported that the properties
object contains three configuration items: `log-level`, `log-file`, and `log-rotate-length`.
However, this output lacks the specific details most applications require. What
most applications want is to know the values of those configuration items. That
is the express purpose of the getter functions.

The available getter functions are:

- `get_string_property`
- `get_boolean_property`
- `get_integer_property`
- `get_string_list_property`

## Basic Getters

The first three getter functions are the easiest to understand and grasp, as they
deal with retrieving properties using Python's built-in types.
This is possible because each of the configuration file formats
that the `application_properties` package natively supports can represent data as
the base types of: string, integer, and boolean.
While there are other types supported by the different configuration file formats,
these three are the
ones that are distinctly represented in each of the three formats. Therefore, the
`application_properties` package supports
retrieving configuration items in each of those formats.

> **Note on Validity:**
> The `application_properties` packages prioritizes robustness. Instead of throwing
> exceptions for invalid data, getters return `None` if the value cannot be converted
> or if the key is missing. We will explore how to handle these scenarios in detail
> later in this guide. For now, assume your properties match the types you are requesting.

To see how getters work in context, we can combine the loader setup and the getter
calls into a single script. Create a new file named `getters_scalar_types.py` in
your project directory. This file demonstrates the complete flow from loading configuration
to retrieving specific properties.

```python title="getters_scalar_types.py" linenums="1"
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader, ConfigurationFileType

# 1. Initialize the properties object and load the configuration file
#    using the same logic as previous page.
properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_specified_configuration_file(
    "sample.yaml",
    ConfigurationFileType.YAML,
)
if loader.process(properties):
    raise ValueError("Configuration loading failed")

# 2. Use Getters to retrieve specific configuration items.
print(f"log-level           = {properties.get_string_property('log-level')}")
print(f"log-rotate-length   = {properties.get_integer_property('log-rotate-length')}")
print(f"log-rotate-each-day = {properties.get_boolean_property('log-rotate-each-day')}")
```

When you run the script, it should now produce the following output:

```text title="standard output"
log-level           = INFO
log-rotate-length   = 10000
log-rotate-each-day = None
```

You've seen how getters retrieve properties. You may have noticed they can return
`None`. This isn't an error; it's a robust way to handle missing or invalid data.
Let's dive into the details of when and why this happens.

## Understanding Return Values: None, Defaults, and Errors

When using getters, it is critical to understand when a `None` return value occurs.
The package returns `None` in two primary situations: **Missing Keys** and
**Type Mismatches**. Distinguishing between these two is key to effective debugging.

### 1. Missing Keys (Structure Issue)

Returns `None` if the key is absent.

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Example Configuration (`sample.yaml`):**

```yaml title="snippet: Missing Key YAML"
log-level: "INFO"
# `log-rotate-length` is NOT defined
```

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Python Code:**

```python title="snippet: Missing Key Python"
length = properties.get_integer_property('log-rotate-length')
# Returns: None
# Reason: 'log-rotate-length' cannot be found
```

**How to Check:**
You can verify if a key exists before calling the getter using the `property_names`
list:

```python title="snippet: Verify Existence"
if 'log-rotate-length' in properties.property_names:
    length = properties.get_integer_property('log-rotate-length')
    if length is not None:
        print(f"Length is {length}")
    else:
        print("Key exists but value is invalid/missing")
else:
    print("Key does not exist in configuration")
```

### 2. Type Mismatches (Data Issue)

If the key exists but the value cannot be converted to the requested type, the getter
returns `None`.

**Example Configuration (`sample.yaml`):**

```yaml title="snippet: Type Mismatch YAML"
log-rotate-length: "not_a_number"
# `log-rotate-length` is defined as a string
```

**Python Code:**

```python title="snippet: Type Mismatch Python"
length = properties.get_integer_property('log-rotate-length')
# Returns: None
# Reason: 'not_a_number' cannot be cast to an integer
```

**How to Handle:**

The return value is `None` for both missing keys and type mismatches. You must check
for key existence first. If the key exists but the value is `None`, this indicates
a type mismatch.

> **Best Practice:** Always initialize your properties with defaults in your Python
> code to handle `None` gracefully. Here is an example:
>
> ```python title="snippet: Safe Getter"
> log_level = properties.get_string_property('log-level') or 'WARNING'
> ```

## String Lists

The scalar getters we have used thus far retrieve single properties, while real-world
configurations often require multiple items (e.g., file extensions). The package
handles string lists in two distinct ways: as **native list structures** (like YAML
arrays) or as **comma-separated strings**. The package normalizes both native arrays
and comma-separated strings into a single Python list object by parsing the raw
configuration data. To support this, the `ApplicationProperties` object provides
the `get_string_list_property` method. The `get_string_list_property` handles native
arrays and comma-separated strings differently. Native lists (YAML/JSON/TOML) are
handled automatically. Only legacy-style comma-separated strings require the `delimiter`
argument.

*Key Concept - Input Normalization:* Your Python code remains **consistent** regardless
of format. The `get_string_list_property` method automatically parses native list
structures (like YAML lists or JSON arrays). However, if your configuration value
is a **comma-separated string** (common in legacy properties files), you must explicitly
provide a delimiter argument. This tells the method exactly how to split the items.

> Use native lists for modern config files (YAML/JSON/TOML). Use comma-separated
> strings only when integrating with legacy systems and their properties files that
> do not support arrays.

### Basic Usage: Native List Structures

A native list is a structured array (like `[1, 2, 3]` in JSON or a YAML sequence),
whereas a comma-separated value is a single text string (like `'1, 2, 3'`).
The package automatically detects native array structures in modern formats and
returns a Python list. You can omit the `get_string_list_property` method's `delimiter`
parameter entirely for native lists.

Our recommended approach is to always use native list structures in your config
file for clarity and ease of use, unless there is a significant reason to fallback
to comma-separated string lists.

#### Example: YAML Block List

```yaml title="snippet: YAML Block List"
valid-extensions:
    - .json
    - .yml
    - .yaml
    - .toml
```

#### Example: YAML Flow List

```yaml title="snippet: YAML Flow List"
valid-extensions: [".json", ".yml", ".yaml", ".toml"]
```

### Updating the Script

To handle list data, update your existing `getters_scalar_types.py` script. Keep
the existing loader setup. Simply add the new import and the retrieval logic for
list properties.

<!-- pyml disable-next-line list-marker-space-->
1.  Add List Retrieval Logic

    Append the following code to the end of your script, after the existing scalar
    getter prints:

    ```python title="snippet: String List Support"
    # Retrieve the list of valid extensions
    valid_extensions = properties.get_string_list_property('valid-extensions')
    if valid_extensions is not None:
        print(f"valid-extensions    = {valid_extensions}")
    else:
        print("valid-extensions    = (not found or invalid)")
    ```

<!-- pyml disable-next-line list-marker-space-->
2.  Expected Output

    When you run the updated script, the output will now include the list:

    ```text title="standard output"
    log-level           = INFO
    log-rotate-length   = 10000
    log-rotate-each-day = None
    valid-extensions    = ['.json', '.yml', '.yaml', '.toml']
    ```

### Handling String-Based Lists

If your configuration file uses a **comma-separated string** (common in older YAML
or properties files), the package treats the complete string as a single string
property **by default**. To convert this into a list, you must provide a `delimiter`
argument to the `get_string_list_property` method so the package knows which character
separates the items. Note that this argument is ignored automatically if the configuration
value is already a native list or array.

For example, given the following YAML snippet:

```yaml title="snippet: YAML String List"
valid-extensions: ".json,.yml,.yaml,.toml"
```

update your code as follows:

```python title="snippet: String List Python"
print(f"Valid extensions: {properties.get_string_list_property('valid-extensions', delimiter=',')}")
```

This correctly parses the string into a list.

> **Note:** The second argument has **no effect** on native list structures (like
> the ones shown above). It is only used when parsing string values that contain
> separator characters.

### Format Compatibility Summary

The `application_properties` package handles multiple ways to define lists in your
configuration files. You do not need to change your Python code when switching between
these formats.

<!-- pyml disable-num-lines 4 line-length-->
| Config Structure | Example Value (YAML) | Required Python Argument | Notes |
| :--- | :--- | :--- | :--- |
| **Native List** (Recommended) | `extensions: [.json, .yml]` | None | Library handles parsing automatically. |
| **Comma-Separated String** | `extensions: ".json,.yml"` | `delimiter=','` | Only used if the value is a single string with separators. |

## Format Agnostic Configuration

The `application_properties` package abstracts the differences between configuration
formats. You do not need to change your Python code when switching between YAML,
JSON, or TOML, provided the structure of the data remains consistent.

### Configuration File Examples

Below are the equivalent configurations for valid-extensions in each supported format.
Note that all three formats support native list structures natively.

<!-- pyml disable-num-lines 6 no-inline-html-->
<!-- pyml disable-num-lines 5 line-length-->
| Format | File Name | Content |
| :--- | :--- | :--- |
| YAML | sample.yaml | valid-extensions:<br> - .json<br> - .yml<br> - .yaml<br> - .toml<br> |
| JSON | sample.json | {<br> "valid-extensions": [".json", ".yml", ".yaml", ".toml"]<br>}<br> |
| TOML | sample.toml | valid-extensions = [ ".json", ".yml", ".yaml", ".toml" ]<br> |

### Unified Python Implementation

This script demonstrates the complete workflow: loading configuration from any supported
format (YAML, JSON, or TOML) and retrieving a list property. The key benefit of
this library is that the **Python code remains identical** regardless of the configuration
file format.

```python title="getters_string_list_unified.py" linenums="1"
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader, ConfigurationFileType

# 1. Initialize the properties object and loader
properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()

# 2. Add your configuration file
#
# NOTE: Only this block changes between formats. 
# The getter call in Step 3 remains identical.
#

# Option A: YAML
loader.add_specified_configuration_file(
    "sample.yaml",
    ConfigurationFileType.YAML,
)

# Option B: JSON
# loader.add_specified_configuration_file(
#     "sample.json",
#     ConfigurationFileType.JSON,
# )

# Option C: TOML
# loader.add_specified_configuration_file(
#     "sample.toml",
#     ConfigurationFileType.TOML,
# )

if loader.process(properties):
    raise ValueError("Configuration loading failed")

# 3. Retrieve the configuration item
# This line works identically for YAML, JSON, and TOML because the package
# normalizes the input data into a standard Python structure.
valid_extensions = properties.get_string_list_property('valid-extensions')

if valid_extensions is not None:
    print(f"Valid extensions: {valid_extensions}")
else:
    print("Configuration item 'valid-extensions' not found or invalid.")
```

> Notice that only the **filename** and **`ConfigurationFileType`** in step 2 change
> between formats. The getter call in step 3 never needs to change. This is the
> core advantage of using `application_properties`.

### Expected Output

Regardless of whether you use `sample.yaml`, `sample.json`, or `sample.toml`, the
output will be:

```text title="standard output"
Valid extensions: ['.json', '.yml', '.yaml', '.toml']
```

## Next Steps

**Prerequisites For Going On:** If you followed along with the information in the
Quick Start guide, you have:

- **Retrieved** scalar properties like strings, integers, and booleans using type-specific
  getter methods.
- **Parsed** complex list configurations into Python lists, handling both native
  arrays and comma-separated strings.
- **Handled** missing or invalid data robustly by checking for `None` results and
  applying default values.
- **Wrote** configuration code that remains identical regardless of whether the
  underlying file is YAML, JSON, or TOML.

**Next**, in the Quick Start guide series:

- Use [Quick Start: Required Fields & Validation](./validation.md) to enforce required
  fields and catch configuration errors at startup — before your application is
  impacted.

**If** you need some review, select one of the items below:

<!-- pyml disable-num-lines 5 line-length-->
| Quick Start Page | Description |
| -- | -- |
| [Quick Start: Introduction](./index.md) | Understand the package's architecture and find the right learning path for your needs. |
| [Quick Start: Installation](./installation.md) | Quickly install the package and confirm your environment is ready in under five minutes. |
| [Quick Start: Configuration Loaders](./loaders.md) | Load YAML, JSON, and TOML files in just two function calls — no manual parsing needed. |
