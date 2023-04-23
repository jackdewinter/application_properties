# Change Log

## Unversioned - In Main, Not Released

## Version 0.7.0 - Date: 2023-04-22

- [Issue 137](https://github.com/jackdewinter/application_properties/issues/137)
  - to support multiple configurations, added clear_map flag to Json loader
  - refactoring to clean things up for upcoming changes
- [Issue 2](https://github.com/jackdewinter/application_properties/issues/2)
  - added ability to translate from string to other forms
  - controlled by flag, and only occurs on pure strings, not any strings with any typing
    - i.e. only manual set and "config" files are untyped, so only those are affected
- [Issue 145](https://github.com/jackdewinter/application_properties/issues/145)
  - added TOML configuration file support as a typed configuration file

## Version 0.6.0 - Date: xxxx-xx-xx

- quick release to help PyMarkdown project

## Version 0.5.2 - Date: 2022-04-01

### Fixed and Added

- Added `py.typed` file to ensure that type hints are consumed by package.
- Added `__all__` variable to `__init__.py` to resolve mypy error

## Version 0.5.1 - Date: 2022-04-01

### Fixed and Added

- Adding Python typing hints
- Cleaning up project infrastructure to current PyMarkdown standards.

## Version 0.5.0 - Date: 2021-06-16

### Fixed and Added

- Initial release
