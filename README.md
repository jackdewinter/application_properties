# Library Package: application_properties

|   |   |
|---|---|
|Project|[![Version](https://img.shields.io/pypi/v/application_properties.svg)](https://pypi.org/project/application_properties)  [![Python Versions](https://img.shields.io/pypi/pyversions/application_properties.svg)](https://pypi.org/project/application_properties)  ![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)  [![License](https://img.shields.io/github/license/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/blob/main/LICENSE.txt)  [![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/application_properties)](https://github.com/jackdewinter/application_properties)|
|Quality|[![GitHub Workflow Status (event)](https://img.shields.io/github/actions/workflow/status/jackdewinter/application_properties/main.yml)](https://github.com/jackdewinter/application_properties/actions/workflows/main.yml)  [![Issues](https://img.shields.io/github/issues/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/issues)  [![codecov](https://codecov.io/gh/jackdewinter/application_properties/branch/main/graph/badge.svg?token=PD5TKS8NQQ)](https://codecov.io/gh/jackdewinter/application_properties)  [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.mkdocs&label=MkDocs) |
|  | ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.black&label=Black)  ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.flake8&label=Flake8) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pylint&label=PyLint) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.mirrors-mypy&label=MyPy) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pyroma&label=PyRoma) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.pre-commit&label=Pre-Commit) ![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fjackdewinter%2Fapplication_properties%2Fmain%2Fpublish%2Fdependencies.json&query=%24.sourcery&label=Sourcery) |
|Community|[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/jackdewinter/application_properties/graphs/commit-activity) [![Stars](https://img.shields.io/github/stars/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/stargazers)  [![Forks](https://img.shields.io/github/forks/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/network/members)  [![Contributors](https://img.shields.io/github/contributors/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/graphs/contributors)  [![Downloads](https://img.shields.io/pypi/dm/application_properties.svg)](https://pypistats.org/packages/application_properties)|
|Maintainers|[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=555)](https://www.linkedin.com/in/jackdewinter/)|

## Jumping Off Points

- **I want a high-level overview.**\
  Stay on this page to learn what `application_properties` is, why you might use it, what it
  can do, and whether it fits your projects.
- **I've decided to use `application_properties` and want to start quickly.**\
  Follow our [Quick Start guides](https://application-properties.readthedocs.io/en/latest/quick-starts/)
  to learn the core concepts and start incorporating configuration into your Python projects
  with easy-to-follow examples.
- **I've finished the Quick Starts or want deeper details.**\
  Read the [full documentation](https://application-properties.readthedocs.io/en/latest/) for
  TBD.

## What Is `application_properties`?

The `application_properties` package was born out of necessity. During the creation
of the [PyMarkdown](https://github.com/jackdewinter/pymarkdown) project,
there was a distinct need for a configuration subsystem that was able to handle more
complex configuration scenarios, such as only exposing relevant configuration to
the Rule Plugins that are a key part of PyMarkdown's rule system.

The `application_properties` package is for Pythond developers who want to add
solidly-tested plug-and-play configuration retrieval to their projects with a
minimum of fuss and management. The package has the following advantages:

- Thoroughly tested
  - The project currently has over 280 tests and coverage percentages over 99%.
- Simple... With Examples
  - The package was created with the intention of being as easy to use as possbile.
- Complex When Required
  - The default is simplicity, but the package can step up when required to do so.
  - Any actions outside of the simple scenario of getting an optional string value should
    be relatively easy to request of the package API.
- Hierarchically Aware
  - By default, uses the `.` character in the property names to define levels of hierarchy.
  - Hierarchy levels can be used to find only those properties that exist under a
    given hierarchy.
  - If desired for use cases that involve shared configuration, such as with PyMarkdown's Rule Plugins, the `ApplicationPropertiesFacade` object can be used to restrict access
    to only those properties that exist under a given hierarchy.
- Command Line Aware
  - The `set_manual_property` function provides for one or more individual properties to be
    supplied by the command line.
- Extensible
  - The loading of the properties is separate from access to the values for those properties.
  - Due to the separation of the loading and accessing parts of the library, custom loading
    classes can be added with ease.
    - Current loading classes include configuration file loaders for JSON files, YAML files, and TOML files.

## Requirements

This project requires Python 3.10 or later to function.

## Getting Started

If you are still with us at this point, you probably want to try this package out
for yourself and see if we can live up to our claims in the previous section. To
faciliate this, we have prepared [Quick Start guides](https://application-properties.readthedocs.io/en/latest/quick-starts/)
that walk your through the most common use cases for the `application_properties` package.

When you finish trying out the Quick Start guides for yourself, consider walking through
one of more sections of our [full documentation](https://application-properties.readthedocs.io/en/latest/)
to get more information on how `application_properties` can help you with your
Python configuration needs.
