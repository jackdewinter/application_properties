# Data Source Layering

If you are only implementing simple configuration handling that does
not extend past a single configuration data source, you may decide
to skip over this section and select another documentation page to
review.  However, if you are using more than one data source, you
will want to read the rest of this section to undertand how the
`application_properties` package thinks about the different layers or sources
of configuration data.

**Note:** The information on this page is complimented by the
[Quick Start: Configuration Data Layering](./quick-starts/layering.md) page.

## History

When our team created this package as part of the [PyMarkdown](https://github.com/jackdewinter/pymarkdown)
project, we wanted to provide flexibility in how
users can apply layers of configuration items.  Therefore, our team
designed this layered, hierarchical configuration property management
system to meet this requirement.  This design was essential to meet our requirements
that it supports the predictable collapse of multiple configuration layers according
to
the increasing specificity of the configuration
information.  

What does that mean in plain words? It means that we believe that more mature
projects work with multiple levels of configuration data, working from the least
specific data source (default values) to the most specific data source
(general command line settings).  It therefore stands to reasons that we want
to apply each layer of data independently according to that layer's specificity.

## Where to Start

Based on our own requirements, we believe that the majority of applications may
want to apply each
configuration layer based on some subset or some form of these layers in this order:

- default values (implicit if no other value provided)
- alternate configuration file (`tool.pymarkdown` section of `pyproject.toml` file)
- default configuration file (for example, `.application` file in current directory)
- configuration file specified on the command line by the arguments `--config {filename}`
- general command line setting (for example, `--set log.level=INFO`)
- specific command line settings (for example, `--log-file`)

By following this order, we can predictably build any required configuration item's
value in a manner that is logical and explainable to our users.  While most applications
will only
use one or two of these configuration data sources, we wanted to make sure that
we
can clearly and unambiguously describe
this ordering for any users that have a more complex configuration involving
multiple configuration data sources.

### Default Values

Each time that an application asks the configuration manager for a configuration
item,
it provides
a default value to use if none other are provided. Unless set to something specific,
this default value is the value `None`. That default ensures that a
predictable
value is returned if no layers have a value for the configuration item in question.
Note
that this layer is special in that it is implicit. If no value is assigned after
every other layer is applied, the default value is then applied.

### Alternate Configuration File

Support for the `pyproject.toml` file was added as a more generic way to support
many aspects of application configuration in a single, common file.  This layer
supports
loading configuration data from under a specific section within the local `pyproject.toml`
file.

### Default Configuration Files

Support for default JSON based configuration files were added right after the
[Command Line Configuration File](#command-line-configuration-file) support detailed
in the next section. Just as YAML and TOML support was added for those files,
default configuration files were added as a natural progression of the package.

### Command Line Configuration File

The initial form of configuration added to this project was to support a JSON
configuration file on the command line.  Typically provided to applications by
using something
like a `--config` command line argument followed by a file name,
this allowed for a consistent and concise way to configure an application for each
needed
scenario. Currently, the configuration file may be one of: JSON, YAML or TOML.

### Command Line `--set` Argument

With other forms of configuration implemented, our team found that there was a
bit of a gap between the general command line arguments and the configuration files.
The command line `--set` argument was introduced to fill this gap.  It was added
to be able to set an argument or two on the command line without having to craft
a new configuration file to support a temporary change, which our team does often
during debuging.
Note that because the command line does not support any implicit hierarchical
format, these arguments use a [flattened hierarchical](./basic-concepts#flattened-hierarchical)
format.
Also, because the command line is not capable of conveying type information,
a [special type system](./command-line.md#configuration-item-types) was devised
to convey that information.

### Specific Command Line Argument

At the top of the layering system is support for direct changes to how
the application works.  From our experience, these changes are at the command
line level and are shortcuts for the `--set` argument.

A good example of this is the `--log-level` command for the PyMarkdown application.
While it is true that the user can simply type `--set 'log.level=INFO'`, for
the more frequently used commands, users want a shortcut like `--log-level=INFO`.

## [TBD need a good title here]

When layering configuration data sources, there are two rules to remember:

1. **Load errors stop everything.** If any of the layer have an issue that raises
   an error, the loading of
   the configuration data is aborted to deal with the error.
2. **Last one wins.** If your first layer loads a configuration item with
   a key of `my.value` and the the last layer loads another configuration item with
   the same `my.value` key, the value that last layer provided will be used.

## How Are These Layers Used?

From our personal observations, when users first start using applications, they
are in the experimentation stage with the application. At that point in time,
they want to have the flexibility to change configuration items at will as they
figure out what configuration works for their particular needs. When they start
settling down on what works for them, those tried and tested configuration items
are added to a configuration file, with any other configuration items remaining
on the command line. Depending on the project team, a decision is made whether
they want to explicitly specify the configuration file on the command line
(with the `--config` command) or to simply use an default configuration file or
an alternate configuration file to host their configuration items.

While that progression may not match up with what you and your team have experienced,
our observations lead us to believe that it is a common pattern. As such, we
implemented these layers to match that pattern as a baseline.

### How Our Team Uses Configuration Layering

Our team makes heavy use of the command line configuration
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

## Practical Example

This example is provided to demonstrate these concepts of our configuration layering
system at work.  While we included examples of all six configuration layers, we
realize that it is overkill for many applications.  However, we would rather provide
an example that is easy to understand and goes too far, rather than one that does
not demonstrate the one type of configuration layer that you intended to use.
Please take from this example the information that you need.

### Setup

For the sake of this example, assume that we have a `pyproject.toml` in the local
directory with the content:

```toml title="pyproject.toml" linenums="1"
[tools.my-utility]
my.value: 1
```

a JSON file `.my-utility.json` that looks like:

```json title=".my-utility.json" linenums="1"
{
    "my" : {
        "other-value" : 2
    }
}
```

and a YAML file `my-specific.yaml` that looks like:

```yaml title="my-specific.yaml" linenums="1"
my:
    value: 3
```

In addition to those files, let us assume that our application has
a command line that accepts both `--set` direct manual arguments and a special `--value`
argument that is an indirect manual argument, a shortcut for the `--set my.value=`
argument.

### Working Through Each Level

[TBD needs better explanation, reword example]

Based on the settings defined at the start of [Where to Start](#where-to-start),
the general Python configuration comes first, setting the `my.value`
value to `1`.  Going up in order of specificity, the general project configuration
is next and sets the value of `my.other-value` to `2`.  While this example shows
these configuration items having different keys, that is not always the case.
In cases where `other-value` is replaced with `value`, the value of the configuration
item `my.value` would be `2`, as the more specific configuration overrides the
less specific configuration.

The `my-specific.yaml` file can be specified directly with the same effect as
when the `.my-utility.json` file was applied.  With the content specified above,
the value
of `my.value` would then change to `3` without affecting any other configuration
items.
Increasing in specificity yet again, if the user chopse to use a `--set` argument
like `--set my.other-value=3`
and a `--value 4` (mapped internal to the application to have the same effect
as `--set my.value=`) would override those two values that were set in the automatic
configuration files.

<!-- pyml disable-num-lines 5 no-inline-html-->
<!-- pyml disable-num-lines 4 line-length-->
| Flat Hierarchical Name<br>a.k.a. Property Name | `pyproject.toml` | `.my-utility.json` | `my-specific.yaml` | Final |
| --- | --- | --- | --- | --- |
| my.value | 1 | N/A | 3 | 3 |
| my.other-value | N/A | 2 | N/A | 2 |
