# Introduction

> **NOTE:** Please bear with our "mess" as we reorganize our documentation and work
> on making it more reflective of the changes that have been introduced since the
> last documentation update.
>
> We have completed the new [Quick Start guides](./quick-starts/index.md), barring
> an extra review against the [User Guide](./user-guide.md) section once that section
> is finished. These Quick Start guides offer ready-to-run examples for the `application_properties`
> package. We hope to have the changes to the [User Guide](./user-guide.md) section
> and other changes to the documentation completed by 2026 Jul 01.
>
> Thanks for your patience. Please reach out with [any issues](./usual.md) in the
> documentation, and we will endeavor to address it as quickly as possible.

## Where to Start

If you are looking for a high-level overview of the `application_properties` package
— what it is, why you
might use it, and what it can do — the main [README.md](https://github.com/jackdewinter/application_properties/blob/main/README.md)
file is a great place to start and to decide whether `application_properties`
is a good fit for
your project, your workflow, and your team.

If you have decided to use the `application_properties` package for your Python
configuration needs, read our
[Quick Start guides](./quick-starts/index.md) to get started quickly and learn the
core concepts
of using the `application_properties` package in your Python projects.

If you have already viewed our Quick Start guides, or simply want more information
on the `application_properties` package and its capabilities, continue reading
the information provided in the pages of this documentation. By using the contents
controls located
on the left and right sidebars, you can quickly navigate to information and other
reference material that you can explore
as you become more comfortable with `application_properties` and want to go beyond
the basics.

## Core Package Concepts

The `application_properties` package was born out of necessity.
During the creation of the [PyMarkdown](https://pymarkdown.readthedocs.io/en/latest/)
project, there was a distinct need for a configuration subsystem that was able
to
handle more complex configuration scenarios. That is where the bulk of the
development of the package foundations occurred.

But it did not stop there. When creating small personal projects, our team found
that we wanted to have the simple configuration file support and the interfaces that
resembled parts of what we had in our PyMarkdown project.
That is when the application_properties
project was born [on GitHub](https://github.com/jackdewinter/application_properties).

Since then, we have worked to balance the concepts of a useful configuration system
and
an interface that is easy to use. Here are some of the features we believe help
us achieve that balance.

### Ease of Implementation

Our goal with this concept is to motivate our users towards using `application_properties`
in all of
their applications, simply because it is a low friction way to handle application
configuration.

This one is very important to us. What use is a configuration system if you have
to
spend a lot of time setting it up to match what you project needs? Additionally,
if a configuration
system takes a lot of time to set up, that probably indicates that it will have
similar needs
when it comes to maintenance. For larger projects that is often assumed, but that
should definitely
not be the case for small projects. As our team uses our own `application_properties`
package
in our own local Python projects, we continue to make sure that we can add it to
those projects quickly
and without much fuss.

Currently, small applications can use a minimal setup of the `application_properties`
package that is contained within four function calls. But even in the
configuration setup for the [PyMarkdown application](https://raw.githubusercontent.com/jackdewinter/pymarkdown/refs/heads/main/pymarkdown/application_configuration_helper.py#:~:text=options%20%3D%20MultisourceConfigurationLoaderOptions(%0A%20%20%20%20%20%20%20%20%20%20%20%20load_json_files_as_json5,True%0A%20%20%20%20%20%20%20%20)%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20properties.enable_strict_mode()),
only nine calls to the `ApplicationProperties` and `MultisourceConfigurationLoader`
are
required to meet its configuration setup needs. For our team, this ease of use is
a big win.

### Separation of Concerns

The goal here is a simple one. If a package clearly implements separation of concerns
within itself,
that package is easier to understand, easier to maintain, and easier to test.

With the `application_properties` package, there is a clear separation between loading
configuration data at the start of the application and getting that configuration
data
later in the application. We feel that this distinction is important because it
allows the developer
that is adding `application_properties` to their application to make intelligent
decisions on how to use the configuration information.

A great example of this is a small monitoring project that we use to monitor some
of our local systems. Because of the separation of concerns, we are able to deploy
monitoring changes by adjusting the configuration file that the application runs
off of without restarting
that application. When
configuration file changes are encountered, the new configuration is loaded without
affecting any of the getter functions used to retrieve the data.

**NOTE**: To be clear, that project takes steps to ensure that the new data is
properly staged to avoid any underlying data changing during a monitoring pass.
However, other than those steps, the rest of the configuration management is 100%
`application_properties`.

### Extensible

Our team's goal is not to [boil the ocean](https://www.theidioms.com/boil-the-ocean/)
when
it comes to configuration.  Our goal is to provide a solid foundation that meets
at least ninety
percent of our user's needs while providing extensibility paths that they can follow
to enable
them to complete that final ten percent of their needs themselves.

The `application_properties` package currently ships with support for loading
configuration from four type of configuration files and four primitives for retrieving
data from the `ApplicationProperties` object. These are all interfaces for populating
and retrieving information from the combined dictionary at the heart of the `ApplicationProperties`
object.

If you want to extend `application_properties` locally to load your configuration
data from a different data source, there is a simple
path to add [custom configuration data loaders](./custom.md#custom-configuration-data-loaders).
If you have unusually shaped configuration information
and want to extend `application_properties` to fetch that data 'natively', there
is a simple path
to add [custom configuration data accessors](./custom.md#custom-configuration-data-accessors)
that meets your needs.

<!-- pyml disable-next-line no-trailing-punctuation-->
### K.I.S.S.

The [KISS Principle](https://en.wikipedia.org/wiki/KISS_principle) clearly states
that
simplicity should be a design goal. From our team's collective experience, the more
complex a system
is, the more difficult it is to effectively implement, maintain, and test. Our goal
here is to keep `application_properties` simple by default, only adding complexity
when needed.

Each of our configuration loaders implements a `load_and_set` function that allows
it to do whatever processing it needs to add the right data to the `application_properties`
configuration data store. Each of those configuration loaders is then fronted by
a `BaseConfigurationSource` based class that allows for it to be referenced by the
`MultisourceConfigurationLoader`. With few exceptions, each of our `get_*` functions
implements the
exact same group of parameters to ensure that users can easily transition from one
of
those functions to any other of those functions.

For our users, there is an easy win that is enabled by keeping things simple. Once
our users have configured `MultisourceConfigurationLoader` to use one of our configuration
loaders,
adding other configuration loaders should be an easy task. Similarly,
after using one of our getter functions, such as the `get_string_property` function,
the other
getter functions should be self-explanatory. And where things are not simple, we
have online
documentation and in-editor documentation to help them out.

### Common Sense Defaults

For our team, this is an extension of the previous section on K.I.S.S., but it is
important
enough to us that we wanted to emphasize it in its own section.

We strive for keeping things simple. But writing a configuration package like `application_properties`
that handles both simple cases and complex cases is not easy. We continuously have
to ask ourselves,
"if we enable this new feature, how will it affect the rest of the package?" This
is where
smart and common sense defaults come into play.

Each time your application calls one of the `application_properties` functions,
there should be no surprises on
what that function's default behavior should be. The name of the function should
give the
user an expectation of what will happen when they invoke that function. When that
function is called,
it should have proper defaults that ensure that the default behavior is followed.
It takes a configuration object change (on either
the `ApplicationProperties` object or the `MultisourceConfigurationLoader` object)
or changing
a previously defaulted parameter to now be a parameter with a valid value to enable
that
extended behavior.

### Near Invisibility

This concept is one where you may be reading this and going "huh? what?", but let
us explain.
In our office,
the two most useful tools are the office lights and the office sound system. We
have both
connected up to automation services. Both of these work together to provide our
team with the creative environment that we need to develop our projects. Both of
these tools
are relatively invisible until they are needed.

For us, a large part of this package is making the package so simple to use that
you almost forget
that it is there. Most projects where we use `application_properties` have a simple
"load configuration here" section
that sets configuration data once, and then uses `get_*` functions in key areas
to
use that configuration data. Because `application_properties` provides the configuration
capabilities that we normally require, we often forget it is there.

In our minds, that is a good thing. A simple package that does what it is supposed
to do,
does it without fanfare, and does it without requiring a lot of maintenance.

## What to Do Next?

After reading the above sections, if you believe that the `application_properties`
package will be a benefit to your development project, we encourage you to follow
up by reading
more about the `application_properties` package at one of the following places:

- our [Quick Start guides](./quick-starts/index.md) for the `application_properties`
  package for a fast-track to installing the package and using it in one of your
  own Python applications
- our [Getting Started](./getting-started.md) page that presents a slower and more
  complete path to installing the package
- our [User Guide](./user-guide.md) that contains everything you need to know about
  the `application_properties` package
