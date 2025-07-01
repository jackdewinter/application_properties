# Change Log

## Unversioned - In Main, Not Released

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- None

## Version 0.9.0 - Date: 2025-06-30

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- Added proper documentation.
- Hosting documentation at ReadTheDocs.
- [Issue 148](https://github.com/jackdewinter/application_properties/issues/148)
    - Added JSON5 support, which includes support for JSON comments.

## Version 0.8.3 - Date: 2025-06-15

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- [Issue 271](https://github.com/jackdewinter/application_properties/issues/271)
    - Applying project templates across projects.

## Version 0.8.2 - Date: 2024-01-28

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- [Issue 195](https://github.com/jackdewinter/application_properties/issues/195)
    - Added YAML support for loading properties
- Fixed issue with installation not specifying `pyyaml>=6.0` as an installation dependency

## Version 0.8.0 - Date: 2023-07-16

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- [Issue 192](https://github.com/jackdewinter/application_properties/issues/192)
    - moved useful utility functions from PyMarkdown project into application_properties
      project
- [Issue 156](https://github.com/jackdewinter/application_properties/issues/156)
    - brought into alignment with other projects, for ease of maintenance
    - split up Pipfile dependencies into dev-packages and packages
- updating dependencies - 2023Jul15
- updating dependencies - 2023Jul02

## Version 0.7.0 - Date: 2023-04-22

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- [Issue 137](https://github.com/jackdewinter/application_properties/issues/137)
    - to support multiple configurations, added clear_map flag to Json loader
    - refactoring to clean things up for upcoming changes
- [Issue 2](https://github.com/jackdewinter/application_properties/issues/2)
    - added ability to translate from string to other forms
    - controlled by flag, and only occurs on pure strings, not any strings with
      any typing
        - i.e. only manual set and "config" files are untyped, so only those are
          affected
- [Issue 145](https://github.com/jackdewinter/application_properties/issues/145)
    - added TOML configuration file support as a typed configuration file
- upgraded tooling packages to latest version

## Version 0.6.0 - Date: xxxx-xx-xx

- quick release to help PyMarkdown project

## Version 0.5.2 - Date: 2022-04-01

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- Added `py.typed` file to ensure that type hints are consumed by package.
- Added `__all__` variable to `__init__.py` to resolve mypy error

## Version 0.5.1 - Date: 2022-04-01

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- Adding Python typing hints
- Cleaning up project infrastructure to current PyMarkdown standards.

## Version 0.5.0 - Date: 2021-06-16

<!--- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- Initial release
