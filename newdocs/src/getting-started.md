# Getting Started

In this document, we define the concepts that we believe are important
in the `application_properties` package.
This document is meant to be bridge between the [Index](./index.md), where we talk
about this package at a high level, and the [User Guide](./user-guide.md),
where we walked you through the code required to interact with this package from
your project.

Note that while it is possible to jump ahead to the [User Guide](./user-guide.md),
we strongly encourage you to at least scan this document to gain familiarity
with the nomenclature and ideas presented here.  As the other documents assume
that you have read this document, even a cursory scan of this document may avoid
future trips back to this document.  But in the end, please use these documents
in a manner that works for you and how you learn.

## Nomenclature

Before progressing through the rest of the documentation, we feel that it is necessary
to clearly describe the more important words and phrases we will be using.

### Configuration Manager

A component that takes care of managing multiple configuration input
sources and represents them as a logical and coherent set of configuration items.

### Configuration Item

A pairing of the rank and name of the configuration item along with its value.
This can be thought of as a key-value pair, as that is how these configuration
items will typically be represented.

### Hierarchical

The word [hierarchy](https://www.merriam-webster.com/dictionary/hierarchy) has many
definitions.  The one that comes closest to our use of it is:

> a ruling body of clergy organized into orders or ranks each subordinate to the
> one above it

Our configuration manager is hierarchical because it organizes its data into ranks,
where each rank determines the context of the rank below it.  For example, each group
of top-level items has a subordinate group of items below them, and those subordinate
items may also have their own subordinate items.

### Flattened Hierarchical

While a tradition hierarchy is expressed in a form such as:

```text
extensions
   my_extension
      my_value_1
      my_value_2
   my_other_extension
      my_value_1
```

some configuration files cannot support this expression of the hierarchy.  To
accommodate those systems, our configuration manager supports a flattened form
of this hierarchy.  A flattened hierarchy achieved this by taking each rank,
appending a `.`
character to it and then repeating this process for the next rank.  Given
the above hierarchy as an example, a flattened form would be:

```text
extensions.my_extension.my_value_1
extensions.my_extension.my_value_2
extensions.my_other_extension.my_value_1
```

The expression of the hierarchy has been brought down from 6 traditional elements
to
3 flattened elements.  For that compression, the cost is that there is
repetition in the flattened hierarchy, making the flattened hierarchy less readable
than the non-flattened hierarchy.  So why do this? Because even the simplest configuration
file formats can specify configuration item names with this format. As an extra
benefit, trying to convey a normal hierarchy can be time consuming, whereas
the flattened form is compact and simplifies communication of the hierarchy.

### Layered

The word `layered` implies that something has multiple distinct parts to it.  For
our configuration manager, we designed a data store that can manage input from various
sources, assigning each of those types of data sources to a given "layer".  When
viewed from an external point of view, these layers collapse to provide a single
view of the configuration data.

### String Value

A string value is a sequence of characters that is usually surrounded on both sides
by a boundary character.  For string values, that boundary character is typically
either the
`'` (apostrophe or single quote) character or the `"` (quotation mark or double
quote) character. For example, `"surrounded"` and
`'surrounded'` are standard examples of a string value.  Note that different formats
may
have conditions on which of the boundary characters denote a string value for that
format.

### Integer Value

An integer value is a sequence of numeric characters which may start with a single
`-` character or a single `+` character.  While some formats may accept a specified
value that includes a decimal point (`.` character), an integer value specifically
does not include any decimal point character.

### Boolean Value

A boolean value is a value that is either `true` or `false`.  Note that different
formats will have different rules regarding what values are considered `true` or
`false`, including whether any capitalization of the value is allowed.

### Case-insensitive

This refers to a comparison that is done without respect to the case of any
characters in the given string.  Using a case-insensitive comparison,
`False`, `false`, `FALSE`, and `FaLsE` are all equal.

## Our Philosophy of "Work By Default"

After taking stock of the requirements that we needed from a configuration manager,
we set out to create a configuration manager that we could feel proud of.  Given
our internal list of requirements, we
worked to balance the need for multiple sources of truth with the ability
to efficiently present that data to the application.  In the end, we are
pleased that we built a solid configuration manager that
meets our needs and has room for future extension.

While a lot of the decisions were easy, it took us a while to arrive at
the decision that we wanted our configuration manager to "work by default".
We use the phrase "work by default" as we have seen systems designed with
configuration managers that are extremely strict about what they accept. When
evaluating certain tools, we found that we spent 5-10 minutes setting various values
before we
were able to figure out if the tool worked for us.  We wanted to avoid giving
our users that sense of exasperation, if possible.

We do acknowledge that a strict configuration system is beneficial for large-scale,
back-end systems, especially ones without any reasonable user interface.  Using
our
PyMarkdown application as an example, we strongly believe that when a user starts
that
application, the application should be lenient with configuration items until the
user configures it to be strict in what it accepts for valid values.  If the user
requires a stricter interpretation of the configuration to be used, they can decide
to enable the [strict configuration mode](./command-line.md#strict-configuration-mode)
to enforce those requirements.

## Configuration Items

Back in the previous section on Nomenclature, we defined the terms
[Configuration Item](#configuration-item)
and [flattened hierarchical](#flattened-hierarchical) format.  Before we go forward,
we believe it is useful to be succinct in what we mean about a configuration item
and how we define such an object.

A configuration item contains two components: a hierarchical name
and a typed value.  We choose to store our configuration items within a hierarchical
structure, but not all file formats are able to convey that hierarchical format effectively.
In
addition, it is difficult for our team to express that exact hierarchical structure
in a text format that
does not involve multiple lines and wasteful whitespace.
As such, we describe the configuration item name using a flattened hierarchical format
that at least conveys the hierarchy information properly.

When we describe the value component of a configuration item, the value
is implicitly typed as a [string value](#string-value) unless otherwise specified.
Our configuration manager also supports a [boolean value](#boolean-value) and an
[integer value](#integer-value).  To date, we have not found any solid reason for
expanding our type system beyond those three type values.

## Configuration Ordering (Layering)

When our team created this package as part of the [PyMarkdown](https://github.com/jackdewinter/pymarkdown)
project, we wanted to provide flexibility in how
users can apply layers of configuration items.  Therefore, our team
designed this layered, hierarchical configuration property management
system to meet this requirement.  This design was essential to meet our requirements
that it supported the predictable collapse of configuration layers according to
the increasing specificity of the configuration
information.  

What does that mean in plain words? It means that we believe that more mature
projects work with multiple levels of configuration data, working from the least
specific data source (default values) to the most specific data source
(general command line settings).  It therefore stands to reasons that we want
to apply each layer of data independently according to that layer's specificity.
Specifically, we believe that the majority of applications want to apply each
configuration layer based on a subset of these layers:

- default value (implicit if no other value provided)
- alternate configuration file (`tool.pymarkdown` section of `pyproject.toml` file)
- default configuration file (for example, `.pymarkdown` file in current directory)
- configuration file specified on the command line by the arguments `--config {filename}`
- general command line setting (for example, `--set log.level=INFO`)
- specific command line settings (`--add-plugin`, `--log-file`)

By following this order, we can predictably build any required configuration item's
value in a manner that is logical and explainable.  While most applications will
only
use one or two of these configuration data sources, we wanted to make sure that we
clearly describe
this ordering for any users that have a more complex configuration involving
multiple configuration data sources.

### Default Value

Each time that an application asks the configuration manager for a configuration
item,
it provides
a default value to use if none other are provided.  This default ensures that a
predictable
value is returned if no layers have a value for the configuration item in question.
Note
that this layer is special in that it is implicit. If no value is assigned after
every other layer is applied, the default value is then applied.

### Alternate Configuration File

Support for the `pyproject.toml` file was added as a more generic way to support
application configuration.  For those users who prefer their project configuration
in
a single file, this layer supports a specific section of the `pyproject.toml` file
that allows the user to specify configuration items using a flattened hierarchy.

### Default Configuration File

Support for the JSON based configuration files were added as our team
got tired of having to add a configuration value to the application's command line
for every required setting.  While the
initial default configuration files were in the JSON format, support for the YAML
and TOML
configuration files were added later.

### Command Line Configuration File

The first form of configuration added to this project was support for a JSON
configuration file on the command line.  Typically provided to applications by
using something
like a `--config` command line argument followed by a file name,
this allowed for a consistent and concise way to configure an application for each
needed
scenario. Currently, the configuration file may be one of: JSON, YAML or TOML.

### Command Line `--set` Argument

With other forms of configuration implemented, our team found that there was a
bit of a gap between the general command line arguments and the configuration files.
The command line `--set` argument was introduced to fill this gap, mainly added
to be able to
set an argument or two on the command line without having to craft a new configuration
file.  Note that because the command line does not support any implicit hierarchical
format, these arguments use a [flattened hierarchical](#flattened-hierarchical) format.
Also, because the command line is not capable of conveying type information,
a [special type system](./command-line.md#configuration-item-types) was devised
to convey that information.

### Specific Command Line Argument

At the top of the layering system is support for direct changes to how
the application works.  From our experience, these changes are at the command
line level and are shortcuts for the `--set` argument.

A good example of this
is the `--log-level` command for many applications.  At the beginning, most
people want to control this only from the command line, keeping things simple.
As the project gets more mature, users often ask for items like the `log-level`
to be available at the command line and in configuration files. From our observations
on other projects, there are rarely two separate configuration values for items
such as log levels.  To keep things simple, these two (or more) ways of specifying
the log level are performed as high up in the configuration code as possible.

## Practical Example

This example is provided to demonstrate these concepts of our configuration layering
system at work.  While we included examples of all six configuration layers, we
realize that it is overkill for many applications.  However, we would rather provide
an example that is easy to understand and goes too far, rather than one that does
not demonstrate the one type of configuration layer that you intended to use.
Please take from this example that information that you need.

For the sake of this example, assume that we have a `pyproject.toml` in the local
directory with the content:

```toml
[tools.my-utility]
my.value: 1
```

a JSON file `.my-utility.json` that looks like:

```json
{
    "my" : {
        "other-value" : 2
    }
}
```

and a YAML file `my-specific.yaml` that looks like:

```yaml
my:
    value: 3
```

In addition to those files, let us assume that our application has
a command line that accepts both `--set` arguments and a special `--value`
argument that is a shortcut for the `--set my.value=` argument.

By default, the general Python configuration comes first, setting the `my.value`
value to `1`.  Going up in order of specificity, the general project configuration
is next and sets the value of `my.other-value` to `2`.  While this example shows
these configuration items having different keys, that is not always the case.
In cases where `other-value` is replaced with `value`, the value of the configuration
item `my.value` would be `2`, as the more specific configuration overrides the
less specific configuration.

At this point in the layering, the value of `my.value` is `1`, the value of `my.other-value`
is `2`, and the value of another value `my.other-other-value` would be determined
by the default value passed in retrieving these values.  By processing these default
settings automatically, the application can provide for a predictable manner
with which to specify application baselines, while keeping its command line clean.
This can be done safely with the knowledge that any changes applied in the more
specific configuration layers have precedence over those foundational configuration
items.

The `my-specific.yaml` file can be specified directly with the same effect as
when the `.my-utility.json` file was applied.  With the content specified above,
the value
of `my.value` changes to `3` without affecting any other configuration items.
Increasing in specificity yet again, using a `--set` argument like `--set my.other-value=3`
and a `--value 4` (mapped internal to the application to have the same effect
as `--set my.value=`) would override those two values that were set in the automatic
configuration files.

Why is this useful?  Our team makes heavy use of the command line configuration
file and the `--set` argument in the PyMarkdown test suites to set configuration.
Depending
on the individual test or the group of tests, we can use a combination
of those two layers to focus our configuration on what we need.  From a debugging
point of view, we will often use the `--set` layer to experiment with rules and
settings.  Most importantly, giving our users the ability to work with the configuration
items in a way that makes sense to them is important to us.

Which is also where the general command line arguments come in.  While it is
technically outside the scope of the `application_properties` package, it is the
final configuration layer.  Before configuration managers are added to a project,
most of the options are specified with command line arguments.  As the number of
configuration items grows and the project becomes more complex, many of those
command line arguments are folded into the configuration manager.

However, one thing that our team has noticed when looking at other applications
is that most projects do not completely
do away with those configuration-based command line arguments.  The two big reasons
for this are shortcuts.  Whether the shortcut
is to save the user from typing in `--set my.value=` each time or providing an
aggregation `--profile X` that allow the user to specify a provide that gets expanded
into multiple configuration items, both provide can provide a better experience
of the application to the user.
