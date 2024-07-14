# Library Package: application_properties

|   |   |
|---|---|
|Project|[![Version](https://img.shields.io/pypi/v/application_properties.svg)](https://pypi.org/project/application_properties)  [![Python Versions](https://img.shields.io/pypi/pyversions/application_properties.svg)](https://pypi.org/project/application_properties)  ![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)  [![License](https://img.shields.io/github/license/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/blob/main/LICENSE.txt)  [![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/application_properties)](https://github.com/jackdewinter/application_properties)|
|Quality|[![GitHub Workflow Status (event)](https://img.shields.io/github/actions/workflow/status/jackdewinter/application_properties/main.yml?branch=main)](https://github.com/jackdewinter/application_properties/actions/workflows/main.yml)  [![Issues](https://img.shields.io/github/issues/jackdewinter/application_properties.svg)](https://github.com/jackdewinter/application_properties/issues)  [![codecov](https://codecov.io/gh/jackdewinter/application_properties/branch/main/graph/badge.svg?token=PD5TKS8NQQ)](https://codecov.io/gh/jackdewinter/application_properties)  [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)  ![snyk](https://img.shields.io/snyk/vulnerabilities/github/jackdewinter/application_properties) |
|  |![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/dev/black/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/dev/flake8/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/dev/pylint/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/dev/mypy/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/dev/pyroma/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/dev/pre-commit/main) ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/application_properties/dev/sourcery/main)|
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

This project required Python 3.8 or later to function.

## Installation

```sh
pip install application_properties
```

## How To Use This Package

The primary goal of this package is to provide a simple, easy to use interface
to access properties within a Python script or program.  It is our contention
that 80% or more of general usage of such a package will be focused on two
elements:

- loading a group of properties from a file that is properly formatted
  for a given format
- accessing a specific string property, possibly with a default, from the that
  property store

### Examples

For concrete examples that show the power of this library package, please consult
the [Examples Document](./docs/examples.md).  If you come up with a normal example
of how to use our package that we have missed, or come up with a novel example of
how to use our package, please file an issue using the process below and let us
know. From our experience, one example can often paint a picture of how to use our
project that is difficult to explain clearly with just words.

## Issues and Future Plans

If you would like to report an issue with the library or the documentation, please
file an issue [using GitHub](https://github.com/jackdewinter/application_properties/issues).
Please remember to fill in as much information as possible including a good, repeatable
pattern for reproducing the issue.  Do not overflow us with too much information,
but provide us with enough information to make the problem evident to us.

If you would like to us to implement a feature that you believe is important, please
file an issue [using GitHub](https://github.com/jackdewinter/application_properties/issues)
that includes what you want to add, why you want to add it, and why it is important
to you, and how you think it will help others.  We truly want to listen to what
you see as a good feature, so please do not be upset if we say "no" or "let me
think about it".

Please note that the issue you file will usually be the start of a conversation,
so be ready for more questions.  If you have any Python developer skills, please
mention that as well.  The conversations about "hey, can you..." is a lot different
than "if I do... can I add it to the project?".

## When Did Things Change?

The changelog for this project is maintained [at this location](/changelog.md).

## Still Have Questions?

If you still have questions, please consult our
[Frequently Asked Questions](/docs/faq.md) document.

## Instructions For Contributing

Developer notes on various topics are kept in the the
[Developer Notes](/docs/developer.md) document.

If you attempting to contribute something to this project,
please follow the steps outlined in the
[CONTRIBUTING.md](/CONTRIBUTING.md) file.
