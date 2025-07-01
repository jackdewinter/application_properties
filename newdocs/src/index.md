# Index

The `application_properties` package was born out of necessity.
During the creation of the [PyMarkdown](https://pymarkdown.readthedocs.io/en/latest/)
project, there was a distinct need for a configuration subsystem that was able to
handle more complex configuration scenarios. That is when the application_properties
project was born [on GitHub](https://github.com/jackdewinter/application_properties).

The `application_properties` package has the following advantages:

- Thoroughly tested
    - The project currently has over 200 tests with 100% coverage.
    - Comprehensive set of scenarios that test how `application_properties`
      reacts to situations are coded and passing.
- Simple... With Examples
    - The package was created with the intention of being as easy to use as possible.
    - The [User Guide](./user-guide.md) provides solid examples of how to use this
      package with real world examples.
- Complex When Required
    - The default is simplicity, but the package can step up when required to
      do so.
    - Any actions outside of the simple scenario of getting an optional string value
      should be relatively easy to request of the package API.
- Hierarchically Aware
    - By default, uses the `.` character in the property names to define levels
      of hierarchy.
    - Hierarchy levels can be used to find only those properties that exist under
      a given hierarchy.
    - If desired, the `ApplicationPropertiesFacade` object can be used to restrict
      access to only those properties that exist under a given hierarchy.
- Command Line Aware
    - The `set_manual_property` function allows for one or more individual properties
      to be supplied by the command line.
- Extensible
    - The loading of the properties is separate from access to the values for those
      properties.
    - Due to the separation of the loading and accessing parts of the library, custom
      loading classes can be added with ease.
    - Current loading classes include loaders for Json files, with Simple Property
      files right around the corner.

If these advantages are to your project's benefit, we encourage you to read the
other documentation on the `application_properties` package. Documents that we
feel are important to point out are:

- Our [Getting Started](./getting-started.md) document covers what we believe are
  necessary topics that provide a comprehensive foundation of why we created the
  `application_properties` package.
- Our [User Guide](./user-guide.md) document provides information on how to
  interact with `application_properties` package.
    - This includes simple examples that you can try yourself!
- Our [Configuration File Types](./file-types.md) document covers the out-of-the-box
  file types that the `application_properties` package supports, including feature
  comparisons between those types.
    - If you are interested in the journey of the `application_properties` package,
      we encourage you to read the [History of Configuration File Support](./file-types.md#history-of-configuration-file-support).
      It may be dry reading, but the journey will be of interest to any developer
      who has had to evolve a project over a given period.
- Our [Command Line Support](./command-line.md) document provides for a solid baseline
  to use when adding `application_properties` command line support into a project.
    - The [Configuration Item Types](./command-line.md/#configuration-item-types)
      provides information on how `application_properties` can use string prefixes
      to allow for stronger value typing for untyped sources.
    - The [Strict Configuration Mode](./command-line.md#strict-configuration-mode)
      continues the discussion of Configuration Item Types by talking about
      "strict mode"
