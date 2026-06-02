# Quick Start: Configuration Hierarchy

For simple applications with fewer than ten configuration items, flat configuration
files are often sufficient. However, as your application grows, relying on a flat
list of keys becomes increasingly difficult to manage. Without logical grouping,
it is easy to encounter naming conflicts, overlook related settings, or struggle
to locate specific parameters in a long list of unstructured data.

This is where **hierarchy** becomes essential. By organizing configuration items
into logical groups, you create a clear structure that improves maintainability,
prevents key collisions, and makes the configuration file significantly easier for
both developers and users to navigate.

## What You Will Learn

On this page, you will master the structural organization of configuration files
by learning to:

- **Evaluate** flat configuration keys to identify logical groupings that reduce
  cognitive load and prevent naming collisions.
- **Design** a hierarchical structure adhering to principles of shallow depth and
  explainability to ensure maintainability.
- **Implement** this hierarchy across YAML, JSON, and TOML formats, including the
  specific syntax required for `pyproject.toml`.
- **Access** nested configuration values in Python using simple dot-notation strings,
  bridging the gap between file structure and API usage.

## Prerequisites

This Quick Start guide builds upon the foundations established on the
[Quick Start: Configuration Loaders](./loaders.md)
and [Quick Start: Configuration Getters](./getters.md) pages.
If you are new to those concepts, please review them before continuing.

## Why Hierarchy Matters

Hierarchy is often mistaken for mere aesthetics, but its primary value is functional:
**reducing cognitive load** and **preventing naming collisions**.

<!-- pyml disable-next-line no-emphasis-as-heading-->
1. **Reducing Cognitive Load**

    Good organization provides structured categories for your brain to classify
    information efficiently. By grouping related settings, you reduce the mental
    effort required to scan and locate specific configuration items. For example,
    seeing a `log` group immediately signals that `level` and `file` are related
    to logging, rather than searching through a flat list of unrelated keys.

<!-- pyml disable-next-line no-emphasis-as-heading-->
2. **Preventing Naming Collisions**

    Without hierarchy, configuration keys are flat and prone to conflicts. For instance,
    a database configuration might use `host` and `port`, while a web server configuration
    also uses `host` and `port`. In a flat structure, you might end up with `db_host`,
    `db_port`, `web_host`, and `web_port`, which is hard to scan and maintain.

    Hierarchy solves this by grouping related settings under a common namespace,
    allowing you to use simple, descriptive keys like `host` within each group without
    risk of collision.

## Reviewing Current Configuration

In the last page on [Quick Start: Configuration Data Layering](./layering.md), we
used two configuration files to demonstrate how later-loaded files overwrite earlier
values:

- `sample.yaml` **(Base Configuration):** Contains default settings for logging
  and system behavior.
- `other-sample.yaml` **(User Overrides):** Simulates a user-specific configuration
  that overrides specific base values.

Here are the original contents of those files:

```yaml title="sample.yaml"  linenums="1"
log-level: "INFO"
log-file: mylog.log
log-rotate-length: 10000
valid-extensions: ".json,.yml,.yaml,.toml"
```

and the `other-sample.yaml` file:

```yaml title="other-sample.yaml"  linenums="1"
log-level: "DEBUG"
something-else: 42
```

While these files are sufficient for providing the five configuration items that
they represent
(note that log-level is common to both files), they fail to clearly indicate their
relationship. This repetition indicates a logical grouping that should be reflected
in the structure of the configuration file.

## Design Guidelines

