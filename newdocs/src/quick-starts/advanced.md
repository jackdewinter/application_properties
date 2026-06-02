# Quick Start: Fast Path for Experienced Python Users

This page is a focused, opinionated path to get `application_properties` installed
and used within a project. It assumes you already know Python, the command line,
and packaging tools, and you just want to see `application_properties` running in
sample code — without reading all the docs first.

This is not a complete guide. It is a fast run through our Quick Start pages with
the single goal of getting you using `application_properties` effectively as quickly
as possible.

If you prefer more explanation, screenshots, or step‑by‑step troubleshooting, use
the links in each **Troubleshooting** box to jump into the longer guides.

## Is This Guide Right For You?

Ready for a quick "jog" through the installation and example process? **If so**,
this guide is for you.

**If you are not sure if you are ready**, please go to our [Quick Start: Introduction](./index.md)
page. No harm, no foul. We would rather you have a good experience being introduced
to `application_properties` than be frustrated and giving up on it!

## TL;DR: Fastest Path

If you just want the absolute shortest path to see `application_properties` work
without any extra frills,
write the content below to a temporary bash script, and execute that script.

```bash title="temp.bash" linenums="1"
# Install globally
pip install pymarkdownlnt

# Or with Pipenv
pipenv install pymarkdownlnt

# Run once on a sample file
echo -e "system:\n  some-value: 1\n  another-value: one" > sample.md
cat > myfile.txt <<EOF
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader

properties = ApplicationProperties()
did_error = MultisourceConfigurationLoader() \
    .add_specified_configuration_file("sample.yaml", ConfigurationFileType.YAML) \
    .process(properties)
property_value = properties.get_string_property("mode", "(None)")

print(f"did_error = {did_error}")
print(f"property_value = {property_value}")
EOF

python ./sample.py
```

Note that this example is just what is advertises itself to be: a shortest path
example. If you want to know
more about the options available for you to use, read through the rest of this Quick
Start guide. Our team
has endeavoured to put together these high level examples that hit the major points
required for you to start
using the `application_properties` package in your project.

## Page Overview

This guide is organized as:

