# Quick Start: Required Fields & Validation

You have learned how to load configuration data into an `ApplicationProperties`
object and retrieve it using getter methods. Now, you will learn how to modify those
getters to handle edge cases when retrieving those properties.

## What You Will Learn

On this page, you will master the advanced retrieval capabilities of `ApplicationProperties`
by learning to:

- **Simplify** data retrieval by replacing verbose null-checks with `default_value`
  fallbacks for missing or invalid keys.
- **Enforce** mandatory configuration presence by setting `is_required=True` to
  ensure critical properties are never omitted.
- **Validate** data integrity on-the-fly using `valid_value_fn` callbacks to ensure
  retrieved values meet specific business rules.
- **Control** failure handling globally or per-call using `strict_mode` to decide
  whether invalid data raises exceptions or returns silent defaults.

## Quick Reference: Optional Parameters

<!-- pyml disable-num-lines 6 line-length-->
| Parameter&nbsp;Name&nbsp;&nbsp; | Category | Default | Description |
| :--- | :--- | :--- | :--- |
| `default_value` | Fallback | `None` | The value to return if the configuration key is **missing** or **invalid**. Note: Does not apply if the key exists but is set to `null`. |
| `is_required` | Mandatory Validation| `False` | If `True`, raises an error if the configuration key is missing or null. |
| `valid_value_fn` | Content Validation | `None` | A function to validate the retrieved value. Raises if validation fails. |
| `strict_mode` | Type Safety | `False` (or instance default) | If `True`, enforces strict type checking and allows validation errors to propagate. |

## Prerequisites

Since this page deals with modifying the getter methods introduced on the
[Quick Start: Configuration Getters](./getters.md) page, it is advisable to revisit
that page if you have any questions about the `ApplicationProperties` object
getter functions.

## Understanding `strict_mode`

Before diving into the specific parameters, it is crucial to understand `strict_mode`,
as it influences how all optional parameters behave.

### What is `strict_mode`?

By default, the `ApplicationProperties` getter methods are lenient. If a type mismatch
occurs (e.g., asking for an integer but finding a string), the getter method will
return the default value which by default is `None`.

The `strict_mode` changes this behavior. When enabled, the getter method will
**raise an error** if:

1. A type mismatch occurs (e.g., the config has `"1"` but you asked for an `int`).
2. A `valid_value_fn` validation fails.

### Enabling Global `strict_mode`

To enable strict mode for **all** getter methods in your instance, set it
during initialization:

```python title="snippet: Enable Global Strict Mode"
properties = ApplicationProperties('config.yaml', strict_mode=True)
```

With this setting, any getter method called on this `properties` object will automatically
fail if it encounters a type mismatch or a validation failure.

### Overriding `strict_mode` Per-Call

You can override the global setting for specific calls.
**The call-site argument always takes precedence** over the global instance setting.

```python title="snippet: Overriding Global Strict Mode"
# Force strict mode for a critical call, even if global is False
critical_value = properties.get_integer_property('critical-id', strict_mode=True)

# Disable strict mode for a non-critical call, even if global is True
optional_value = properties.get_string_property('optional-id', strict_mode=False)
```

## Modifying What The Getter Methods Return

The first version of our getter methods were very simple, simply
performing their required task of retrieving configuration items.  However,
as we used the getters more and more, we started seeing patterns in our getter usage
that were repetitive.  Previously, users had to repeat this pattern for every retrieval.
We folded these patterns into optional parameters to reduce boilerplate.

### The `default_value` Parameter

**Problem:** Handling missing properties often requires repetitive `if None` checks
scattered throughout your codebase, making the retrieval logic noisy and hard to
maintain.

**Solution:** Eliminate redundant `if None` checks by specifying a fallback value
directly in the getter call. This consolidates data retrieval and defaulting into
a single, readable line.

<!-- pyml disable-next-line no-duplicate-heading-->
#### Code Examples

```python title="snippet: Before"
# Option 1: Verbose if-check

my_value = properties.get_string_property('log-level')
if my_value is None:
    my_value = "INFO"

# Option 2: Short-circuiting (less performant for complex types)
my_value = properties.get_string_property('log-level') or "INFO"
```

```python title="snippet: After"
# Single-line retrieval with fallback
my_value = properties.get_string_property('log-level', 'INFO')
```

**Key Takeaway** This pattern aligns with standard Python practices found in `dict.get()`
and `os.getenv()`, reducing cognitive load by leveraging familiar paradigms.

### The `is_required` Parameter

**Problem:** In rare cases, a property is so critical that the application cannot
function without it. Previously, this required manually checking for `None` and
raising an error after every getter call.

**Solution:** Enforce mandatory configuration presence by passing `is_required=True`.
The getter now raises a `ValueError` if the key is missing, aligning with standard
Python practices like `argparse`.

<!-- pyml disable-next-line no-duplicate-heading-->
#### Code Examples

```python title="snippet: Before"
my_value = properties.get_integer_property('log-rotate-length')
if my_value is None:
    raise ValueError("The log-rotate-length property must be set.")
```

```python title="snippet: After"
# Single-line retrieval with fallback
my_value = properties.get_integer_property('log-rotate-length', is_required=True)
```

```text title="Standart Error"
ValueError: A value for property 'log-rotate-length' must be provided.
```

**Key Takeaway** This pattern aligns with standard Python practices found in `argparse`
and `os.environ['key']`, reducing cognitive load by leveraging familiar paradigms.

### The `valid_value_fn` Parameter

**Problem:** Before this feature, validating properties required repetitive `if`
checks after every retrieval, mixing validation logic with data retrieval logic.

