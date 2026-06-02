# Quick Start: Configuration Loaders

The `application_properties` package provides the `ApplicationProperties` class.
This class acts as a central, dictionary-like store for your application's configuration
data.

An instance of the `ApplicationProperties` class requires data to be useful. For
conceptual purposes, consider an `ApplicationProperties` object as an empty container.
In practice, you will populate it using the methods described below.

## What You Will Learn

On this page, you will learn to manage configuration data using the `application_properties`
package by learning to:

- **Populate** configuration data directly in memory using `key-value` pairs or
  dictionaries for simple, static use cases.
- **Assess** the maintenance limitations of manual loading strategies, specifically
  the code volume required to support multiple file formats.
- **Configure** a `MultisourceConfigurationLoader` instance to handle YAML, JSON,
  and TOML files with minimal code.
- **Validate** the configuration data by executing the loader and verifying the
  resulting property names in the `ApplicationProperties` object.

## Prerequisites

The following sections assume that you have already installed the `application_properties`
package
and have verified that it is installed.

Place the following files (provided in later sections) in your project root:

- Scripts (e.g., `loaders_manual_example.py`)
- Configuration files (e.g., `sample.yaml`)"

Create a configuration file named `sample.yaml` in your project root with the
following contents:

```yaml title="sample.yaml" linenums="1"
# Format: key: value
log-level: "INFO"
log-file: mylog.log
log-rotate-length: 10000
```

This `sample.yaml` configuration file will be used by Python examples on
this page.

## Manual Loading Methods and Limitations

Direct population works for simple configurations. However it requires increasing
code management costs in larger projects where
multiple configuration file types are supported. Let's look at the manual approach,
measure the number of source code lines required for each added file type support
in manual loading implementations.

### Simple Key-Value And Dictionary Loading

For simple configurations, you can populate `ApplicationProperties` directly using
one of two methods:

| Method | Best For | Complexity |
| :--- | :--- | :--- |
| `set_manual_property` | Simple string `key-value` pairs | Minimal |
| `load_from_dict` | Complex structures (mixed types) | Moderate |

**Combined Example:**

```python title="loaders_manual_example.py" linenums="1"
from application_properties import ApplicationProperties

properties = ApplicationProperties()

# Method 1: loading via simple `key-value` strings
simple_config = [
    "log-level=INFO",
    "log-file=myapp.log"
]
properties.set_manual_property(simple_config)

# Method 2: loading a complex dictionary with mixed types
complex_config = {
    "log-rotate-length": 10000,  # Integer
    "log-rotate-enabled": True   # Boolean
}
properties.load_from_dict(complex_config)

print(properties.property_names)
# Output: ['log-level', 'log-file', 'log-rotate-length', 'log-rotate-enabled']
```

