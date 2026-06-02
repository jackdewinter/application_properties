---
summary: Instructions on how to start working with application_properties
authors:
  - Jack De Winter
---

# Getting Started

The next sections describe how to set up:

- Python (3.10+)
- Pipenv for project-local dependency management

After that, we show how to install the `application_properties` package.

## Quick Start Guide

If you only need the fastest path to "the `application_properties` package is installed",
use our
[Quick Start: Installation](./quick-starts/installation.md) guide.

This page is for readers who want a more complete setup: why we recommend Pipenv
(and other virtual environment managers)
and how to verify everything is installed locally. If you already know some of this,
skim or jump to the sections you care about.

## Prerequisites

The `application_properties` package is a Python package that handles most aspects
of loading and accessing configuration data for use in Python scripts and applications

As this is the case, both Python and Pipenv (or Pip) must be installed on your
system to use the `application_properties` package.  Therefore, it is pivotal that
you install the prerequisites below first.

If you already have Python and Pipenv installed, feel free to skip ahead to
[Installing the `application_properties` package](#installing-the-application_properties-package).

### Installing Python

PyMarkdown requires Python 3.10 or later. Verify your version:

```text
python --version
```

If this does not report at least Python 3.10.x, install or upgrade Python from the
[official downloads page](https://www.python.org/downloads/) before continuing.

### Installing Pipenv

We use [Pipenv](https://pipenv.pypa.io/en/latest/) as a virtual environment manager.
This is a simple way
to manage and contain dependencies and recommend
it for any development project. In most setups, Pipenv is installed globally, and
each project
keeps its own `Pipfile` / `Pipfile.lock` and uses `pipenv run` inside a project-local
virtual environment.

Verify that Pipenv is installed and check its version with:

```bash
pipenv --version
```

If Pipenv is not installed or not on your PATH, this command fails with an error.
If it is installed, you'll see output like:

```text
pipenv, version 2023.12.1
```

where the noted version is the year-month-date of the latest release. If Pipenv
is not installed, it can be installed by executing the following command:

```bash
pip install --user pipenv
```

If Pipenv is installed but not at the latest version, the `pip install` command
will indicate that a newer release is available. Because Pipenv receives regular
security fixes, we recommend upgrading to the latest version whenever possible.

## Installing the `application_properties` package

The examples below use Pipenv-based commands. If you prefer a global installation,
adapt them as follows:

- Replace `pipenv install -d` with `pip install`.
- Remove the `pipenv run` prefix to the other command lines

The rest of the instructions remain the same.

### Installing the `application_properties` package With Pipenv

In your project directory, run:

```bash
pipenv install application_properties
```

To confirm that the `application_properties` package is installed for the project,
enter the
following command line:

```bash
pipenv run pip list | grep application_properties
```

If the `application_properties` package was installed properly, output will be returned
in the form of:

```text
application_properties      {major}.{minor}.{fix}
```

If the package was not installed properly, the `pipenv install` command should output
a lot of information on why the installation failed and hints on what you can do
to address those issues.

### Verifying The Installation

To verify that your chosen execution path works, follow these steps:

In the root directory for your project, create a file named `sample.py` and add
the following contents:

```text
from application_properties import ApplicationProperties

object = ApplicationProperties()
print("Done")
```

After that file is saved, run the following command from your project's root directory:

```bash
pipenv run python sample.py
```

If everything was installed properly, you should see this output:

```text
Done
```

If there was a problem with that installation, you will see something similar to:

```text
Traceback (most recent call last):
  File "/user/home/za.py", line 1, in <module>
    import application_properties
ModuleNotFoundError: No module named 'application_properties'
```

If there was a problem, please walk back through the installation steps that you
just
followed to look for anything that may point to the cause of the problem. The most
common problems that we have encountered are:

- accidentally creating a virtual environment in the wrong directory
- creating the `sample.py` file outside of the project directory
- attempting to execute `pipenv` from outside of the project directory

All of these problems are easily solvable by going back to
[Installing the `application_properties` package With Pipenv](#installing-the-application_properties-package-with-pipenv)
section and working forward from there.