1. [Prerequisites](#prerequisites) – skim to confirm assumptions.
2. [Installation](#installation) – jump here for install commands.
3. [Trying `application_properties` For Yourself](#trying-application_properties-for-yourself)
   – run a sample that illustrates how to use `application_properties`

## Prerequisites

Unlike our other Quick Start pages, where the focus is on trying to keep things
as simple as possible for all users, this page assumes that:

- you are comfortable using the command line in your favorite shell and
  understanding commands like "go to your project root directory and run this"
- Python 3.10+ is installed and available on your `PATH`
- you know whether you need to use a **Python package manager** like Pipenv
  to install PyMarkdown, and if you want to install it as a **development-only dependency**

## Installation

Enter one of the following commands at the command line:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    pip install application_properties
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv install application_properties
    ```

<!-- pyml enable code-block-style-->

When using a Python package manager other than Pipenv, consult that tool's docs
for adding a dependency. For example:

<!-- pyml disable code-block-style-->
```sh
# Poetry
poetry add --dev application_properties

# uv
uv add --dev application_properties
```
<!-- pyml enable code-block-style-->

In general, the command is of the form:

<!-- pyml disable code-block-style-->
```sh
<package-manager> add/install [--dev] application_properties
```
<!-- pyml enable code-block-style-->

### Troubleshooting: Installation

<!-- pyml disable-next-line no-emphasis-as-heading-->
**Quick checks**

Before jumping to other docs, verify:

1. `python --version` shows Python 3.10 or higher.
2. `pip show application_properties` (or `pipenv graph | grep application_properties`)
   shows the package installed.

<!-- pyml disable-next-line no-emphasis-as-heading-->
**More help**

If those checks still fail:

- See [Install `application_properties` Locally](./installation.md) for a step‑by‑step,
  environment‑focused install guide.
- See [Installing `application_properties`](../getting-started.md) for virtualenvs,
  CI setups, and other advanced install scenarios.

## Trying `application_properties` For Yourself

To help you use the `application_properties` package in your projects, this section
walks you through:

- [Creating A Sample Configuration File](#step-1-creating-a-sample-configuration-file)
- [Creating A Simple Python File](#step-2-creating-a-simple-python-file)
- [Run The Sample Python File](#step-3-run-the-sample-python-file)
- [Verify The Output Is Correct](#step-4-verify-the-output-is-correct)
- [Understanding How That Output Was Arrived At](#step-5-understanding-how-that-output-was-arrived-at)
- [Experiment With The Sample Script](#step-6-experiment-with-the-sample-script)

### Step 1: Creating A Sample Configuration File

In a directory of your choice, create a file named `sample.yaml` with the contents:

```yaml title="sample.yaml" linenums="1"
system:
  some-value: 1
  another-value: "one"
```

### Step 2: Creating A Simple Python File

In the same directory, create a new file named `sample.py` with the contents:

```python title="sample.py" linenums="1"
from application_properties import ApplicationProperties
from application_properties.multisource_configuration_loader import MultisourceConfigurationLoader, ConfigurationFileType

properties = ApplicationProperties()
did_error = MultisourceConfigurationLoader() \
    .add_specified_configuration_file("sample.yaml", ConfigurationFileType.YAML) \
    .process(properties)
some_value = properties.get_integer_property("system.some-value", -1)
another_value = properties.get_string_property("system.another-value", "(None)")

print(f"did_error     = {did_error}")
print(f"some_value    = {some_value}")
print(f"another_value = {another_value}")
```

### Step 3: Run The Sample Python File

In the same directory as those two files, enter one of the following commands at
the command line:

<!-- pyml disable code-block-style-->
=== "Global Python Install"

    ```sh
    python ./sample.py
    ```

=== "Pipenv Package Manager"

    ```sh
    pipenv run python ./sample.py
    ```

<!-- pyml enable code-block-style-->

### Step 4: Verify The Output Is Correct

As a result of running the sample Python file, the following output should appear
in your console:

```text title="Standard Output"
did_error     = False
some_value    = 1
another_value = one
```

### Step 5: Understanding How That Output Was Arrived At

If you are here, you have the example working on your system! From here, you can
start to understand what the example does and how it does it.

Starting with the lines after the import statements:

1. an instance of `ApplicationProperties` is created and assigned to the variable
   `properties`
    - this is the configuration manager that will hold the configuration data
2. an instance of `MultisourceConfigurationLoader` is created, is told that it
   will load a specific configuration file, and then proceeds to load that configuration
   file when the `process` function is called
    - the `did_error` return value indicates whether all configuration data was
      loaded or if any of the configuration loaders failed to load their data
3. the property for the `some-value` entry in the `sample.yaml` file is rendered
   as an integer and printed
4. the property for the `another_value` entry in the `sample.yaml` file is rendered
   as an integer and printed

### Step 6: Experiment With The Sample Script

With the newfound knowledge of the `application_properties` package gained through
understanding
the `sample.py` script, you can start to play around with it to deepen you experience
with the
package. It is easier to experiment with a small example script like `sample.py`
than to experiment
from within your application, so take advantage of this opportunity and this script!

Here are some of the experiments you can try to get more experience with the `application_properties`
package:

- Using your IDE, use the inline help functions to discover more about the `MultisourceConfigurationLoader`
  class and the `ApplicationProperties` class
- Read the inline help on the `add_*` functions from the `MultisourceConfigurationLoader`
  class and try and figure out how to load other configuration files
- Add the getting and printing of both a boolean property and a string list property
  from a populated `ApplicationProperties` instance
- Make educated guesses on what the common parameters to all the getters are for
  the `ApplicationProperties` class

## Next Steps

You have three paths forward:

1. **Experiment in Your Codebase:** Jump into your own project. If you do,
   **commit your current changes first** to ensure you can safely roll back
   if conflicts arise.
2. **Skim the Quick Starts:** Review the [Quick Start: Introduction](./index.md)
   and subsequent guides. Use your recent experience to quickly identify which examples
   are relevant to your needs.
3. **Deep Dive:** For comprehensive reference and advanced scenarios, visit the
   [User Guide](../user-guide.md).

You now have the foundational knowledge to start using the `application_properties`
package immediately. Whether you prefer hands-on experimentation or structured learning,
the package is designed to fit seamlessly into your existing workflow. Choose the
path that best supports your development rhythm.
