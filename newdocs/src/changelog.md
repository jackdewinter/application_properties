# Change Log

## Unversioned - In Main, Not Released

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- [Ensure all three loaders can handle a "." inside of keys, with a master switch.](https://github.com/jackdewinter/application_properties/issues/326)
    - Previous issue [Improper parsing of TOML](https://github.com/jackdewinter/application_properties/issues/269)
      added parsing of TOML to include "." characters in keys.  This feature expands
      that to the other two loaders, with a master switch in the key `application_properties`
      object.

<!-- pyml disable-next-line no-duplicate-heading-->
### Changed

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed

- None

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

<!-- pyml disable-next-line no-duplicate-heading-->
### Added

- [Ensure all three loaders can handle a "." inside of keys, with a master switch.](https://github.com/jackdewinter/application_properties/issues/326)
    - Previous issue [Improper parsing of TOML](https://github.com/jackdewinter/application_properties/issues/269)
      added parsing of TOML to include "." characters in keys.  This feature expands
      that to the other two loaders, with a master switch in the key `application_properties`
      object.

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- None

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed

- [Loaders not consistent with loading empty files](https://github.com/jackdewinter/application_properties/issues/325)
    - The three existing loaders were not consistent with respect to loading empty
      files.  This issue ensures that they all load a file, but do not mark it as
     applied, if the file is empty.

## Version 0.9.1 - Date: 2026-01-24

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- Added `py.typed` file to ensure that type hints are consumed by package.
- Added `__all__` variable to `__init__.py` to resolve mypy error

## Version 0.5.1 - Date: 2022-04-01

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- Adding Python typing hints
- Cleaning up project infrastructure to current PyMarkdown standards.

## Version 0.5.0 - Date: 2021-06-16

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed and Added

- Initial release