> **Note:** The specific file changes described in this section were originally
> introduced in the [Adding Grouping to the Configuration Files](#adding-grouping-to-the-configuration-files)
> section. This section expands on the logic behind those changes.

Configuration structures should be logical and clearly communicable to users. In
the previous step, we organized our settings into `log` and `system` groups. The
following design principles guided these decisions:

1. **Logical Cohesion:** Group items by function (`log`, `system`) rather than data
   type. This makes it easier to find all related settings in one place.
2. **Shallow Depth:** Avoid unnecessary nesting. This keeps the configuration file
   shallow and easy to scan.
3. **Explainability:** A good hierarchy allows you to clearly tell users, "All logging
   settings are under `log`," which aids onboarding.
4. **Simplicity:** This guideline balances against **Shallow Depth**. Prioritize
   code clarity and user explainability over rigid adherence to nesting depth.

## Adding Grouping to the Configuration Files

Before looking at the internal mechanics, it helps to understand the primary benefits:
**organization and collision avoidance**.

Consider our previous flat configuration. We had `log-level` and `log-file` scattered
among other keys. Grouping related settings under `log` and `system` transforms
flat keys into nested namespaces. While the file structure is now nested, the access
key remains flat and dot-separated.

The `application_properties` package handles translation automatically, so nested
groups improve file readability. You still access these items in Python using a
flat, dot-separated key. This approach keeps the API simple, even though the underlying
file structure is organized.

Now that we've identified the confusion caused by flat keys across multiple files,
let's see how hierarchy solves this by consolidating our settings into a single,
structured source. This eliminates the need to track which value overrides which
in separate files. In addition, to demonstrate that this hierarchical structure
is format-agnostic and not tied to YAML's indentation, we can map the same structure
directly into JSON and TOML formats. This shows that the organization principle
holds regardless of the file type you choose.

## Applying the Transformations to our YAML Files

Below is our take on how the previous YAML configuration would look in a combined
YAML file. To create this unified file, we merged the keys from `sample.yaml`
and `other-sample.yaml` into a single hierarchical structure, while restructuring
the data from a flat hierarchy into a nested hierarchy to take advantage of grouping.

> You might notice that `log.rotate-each-day` is missing from the new `all-sample.yaml`
> file below. This is intentional; the package uses a default value for this key
> if it is not found in the file. By doing this, the `application_properties` package
> allows you to access configuration items that are **not** present in your files.
>
> This behavior is detailed in the [Quick Start: Required Fields & Validation](./validation.md#the-default_value-parameter)
> document.

The merged file, `all-sample.yaml`, looks like this:

```yaml title="all-sample.yaml"  linenums="1"
log:
  level: "DEBUG"
  file: mylog.log
  rotate-length: 10000
system:
  extensions: ".json,.yml,.yaml,.toml"
  something-else: 42
```

In the `all-sample.yaml`, notice how `log-level` from `sample.yaml` is now nested
under `log:`. This visual grouping immediately clarifies that `level`, `file`, and
`rotate-length` are related, solving the collision issue we saw with `db_host` vs
`web_host` earlier in the [Why Hierarchy Matters](#why-hierarchy-matters) section.

### Translating to JSON and TOML

If you prefer to use JSON or TOML formats instead of YAML, the hierarchical structure
maps directly.

For example, the above structure easily translates directly into JSON. Notice how
the flat key `log-rotate-length` from our original file is simplified to just `rotate-length`
because the `log` group is now defined by the parent object. The full Python access
path remains `log.rotate-length`, which only differs from the original flat key
by 1 character.

```json title="all-sample.json"  linenums="1"
{
    "log": {
        "level": "DEBUG",
        "file": "mylog.log",
        "rotate-length": 10000
    },
    "system": {
        "extensions": ".json,.yml,.yaml,.toml",
        "something-else": 42
    }
}
```

The TOML format requires a slightly different structure.

```toml title="all-sample.toml" linenums="1"
[log]
level = "DEBUG"
file = "mylog.log"
rotate-length = 10000

[system]
extensions = ".json,.yml,.yaml,.toml"
something-else = 42
```

For most projects, you can use standard TOML tables as shown above. They are just
as capable of containing your configuration data as any of the other configuration
file types. However, `pyproject.toml` is a standard file in most Python projects.

## Special Case: `pyproject.toml`

The `pyproject.toml` is a standardized file used by many Python tools
associated with the creation and maintenance of your project.
Specifically, the `pyproject.toml` file reserves the `[tool]` namespace for third-party
tool configurations (like `black` or `pytest`) to prevent conflicts with other software.
To prevent key clashes between tools, settings are grouped under a heading like
`[tool.your_app_name]`."

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Option 1: Nested Tables (Standard TOML)**

You can use standard nested tables, though this results in longer keys in Python:

```toml title="pyproject.toml (Nested)"  linenums="1"
[tool.application.log]
level = "DEBUG"
file = "mylog.log"

[tool.application.system]
extensions = ".json,.yml,.yaml,.toml"
```

Access this property using: `properties.get_string_property('tool.application.log.level')`

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Option 2: Dotted Keys (Recommended for application_properties)**

This package supports dotted keys within the `[tool]` section to match the simplicity
of your Python API:

```toml title="pyproject.toml (Dotted)"  linenums="1"
[tool.application]
log.level = "DEBUG"
log.file = "mylog.log"

system.extensions = ".json,.yml,.yaml,.toml"
```

Access this property using: `properties.get_string_property('log.level')`

> Note: While standard TOML validators might expect nested tables, the `application_properties`
> package explicitly parses these dotted keys within `[tool]` sections to maintain
> consistency with the dot-notation used with the `ApplicationProperties` object
> getter methods.

## Under the Hood

While you use dot-notation strings (like `'database.host'`) in your API calls,
the `application_properties` package handles the complexity for you.

- **Internally:** The package loads your configuration file into a nested Python
  dict (e.g., `{'database': {'host': 'localhost'}}`).
- **During Access:** When you call `get_string_property('database.host')`, the package
  automatically splits the string by the `.` character, navigates the nested dictionary
  for you, and returns the final property.

This design allows the package to handle the complexity of nested navigation, letting
you use simple dot-notation strings in your API calls while maintaining clean, grouped
files.

Now that we have structured our configuration files, let's look at how to access
these hierarchical values in Python using the dot-notation we discussed.

## Updating Our Sample Script

We need to update our Python script to reflect this new structure defined above.
The following code changes demonstrate how to access these grouped settings. All
transitions are trivial.  For instance, the `log.level` key in the `all-sample.yaml`
file maps to `properties.get_string_property('log.level')`. All of the other transformations
are just as simple.

```python title="snippet: Getters With Hierarchy"
print(f"log.level               = {properties.get_string_property('log.level')}")
print(f"log.rotate-length       = {properties.get_integer_property('log.rotate-length')}")
print(f"log.rotate-each-day     = {properties.get_boolean_property('log.rotate-each-day')}")
print(f"system.valid-extensions = {properties.get_string_list_property('system.valid-extensions', ',')}")
```

> Note that we now use the nested key `'log.level'` to reflect the log group we
> defined in the design phase.

From a code point of view, not much has changed. But from a usability point of view,
the configuration file is now a lot more user friendly.

## Next Steps

**Prerequisites For Going On:** If you followed along with the information in the
Quick Start guide, you have:

- **Recognized** how hierarchical grouping reduces cognitive load and prevents naming
  collisions in configuration files.
- **Applied** design principles like logical cohesion and shallow depth to structure
  your configuration logically.
- **Translated** hierarchical structures across YAML, JSON, and TOML formats while
  preserving key relationships.
- **Accessed** nested configuration values in Python using simple dot-notation strings
  via the `application_properties` API.

**Next**, in the Quick Start guide series:

- Use [Quick Start: Setting Properties Manually and Type Inference](./manual.md)
  to learn how to infer types for manual properties

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