Manual loading (using the `set_manual_property` or `load_from_dict` method) has
a key limitation: it cannot externalize configuration data. As a result, updating
settings requires modifying the source code directly. For a detailed breakdown of
these limitations compared to automatic loading, see the
[Loading Strategy Comparison](#loading-strategy-comparison).

Manual loading is suitable for simple cases but becomes repetitive and error-prone
as configuration size increases.

### Limitations of File-Based Manual Loading

To load a YAML file type manually, you need to:

1. Install a parser package, if not already there (e.g., `pip install pyyaml`).
2. Import a YAML parser (e.g., `import yaml`).
3. Open and read the configuration file.
4. Parse the content into a dictionary.
5. Load the dictionary into the `ApplicationProperties` object.
6. Handle any errors that were raised during the previous steps.

```python title="loaders_manual_file.py" linenums="1"
# 17 non-empty, non-comment lines of repetitive setup for 1 file
import yaml
from application_properties import ApplicationProperties

properties = ApplicationProperties()

try:
    # Step 1 & 2: Open and read
    with open("sample.yaml", "r") as f:
        data = yaml.safe_load(f)  # Step 3: Parse
    
    if data is None:
        raise ValueError("Configuration file is empty")
        
    # Step 4: Load into properties
    properties.load_from_dict(data)
    
except FileNotFoundError:
    print("Error: Configuration file 'sample.yaml' not found.")
except yaml.YAMLError as e:
    print(f"Error: Failed to parse YAML: {e}")
except ValueError as e:
    print(f"Error: Invalid configuration data: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

**This implementation requires 17 lines of code just to load one file. The code
footprint grows linearly with each supported file type.**

Because every file type requires new imports and error handling, manual scripts
become difficult to maintain as the project grows.

Review the next section to see how code volume increases to 25+ lines when adding
JSON and TOML support with just basic error handling.

### Scaling To Multiple File Types

Helper functions often fail to simplify this process. Each file type requires a
distinct parsing library, forcing you to duplicate error handling and import statements
across multiple helper functions.

Adding JSON and TOML support to the manual loading approach increases complexity
as shown below:

```python title="loaders_mixed_manual_load.py" linenums="1"
import yaml
import json
import toml
from application_properties import ApplicationProperties

properties = ApplicationProperties()

# --- YAML Loading ---
try:
    with open("config.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)
    if yaml_data:
        properties.load_from_dict(yaml_data)
except Exception as e:
    print(f"YAML error: {e}")

# --- JSON Loading (Repeat of Similar Logic) ---
try:
    with open("settings.json", "r") as f:
        json_data = json.load(f)
    if json_data:
        properties.load_from_dict(json_data)
except Exception as e:
    print(f"JSON error: {e}")

# --- TOML Loading (Repeat Again) ---
try:
    with open("app.toml", "r") as f:
        toml_data = toml.load(f)
    if toml_data:
        properties.load_from_dict(toml_data)
except Exception as e:
    print(f"TOML error: {e}")
```

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Maintenance Burden**

- **3 Different Imports:** `yaml`, `json`, `toml`.
- **3 Duplicate `try/except` blocks:** Nearly identical structure.
- **3 `load_from_dict` calls:** Repetitive code.

This repetition increases code size. Additionally, it multiplies the surface area
for bugs every time a file format or error handling strategy changes.
Finally, it raises the risk of copy-paste errors in error handling logic itself.

In the next section, we show how a `MultisourceConfigurationLoader` instance class
consolidates the file loading functions in the previous example
using a simple, easy-to-use interface.

## The Recommended Approach

The `application_properties` package provides the `MultisourceConfigurationLoader`
class to consolidate parsing logic into a single, consistent interface.
The setup required to use the `MultisourceConfigurationLoader` class is reduced
to just 4 lines of code. This contrasts with the 20+ lines of code required to support
loading just one configuration file format with proper error handling.

The `MultisourceConfigurationLoader` class manages underlying parsers for three
configuration file types. By hiding file type complexities, this abstraction allows
you to focus on configuration data rather than parsing mechanics.

Create `loaders_multisource.py` in your project root (alongside `sample.yaml` and
`loaders_manual_example.py`) with the following content.
Explicitly pass `ConfigurationFileType.YAML` to prevent runtime errors. The package
cannot always infer the file type from the extension alone (e.g., if the file is
named config without an extension).

```python title="loaders_multisource.py" linenums="1"
# 3 lines of setup for 1 file with approximately 3 lines of added setup for each new file type
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import (
    MultisourceConfigurationLoader,
    ConfigurationFileType,              # Enum: JSON, YAML, TOML
)

properties = ApplicationProperties()
loader = MultisourceConfigurationLoader()
loader.add_specified_configuration_file(
    "sample.yaml",
    ConfigurationFileType.YAML,         # <--- Always specify for reliability
)

# process() returns True if an error occurred, False if successful
if loader.process(properties):
    raise ValueError("Configuration loading failed")

print(f"property_names  = {properties.property_names}")
```

The process consists of these steps:

1. **Initialize:** Create an instance of the `MultisourceConfigurationLoader` class.
2. **Add Source:** Call `add_specified_configuration_file()` with the filename and
   `ConfigurationFileType.YAML` enum value.
3. **Execute:** Call `process()` to load the data into an `ApplicationProperties`
   object. Check the return value of the `process()` method. If it returns `True`,
   an error occurred; if it returns `False`, the load was successful.

Using the `sample.yaml` that you created in the same directory as your Python script,
execute the script with `python loaders_multisource.py`. Running `python loaders_multisource.py`
produces the following standard output:

```text title="standard output"
property_names  = ['log-level', 'log-file', 'log-rotate-length']
```

Compare the error handling lines in the manual loading examples versus the 4 lines
of code required for the `MultisourceConfigurationLoader` class to load a single
configuration file.

To address any concerns about whether error handling is properly handled, temporarily
replace the contents of `sample.yaml` with the content `{{invalid: yaml` and re-run
the script. This will cause `process()` to return `True`, triggering the `ValueError`
and preventing the script from continuing with incomplete configuration data.

For JSON, YAML, and TOML, the `MultisourceConfigurationLoader` class provides a
consistent, minimal interface to load data into an `ApplicationProperties` object.

## Loading Strategy Comparison

> **Key Takeaway** Most applications should use the `MultisourceConfigurationLoader`
> class. Reserve manual loading for niche scenarios like testing or simple scripts.

Here is a comparison of the three strategies to help you decide which technique
fits your needs.

<!-- pyml disable-num-lines 8 no-inline-html-->
<!-- pyml disable-num-lines 8 line-length-->
| Feature | `set_manual_property` | `load_from_dict` | `MultisourceConfigurationLoader` |
| :--- | :--- | :--- | :--- |
| *Best For* | Ad-hoc, single values | In-memory config for tests/scripts | Real apps, configuration file-based config |
| *Input Source* | Code strings | Python Dictionary | YAML, JSON, TOML file types<br>(more information [later](./layering.md)) |
| *Extensibility* | Hard | Hard | Easy |
| *External Dependencies* | Manual | Manual | Built-in |
| *Validation* | None | None | Yes (format-aware)\* |
| *Limitations* | Static configuration only | Static configuration only | Requires dependency on file parser libraries (e.g., PyYAML) |

\* Validation ensures that the file is valid YAML/JSON/TOML before parsing, preventing
`None` values from polluting your configuration items.

**When to Use Each Method:** -- "Does your configuration need to change without
modifying your code?"

- **Yes**: If your configuration needs to change without modifying code, use the
  `MultisourceConfigurationLoader` class to externalize settings.
- **No:** If your configuration is static, derived from the environment, or only
  needed for ephemeral test runs, use `set_manual_property` or `load_from_dict`.

The `ApplicationProperties` object is now populated with data from `sample.yaml`.
The next step is accessing this data using the package's getter methods. Next, we
need to explore the equally important second part of the `application_properties`
package: getting information from that object.

## Next Steps

**Prerequisites For Going On:** If you followed along with the information in the
Quick Start guide, you have:

1. **Manually populated** configuration data using `set_manual_property` and `load_from_dict`.
2. **Identified** the maintenance burden of manual parsing for multiple file types.
3. **Implemented** a `MultisourceConfigurationLoader` to load YAML files with minimal
   code.
4. **Verified** the loaded configuration by inspecting the `ApplicationProperties`
   property names.

**Next**, in the Quick Start guide series:

- Use [Quick Start: Configuration Getters](./getters.md) to safely access properties
  with automatic type handling and defaults.

**If** you need some review, select one of the items below:

<!-- pyml disable-num-lines 4 line-length-->
| Quick Start Page | Description |
| -- | -- |
| [Quick Start: Introduction](./index.md) | Understand the package's architecture and find the right learning path for your needs. |
| [Quick Start: Installation](./installation.md) | Quickly install the package and confirm your environment is ready in under five minutes. |
