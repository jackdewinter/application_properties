# Change Log

## Unversioned - In Main, Not Released

<!-- pyml disable-next-line no-duplicate-heading-->
### Added

- None

<!-- pyml disable-next-line no-duplicate-heading-->
### Changed

- None

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed

- None

## Version 0.9.1 - Date: 2026-01-24

<!-- pyml disable-next-line no-duplicate-heading-->
### Fixed

- [Improper parsing of TOML](https://github.com/jackdewinter/application_properties/issues/269)
    - The `.` character is considered a separator character for keys, with the code
      checking to prevent that character from being used within a key. As TOML
      will already break the key on that character, a bypass was added to allow the
      TOML keys to include a `.` character IF it is in quotes.
- [Config flag fails to apply pyproject TOML](https://github.com/jackdewinter/application_properties/issues/318)
    - If the `pyproject.toml` file was loaded implicitly, the file was loading
      and processing the TOML file to only look at the "section header" that was
      specified. If passed using `--config`, it was not. Added the `section_header_if_toml`
      field to the `MultisourceConfigurationLoaderOptions` class to allow an optional
      section header to be passed in when loading an "untyped" configuration file.
