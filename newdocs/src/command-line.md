# Command Line Support

Provided as a default, the `ApplicationPropertiesUtilities` class
includes the `add_default_command_line_arguments` function that provides
three arguments to the command line:

- `--config` to specify a single configuration file
- `--set` to specify a single configuration item
- `--strict-config` to enable strict mode

While users are free to specify their own command line arguments and
names, the following sections will use these arguments as a baseline.

## Command Line Configuration Files

The most visible way to specify a configuration file is to use the
command line `--config` argument.  That argument specifies a relative or absolute
path to the configuration file to load.  The configuration file may be in any one
of three formats discussed in the document on [configuration file types](./file-types.md#configuration-file-types).

Keep in mind that configuration files are firmly in the middle when it comes
to [configuration layers](./getting-started.md#configuration-ordering-layering)
that the `application_properties` package supports.  Especially when debugging
and focusing on other things, it can be easy to forget that there are other
configuration layers that will override the configuration items in the configuration
file. Trust us... it has happened multiple times to our team.

## Command Line Configuration Settings

Configuration items set from the command line are the most specific form
of configuration.  Unlike any of the configuration items in configuration files,
these settings are specifically targeted to a specific invocation of the application
that is using the `application_properties` package.

These arguments come in two classes: a specific command line setting and a general
command line setting.  To illustrate the usage of command line arguments to set
configuration items, the following configuration items from PyMarkdown are used
as a reference point:

- `log.level` - string value of `INFO`
- `plugins.md007.code_block_line_length` - integer value of `160`
- `plugins.md007.enabled` - boolean value of `true`
- `extensions.front-matter.enabled` - boolean value of `true`

### Specific Command Line Settings

Specific command line settings are settings that are provided by the command
line as a shortcut for a longer configuration item or aggregated set of configuration
items.
A good example of a shortcut argument is a `--log-level INFO` command line argument
being a
shortcut for `--set mode.log-level=INFO`.  A good example of an aggregator
argument is a `--profile` argument that accepts a single argument that applies
multiple configuration items when invoked.  In both cases, the specific command
line argument is presented as a shortcut for the user's benefit.

Trying to determine which configuration items should have a more specific way of
setting their values was not an easy task for our [PyMarkdown](https://github.com/jackdewinter/pymarkdown)
team.  Enabling every setting
to have a direct command line invocation is not feasible, so we had to derive
a guideline for when a configuration item would merit its own command line argument.
This is what we came up with.

The first criteria that we decided on was to determine how frequently
that configuration item would be used.  A good example of this is the
`--log-level` and `--log-file` arguments. We figured that out of all
the configuration items in most applications, controlling the log output
was probably one of the top three most used configuration items.  From there,
we tried to
hit any other frequently used configuration setting, giving each a command line
argument.

The second criteria we used was to determine whether the configuration item
changed the behavior of the core application, or if it was related to one
of the features or plugins applied to the application.  For PyMarkdown,
a splendid example of this is the `--return-code-scheme` specific command line
setting.  This setting directly changes how return codes are returned from
the core PyMarkdown engine, something we believed made it eligible for
being a general command line argument.  

Your team may have their own criteria about what to expose as a detailed
command line setting in your application.  We just wanted to share our
criteria to give your team a good starting point for any discussions.

### General Command Line Settings

General command line settings use the `-s` or `--set` argument to
specify a single configuration property to set the value for.  The configuration
item key is identified using
its [flattened hierarchical format](./getting-started.md#flattened-hierarchical)
and an optional [configuration type](./command-line.md#configuration-item-types)
for the configuration item value. If no configuration type is provided, the property
uses a default type of `string`.
These two concepts work together to provide a condensed way to specify configuration
properties from the command line.

For the PyMarkdown development team, these arguments have proven to be useful in
providing shorthand for setting properties that are isolated and near the top
of the configuration item specificity list.  Because of its high ranking in the
configuration layers due to its specific nature, these
settings are less likely to be overridden.  For example, a common command line that
we use to display enhanced logging output is:

```bash
pymarkdown --stack-trace --set log.level=INFO scan examples
```

While a handful of configuration items have general command line settings, most
configuration items do not.

### Configuration Item Types

To provide a more robust configuration system, the configuration
manager uses values that are typed.  This extra
level of specification allows increased confidence that the value that
is provided for that configuration item is interpreted properly.
If you are using a configuration file format that provides type information,
this extra information is not required. However, as the command line
does not provide this type information, our team needed to develop
a notation that indicates what type to apply to the command line `--set` argument.

The type specification notation is as a prefix that the user applies for the configuration
item value. If the `*` character refers to any character, the following
table specifies the type behavior:

| Prefix | Type | Examples |
| --- | --- | --- |
| `*` or None | Default (String) | `abc` |
| `$*` (except for characters below) | Default (String) | `$abc` |
| `$$` | String | `$$abc` |
| `$#` | Integer | `$#1`, `$#-12345` |
| `$!` | Boolean | `$!True`, `$!anything-else-is-false` |

The only two interpretations that likely require further explanation are
the integer and the boolean types.  The integer type attempts to
translate any characters past the prefix as a signed integer.  The
boolean type compares any characters past the prefix in a [case-insensitive](./getting-started.md#case-insensitive)
manner against the sequence `true`, setting the configuration item's value to `True`
only if that comparison is true.

For our team, the decision to compare boolean values against `true` was an
easy one, with precedents in other tools.  But applying similar rules
to the integer conversion was not possible.  After thinking things through, we
landed on generating a ValueError for any invalid integer values, such as `$#1.1`.
There were alternatives, but this was the decision that felt the most
correct to us.  If a user took the time to use the integer prefix `$#`,
we felt they would want to error out on any non-integer value.

### Special Characters and Shells

On a Windows system, when entering configuration item type arguments that specify
a boolean type, the `!` character is used. Since this character is a special character,
you need to enter it as `^^!` on the command line to properly escape the `!` character.

```text
pipenv run pymarkdown --set extensions.front-matter.enabled=$^^!True scan -r .
```

On a Linux or MacOs system, most shells treat the `$` character as a special
character.  To escape this character, you need to enclose the argument with the
`'` character instead of the normal `"` character.

```text
pipenv run pymarkdown --set 'extensions.front-matter.enabled=$!True' scan -r .
```

### Typing Examples

Using actual PyMarkdown configuration items, examples of typing in action are:

<!-- pyml disable-num-lines 30 fenced-code-language-->
- indicate that the logging level should be set to
  show information log messages or higher (string value):

    ```
    pymarkdown --set log.level=INFO scan test.md
    ```

    OR

    ```
    pymarkdown --set log.level=$INFO scan test.md
    ```

    OR

    ```
    pymarkdown --set log.level=$$INFO scan test.md
    ```

- enabling the extension to interpret front matter (boolean value):

    ```
    pymarkdown --set extensions.front-matter.enabled=$!True scan test.md
    ```

- setting the maximum line length for code block lines to `160` (integer value)

    ```
    pymarkdown -s plugins.md007.code_block_line_length=$#160 scan test.md
    ```

## Strict Configuration Mode

During the development of the PyMarkdown linter, there were specific times where
we wanted to be sure that the configuration values that we specified were interpreted
exactly as we specified
them.  As we started doing exploratory testing of the PyMarkdown project, we also
realized that we are sticklers, wanting to ensure that any configuration properties
that we assign are correct and that those values are not reverting to default values.

However, our team's desire for that level of exactness seemed to be at
cross purposes to our decision to provide for a configuration manager that would
[work by default](./getting-started.md#our-philosophy-of-work-by-default).  That
is where the genesis of the idea
that would become the configuration manager's strict mode was formed.

Specified from the command line using the `--strict-config` flag (or
through the configuration as `mode.strict-config=$!True`), this
configuration item turns on the strict mode for the configuration system.
Once enabled, when the application reads values from the configuration,
it will stop the application if:

- the user provided a value for the configuration value, but it was the wrong type
- the user provided a value for the configuration value, but it does not match
  a specified filter for that value

Using the `log.level` example from above, the documentation states that it is required
to be a string in the following set: `CRITICAL`, `ERROR`, `WARNING`, `INFO`,
or `DEBUG`.  Therefore, both an integer value of `1` and a string value of
`information` would fail for distinct reasons.  Normally, these would
cause the configuration system to silently fail and not set the specified
value. As a result of that, the default value for that configuration
value will be used with no warning being issued.

However, with the strict configuration mode enabled, the following command
line:

```sh
pymarkdown --strict-config -s log.level=$#1 scan examples
```

produces the following output:

```text
Configuration Error: The value for property 'log.level' must be of type 'str'.
```

and the following command line:

```sh
pymarkdown --strict-config -s log.level=information scan examples
```

produces the following output:

```text
Configuration Error: The value for property 'log.level' is not valid: Value 'information' is not a valid log level.
```

This feature is more burdensome for the user, but it is provided as an option for
those users who want to make sure their provided configuration items are adhered
to exactly.
