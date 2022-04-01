# application_properties

[![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/application_properties)](https://github.com/jackdewinter/application_properties)
![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)
[![Python Versions](https://img.shields.io/pypi/pyversions/application_properties.svg)](https://pypi.org/project/application_properties)
[![Version](https://img.shields.io/pypi/v/application_properties.svg)](https://pypi.org/project/application_properties)

<!--
[![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/jackdewinter/application_properties/Main)](https://github.com/jackdewinter/application_properties/actions/workflows/main.yml)
[![Codecov](https://img.shields.io/codecov/c/github/jackdewinter/application_properties)](https://app.codecov.io/gh/jackdewinter/application_properties)
-->
![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/black/master)
![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/flake8/master)
![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/pylint/master)
[![Stars](https://img.shields.io/github/stars/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/stargazers)
[![Downloads](https://img.shields.io/pypi/dm/application_properties.svg)](https://pypistats.org/packages/application_properties)

[![Issues](https://img.shields.io/github/issues/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/issues)
[![License](https://img.shields.io/github/license/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/blob/main/LICENSE.txt)
[![Contributors](https://img.shields.io/github/contributors/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/graphs/contributors)
[![Forks](https://img.shields.io/github/forks/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/network/members)

[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=555)](https://www.linkedin.com/in/jackdewinter/)

The `application_properties` package was born out of necessity.
During the creation of the [PyMarkdown](https://github.com/jackdewinter/pymarkdown)
project, there was a distinct need for a configuration subsystem that was able to
handle more complex configuration schemas.

The `application_properties` library has the following advnatages:

- Thoroughly tested
  - The project currently has over 65 tests and coverage percentages over 99%.
- Simple... With Examples
  - The package was created with the intention of being as easy to use as possbile.
  - To that extent, there are 4 basic usage examples and over 10 advanced usage examples.
- Complex When Required
  - The default is simplicity, but the package can step up when required to do so.
  - Any actions outside of the simple scenario of getting an optional string
    value should be relatively easy to request of the package API.
- Hierarchically Aware
  - By default, uses the `.` character in the property names to define levels
    of hierarchy.
  - Hierarchy levels can be used to find only those properties that exist under
    a given hierarchy.
  - If desired, the `ApplicationPropertiesFacade` object can be used to
    restrict access to only those properties that exist under a given hierarchy.
- Command Line Aware
  - The `set_manual_property` function allows for one or more individual
    properties to be supplied by the command line.
- Extensible
  - The loading of the properties is separate from access to the values for
    those properties.
  - Due to the separation of the loading and accessing parts of the library,
    custom loading classes can be added with ease.
    - Current loading classes include loaders for Json files, with Simple
      Property files right around the corner

## Requirements

This project required Python 3.8 or later to function.

## Installation

```sh
pip install app_prop
```

## API Documentation

The full documentation on the API is available in the [API document](dd).
As that document is rather dry, more information is provided in the way of
examples in the [How To Use This Package section](dd) of the home page.

## How To Use, And Other Stuff

For more information on this library please consult the various other
section on the home page.