**Solution:** Validate retrieved data against custom logic by passing a callback
function via `valid_value_fn`. If the callback raises an exception, the error propagates
or the default value is applied (see `strict_mode` above); otherwise, the validated
value is returned.

```python title="snippet: Before"
my_value = properties.get_string_property('log-level', 'INFO')
if my_value not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
    raise ValueError("bad log level")
```

```python title="snippet: After (With Validation Function)"
def validate_log_level(arg: str) -> str:
    """Validates that the log level is one of the accepted values."""
    # Note that for this example, the 'INFO' value was removed from the list
    # to avoid having to change the `sample.yaml` file.
    if arg not in ['DEBUG', 'WARNING', 'ERROR', 'CRITICAL']:
        raise ValueError("bad log level")
    return arg

# Usage
my_value = properties.get_string_property('log-level', valid_value_fn=validate_log_level, strict_mode=True)
```

```text title="Standard Error"
ValueError: The value for property 'log-level' is not valid: bad log level
```

### Real-World Validator Example

This behavior is most evident when using `valid_value_fn` with `strict_mode=True`.
Consider a case where you need to validate that a configuration value is a list
of file extensions, each starting with a dot:

```python title="snippet: Validator Example"
from typing import List, Any

def validate_file_extensions(value: List[str]) -> List[str]:
    """Validates that the value is a list of valid file extensions."""
    for extension in value:
        if not extension.startswith("."):
            raise ValueError(f"Extension '{extension}' must start with a dot")
        
        if len(extension) < 2:
            raise ValueError(f"Extension '{extension}' is too short")
            
    return value

# Configuration input (e.g., in config.yaml):
# allowed_extensions:
#   - .py
#   - .yaml
#   - .txt
```

Once created, we can then use it with a `get_string_list_property` getter as follows:

```python title="snippet: Using The Validator Example"
allowed_extensions = properties.get_string_list_property(
    'allowed_extensions', 
    valid_value_fn=validate_file_extensions, 
    strict_mode=True
)
```

In this example, `strict_mode=True` ensures that if `validate_file_extensions` raises
a `ValueError` or `TypeError`, it is propagated to the caller. Without `strict_mode`,
the getter would silently return the `default_value` (if provided) or `None`, masking
the validation failure.

## Advanced Behavior: Parameter Interactions

When using optional parameters together, their behavior is governed by `strict_mode`
and the source of the configuration value.

### `strict_mode` Influence on Validation

By default (`strict_mode=False`), validation errors from `valid_value_fn` are
**silently ignored**. Instead of raising an exception, the getter returns the `default_value`
(or `None` if no default is set).

To ensure validation failures raise an exception, you must enable `strict_mode`:

```python title="snippet: Global strict_mode with local override"
# Enable globally
properties = ApplicationProperties('config.yaml', strict_mode=True)

# Or enable per-call
value = properties.get_string_property(
    'my-key', 
    valid_value_fn=my_validator, 
    strict_mode=True  # Overrides global setting if needed
)
```

### `default_value` and `is_required`

The getter methods raise a `ValueError` if both of these parameters are provided
at the same time. This is because the `default_value` parameter provides a default
value if no configuration item was found, and the `is_required` parameter requires
the configuration item to be found.

### `null` vs `None` in Configuration

A common source of confusion is how `null` in the file types maps to Python values.

1. **YAML `null` vs Missing Key:**
    - If a key is **missing** from the YAML file, the getter treats it as if it
      were not provided.
    - If a key is present but set to `null` (e.g., `my_key: null`), the getter retrieves
      it as Python `None`.

2. **Impact on `default_value`:**
    - Since the key exists in the configuration (even with a `null` value), `default_value`
      is not applied, and the getter returns `None`.
    - If you want `default_value` to apply when the key is `null`, you must use
      `is_required=False` and handle `None` manually, or use `valid_value_fn` with
      `strict_mode=True` to raise an error.

3. **Impact on `is_required`:**
    - If `is_required=True` and the config value is `null` (Python `None`), the
      getter **does not** raise an error. This is because a value *was* provided
      (even if it is `None`).
    - To strictly require a non-null property, combine `is_required=True` with a
      `valid_value_fn` that checks for `None`.

For a deeper dive into this behavior, see the [Getters and Null](../custom.md#getters-and-null)
section in the Custom documentation.

## Next Steps

**Prerequisites For Going On:** If you followed along with the information in the
Quick Start guide, you have:

- **Applied** `default_value` fallbacks to handle missing or invalid configuration
  keys gracefully.
- **Enforced** mandatory configuration presence by marking specific keys with
  `is_required=True`.
- **Validated** retrieved values against custom business rules using `valid_value_fn`
  callbacks.
- **Controlled** global or per-call failure handling by toggling `strict_mode` for
  error propagation.

**Next**, in the Quick Start guide series:

- Use [Configuration Data Layering](./layering.md) to learn to use multiple configuration
data source and how they interact.

**If** you need some review, select one of the items below:

<!-- pyml disable-num-lines 6 line-length-->
| Quick Start Page | Description |
| -- | -- |
| [Quick Start: Introduction](./index.md) | Understand the package's architecture and find the right learning path for your needs. |
| [Quick Start: Installation](./installation.md) | Quickly install the package and confirm your environment is ready in under five minutes. |
| [Quick Start: Configuration Loaders](./loaders.md) | Load YAML, JSON, and TOML files in just two function calls — no manual parsing needed. |
| [Quick Start: Configuration Getters](./getters.md) | Safely access properties with automatic type handling and defaults. |
