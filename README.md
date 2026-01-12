# Library Package: application_properties

|   |   |
|---|---|
|Project|[![Version](https://img.shields.io/pypi/v/application_properties.svg)](https://pypi.org/project/application_properties)  [![Python Versions](https://img.shields.io/pypi/pyversions/application_properties.svg)](https://pypi.org/project/application_properties)  ![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)  [![License](https://img.shields.io/github/license/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/blob/main/LICENSE.txt)  [![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/application_properties)](https://github.com/jackdewinter/application_properties)|
|Quality|[![GitHub Workflow Status (event)](https://img.shields.io/github/actions/workflow/status/jackdewinter/application_properties/main.yml)](https://github.com/jackdewinter/application_properties/actions/workflows/main.yml)  [![Issues](https://img.shields.io/github/issues/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/issues)  [![codecov](https://codecov.io/gh/jackdewinter/application_properties/branch/main/graph/badge.svg?token=PD5TKS8NQQ)](https://codecov.io/gh/jackdewinter/application_properties)  [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.mkdocs&label=MkDocs) |
|  | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.black&label=Black)  ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.flake8&label=Flake8) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pylint&label=PyLint) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.mirrors-mypy&label=MyPy) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pyroma&label=PyRoma) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pre-commit&label=Pre-Commit) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.sourcery&label=Sourcery) |
|Community|[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/jackdewinter/application_properties/graphs/commit-activity) [![Stars](https://img.shields.io/github/stars/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/stargazers)  [![Forks](https://img.shields.io/github/forks/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/network/members)  [![Contributors](https://img.shields.io/github/contributors/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/graphs/contributors)  [![Downloads](https://img.shields.io/pypi/dm/application_properties.svg)](https://pypistats.org/packages/application_properties)|
|Maintainers|[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=555)](https://www.linkedin.com/in/jackdewinter/)|

The `application_properties` package was born out of necessity.
During the creation of the [PyMarkdown](https://github.com/jackdewinter/pymarkdown) project,
there was a distinct need for a configuration subsystem that was able to handle more
complex configuration scenarios.

The `application_properties` library has the following advantages:

- Thoroughly tested
  - The project currently has over 65 tests and coverage percentages over 99%.
- Simple... With Examples
  - The package was created with the intention of being as easy to use as possbile.
  - To that extent, there are 4 basic usage examples and over 10 advanced usage examples.
- Complex When Required
  - The default is simplicity, but the package can step up when required to do so.
  - Any actions outside of the simple scenario of getting an optional string value should
    be relatively easy to request of the package API.
- Hierarchically Aware
  - By default, uses the `.` character in the property names to define levels of hierarchy.
  - Hierarchy levels can be used to find only those properties that exist under a
    given hierarchy.
  - If desired, the `ApplicationPropertiesFacade` object can be used to restrict access
    to only those properties that exist under a given hierarchy.
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

This project requires Python 3.10 or later to function.

## How To Use This Package

Our documentation for this project is hosted on
[ReadTheDocs](https://application-properties.readthedocs.io/en/latest/).

This documentation includes:

- [Index](https://application-properties.readthedocs.io/en/latest/)
  - Similar to this page, just nicer formatting!
- [Getting Started](https://application-properties.readthedocs.io/en/latest/getting-started/)
  - Explanation of the terms and concepts that we believe will help you understand
    the rest of the documents.
- [Configuration Files](https://application-properties.readthedocs.io/en/latest/file-types/)
  - Information about the configuration file types that we support.
- [Command Line](https://application-properties.readthedocs.io/en/latest/command-line/)
  - How to interact with `application_properties` from the command line.
- [User Guide](https://application-properties.readthedocs.io/en/latest/user-guide/)
  - Walk-through of executable examples to help you get up to speed quicker.
