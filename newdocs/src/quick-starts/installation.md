# Quick Start: Installation

This guide walks you through installing the `application_properties` package so
you can
easily reference your configuration files from your Python projects.

## Prerequisites

Ensure your environment meets the following requirements:

- Python 3.10+ (check with `python --version`).

### Tool Choice For Virtual Environments

This documentation covers the following tools for managing virtual environments:

- [pipenv](https://pipenv.pypa.io/en/latest/) - Oldest of the three, supported for
  legacy systems.
- [poetry](https://python-poetry.org/) - More recent packaging manager.
- [uv](https://docs.astral.sh/uv/) - New kid on the block.

## What You Will Learn

On this page, you will master the foundational setup for the `application_properties`
package by learning to:

- **Select** the most appropriate virtual environment tool (pip, pipenv, poetry,
  or uv) based on your project's legacy or modernization needs.
- **Isolate** your project's dependencies by creating and activating a dedicated
  virtual environment to prevent global conflicts.
- **Install** the `application_properties` package using the command syntax specific
  to your chosen environment tool.
- **Verify** the successful installation by executing a provided validation script
  that confirms the package is accessible in your current context.

## Install `application_properties` Locally

The quickest way to get started with the `application_properties` package is to
install it globally with `pip`. This option requires no configuration and is the
simplest way to get started.

### Using Virtual Environments

We recommend using a virtual environment for each project. A virtual environment
isolates your project's packages from the global Python environment. Use virtual
environments for project isolation. For production projects or serious development,
virtual environments are required to prevent dependency conflicts.

If you are not using a virtual environment, perform the basic installation by following
the **Global Python Environment** advice below.

Note that Pipenv is one option for virtual environments. You may also use `poetry`
or `uv` if you prefer. These tools have similar formats to what `pipenv` uses.

For detailed information about installation, prerequisites, and alternative setups,
see the [Getting Started](../getting-started.md) guide. It covers more background
and advanced configuration examples.

Select the tab corresponding to your preferred installation method below.

### Installing The Package

From the base of your project root directory, open a terminal or command prompt
and run one of the following:

<!-- pyml disable code-block-style-->
=== "Global Python Environment"

    ```sh
    pip install application_properties
    ```

=== "Pipenv Virtual Environment"

    ```sh
    pipenv install application_properties
    ```

=== "Poetry Virtual Environment"

    ```sh
    poetry add application_properties
    ```

=== "UV Virtual Environment"

    ```sh
    uv add application_properties
    ```
<!-- pyml enable code-block-style-->

## Verifying `application_properties` Installation

Use this quick check to confirm that the `application_properties` package is installed
correctly. You only
need to perform this check once, after installation or after configuration changes.

In the root directory for your project, create a file named `install_validate.py`
and add the following contents:

<!-- pyml disable code-block-style-->
```python title="install_validate.py"
from application_properties import ApplicationProperties

properties = ApplicationProperties()
print("Done")
```
<!-- pyml disable code-block-style-->

After that file is saved, run the following command from your project's root directory:

<!-- pyml disable code-block-style-->
=== "Global Python Environment"

    ```sh
    python install_validate.py
    ```

=== "Pipenv Virtual Environment"

    ```sh
    pipenv run python install_validate.py
    ```

=== "Poetry Virtual Environment"

    ```sh
    poetry run python install_validate.py
    ```

=== "UV Virtual Environment"

    ```sh
    uv run python install_validate.py
    ```

<!-- pyml enable code-block-style-->

If everything was installed properly, you should see this output:

<!-- pyml disable code-block-style-->
```text title="standard output"
Done
```
<!-- pyml enable code-block-style-->

If the installation failed, you may see an error like:

<!-- pyml disable code-block-style-->
```text title="standard error"
Traceback (most recent call last):
  File "/user/home/za.py", line 1, in <module>
    import application_properties
ModuleNotFoundError: No module named 'application_properties'
```
<!-- pyml enable code-block-style-->

## If You Run Into Issues

If you encountered an error, review the installation steps above to identify the
cause. The most
common problems that our team has encountered are:

- accidentally creating a virtual environment in the wrong directory
- creating the `install_validate.py` file outside of the project directory
- attempting to execute `pipenv` from outside of the project directory

If you still have problems, the full [installation guide](../getting-started.md)
is always available to help you out.

## Next Steps

**Prerequisites For Going On:** If you followed along with the information in the
Quick Start guide, you have:

- **Selected** the appropriate package manager (pip, pipenv, poetry, or uv) for
  your project's needs.
- **Isolated** your project dependencies by creating and activating a dedicated
  virtual environment.
- **Installed** the `application_properties` package using the correct command
  syntax for your chosen environment.
- **Verified** your installation was successful by running the validation script
  and checking the output.

**Next**, in the Quick Start guides series:

- Use [Quick Start: Configuration Loaders](./loaders.md) to load YAML, JSON, and
  TOML files in just two function calls — no manual parsing needed.

**If** you need some review, select one of the items below:

<!-- pyml disable-num-lines 3 line-length-->
| Quick Start Page | Description |
| -- | -- |
| [Quick Start: Introduction](./index.md) | Understand the package's architecture and find the right learning path for your needs. |
