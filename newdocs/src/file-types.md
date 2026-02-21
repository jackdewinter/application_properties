# Configuration Files

When you start building an application, you typically have a small set of configuration
values to set. At that point, setting those values through command line arguments
is
usually the most efficient route to take for your development team. Those arguments
are flexible
and easy to control, providing quick feedback on your changes and how they affect
your application.  At the start of building an application, that flexibility and
quick
reaction time is exactly what your team needs.  But as your application grows,
that small set of configuration
items grows according to the needs of your application.  For most applications,
possessing the ability to also specify those configuration items using configuration
files
becomes necessary.

Depending on the requirements of your application, your application may need the
`application_properties`
configuration manager to provide [strict adherence to typing](./command-line.md#strict-configuration-mode).
As any application using the `application_properties` package may require it to
adhere to strict typing,
it only makes sense that each configuration file format that the package natively
supports
also supports typed values to allow for strict typing to occur.  Specifically,
`application_properties` requires that
any standard configuration file format support the ability the represent data as
a string value, an integer value, or a boolean value.  All three of the configuration
file types listed in the following section adhere to those requirements.

## Configuration File Types

The `application_properties` package supports configuration files in three formats:
JSON, YAML and TOML.

### JSON

The [JSON file format](https://www.w3schools.com/whatis/whatis_json.asp) is one
of the most widely used file formats for exchanging
data between systems.  The [JavaScript Object Notation](https://en.wikipedia.org/wiki/JSON)
format was created
in 2001 by David Crockford to enable standardized electronic data interchange
between browsers and backend system.  In fact, one of the first uses of JSON
was to allow browsers to refresh sections of their pages without having to
reload the entire page.  While that may seem ordinary now, that was a novel concept
when it was introduced.  From there, its use just continued to grow due to its
readability and robustness.

Here is an example of a JSON configuration file, using a simplified form of the
configuration file used with the documentation for our
[PyMarkdown](https://github.com/jackdewinter/pymarkdown) application:

```json
{
    "plugins": {
        "md007": {
            "enabled": true,
            "code_block_line_length" : 160
        }
    },
    "extensions": {
        "front-matter" : {
            "enabled" : true
        }
    }
}
```

There are three important things to understand about the JSON configuration
file format.  The first thing is that the values presented above are typed
values.  Due to the absence of `"` characters, each of the two `enabled` fields
denote a boolean `true` value, and the `code_block_line_length` field denotes
an integer `160` value.  As JSON is extremely strict about its structure, the
configuration manager can read this file and leverage that strictness.

The second thing to understand is the use of a normal hierarchical structure
instead of a flattened hierarchical structure.  While flattened structures
are useful when describing the configuration item, they are not efficient
when storing the configuration item.  As we can see by the above example,
there are two configuration items that reference Rule Md007: the `enabled`
item and the `code_block_line_length` item. This shared structure serves
as a visual reminder that they are related, while also reducing the count
of characters needed to represent those two configuration items.

The final thing to understand is that the hierarchy of a JSON file is
enforced through the choice of specific characters at each level. For
example, the line `"plugins": {` means that the JSON object `plugins`
contains another object.  The line `"enabled": true` means that the
JSON object `enabled` contains a boolean value of true.  Those characters,
and other similar characters, allow JSON to unambiguously represent the configuration
items. That strict representation is one of JSON's strengths.

#### "Pretty" JSON

Please keep in mind that the JSON example above is what is referred to as a "pretty"
example,
a JSON file with a four-space indent at each level.  It can also be
rendered in a condensed format with a zero-space indent as:

```json
{
"plugins": {
"md007": {
"enabled": true,
"code_block_line_length" : 160
},
},
"extensions": {
"front-matter" : {
"enabled" : true
},
}
}
```

or as a single line:

```json
{"plugins":{"md007":{"enabled":true,"code_block_line_length":160},},"extensions":{"front-matter":{"enabled":true},}}
```

or with any indent you require without any loss of hierarchy or data.  While that
is possible, we highly recommend that you use a 2-space-indent of 4-space-indent
form of the "pretty" JSON format for your human
readable configuration file, simply because it is more readable.

#### Comments and JSON5

As of the [v0.9.0](https://github.com/jackdewinter/application_properties/releases/tag/v0.9.0)
release, the `application_properties` package now supports the loading of JSON
configuration files using the standard JSON5 library instead of the standard
JSON library.  While there are five main differences between JSON5 and JSON
outlined in [this article](https://json-5.com/json-vs-json5), we feel that the
most important of those five differences is support for comments.

Having been created in 2001 for the purpose of exchanging data, I doubt that
the authors foresaw a future in which JSON was being used for the wide range
of purposes that it is being used for today.  From a configuration file point
of view, our team feels that one of JSON's weaknesses for representing configuration
is the lack of comments.  While machines and protocols have little use for comments
when exchanging data, having the ability to annotate a JSON file with comments
regarding why a configuration item was set is priceless in terms of understanding
the configuration and potential future debugging.  Given that viewpoint, we feel
that the addition of comments to the JSON5 specification is critical for its
use in the `application_properties` package.

### YAML

Like the JSON file format, the [YAML file format](https://yaml.org/) can
represent hierarchical data. This acronym, standing for the recursive
[YAML Ain't Markup Language](https://en.wikipedia.org/wiki/YAML), removes most
markup characters in favor of a more simplistic approach:

```yaml
plugins:
  md007:
    enabled: true
    code_block_line_length: 160
extensions:
  front-matter:
    enabled: true
```

Here, instead of the `{` and `}` characters of JSON, YAML uses whitespace to
denote hierarchy.  But it does not stop there, as shown in [this tutorial](https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started).

<!-- pyml disable-next-line no-duplicate-heading-->
#### Added Note

From a configuration file viewpoint, it is not useful that YAML files may contain
multiple documents by using a `---` separator to denote a new document. However,
two things that YAML does have that are useful for configuration files are comments
and the string-block character.

Comments are a feature that is particularly useful in configuration files, as shown
in the following example:

```yaml
# See organization standards at https://internal.org.com/standards
plugins:
  md007:
    enabled: true
    code_block_line_length: 160

# Enable front-matter extensions, as MkDocs needs them.
extensions:
  front-matter:
    enabled: true
```

Where the block character (`|`) comes into play is when defining strings that
are long and span multiple lines.  If a string is long and spans multiple lines,
instead of the following (for a made-up Rule Smt001):

```YAML
plugins:
  SMT001:
    response: "Please send any questions\nto our organization mailbox\nat help@internal.org.com"
```

that string can be represented as:

```YAML
plugins:
  SMT001:
    response: |
Please send any questions
to our organization mailbox
at help@internal.org.com"
```

While both forms of the `response` field are equal, the block character field
value is the most readable.

#### Comparison To JSON

Between YAML having fewer moving parts and fewer format
characters, we feel that YAML mostly wins when it comes to readability.  If you
are a fan of using tab characters in configuration files, be aware that YAML
does allow tab characters, but only in situations where indentation does not apply.

The only issue our team has with YAML's readability (hence our statement that YAML
"mostly wins when it comes to readability") is how its string values are interpreted.
For example, in YAML:

```YAML
code_block_line_length: my string
```

is interpreted as a string, and:

```YAML
code_block_line_length: "160"
```

is interpreted as a string, but:

```YAML
code_block_line_length: 160
```

is interpreted as a number.  From our point of view, we would like to
be able to look at YAML field values and to determine their value quickly.
This could easily be mitigated by a team guideline that states that all YAML string
fields must use the `'` or `"` characters to denote the string.

### TOML

Rounding out our list of configuration file formats is the [TOML file format](https://toml.io/en/).
With another acronym, [Tom's Obvious, Minimal Language](https://en.wikipedia.org/wiki/TOML)
has gained support as an easy to read and understand file format.  Keeping with
our established tradition, here is the same configuration presented in TOML
format.

```toml
[plugins.md007]
enabled = true
code_block_line_length = 160

[extensions.front-matter]
enabled = true
```

Not shown in the examples, all strings must be enclosed in either
the "single quote" character (otherwise known as the apostrophe character `'`)
or the quote character (`"`).  Along with providing for comments, it is a nice
middle ground reminiscent of the [Ini File Format](https://en.wikipedia.org/wiki/INI_file)
used on Windows machines.

<!-- pyml disable-next-line no-duplicate-heading-->
#### Added Note

While TOML does not normally support any visible hierarchical structure,
the format of a TOML file does allow for empty sections and indented values.
Those features of TOML allow the following TOML hierarchy to be valid:

```toml
[plugins]
  [plugins.md007]
    enabled = true
    code_block_line_length = 160

[extensions]
  [extensions.front-matter]
    enabled = true
```

even if it is not enforced.  Along those same lines, since the `.` character is
a valid part of a TOML property name, the following hierarchy is also possible:

```toml
[plugins]
md007.enabled = true
md007.code_block_line_length = 160

[extensions]
front-matter.enabled = true
```

<!-- pyml disable-next-line no-duplicate-heading-->
#### Comparison To JSON

After examining the JSON and YAML file formats, TOML is a decent compromise between
the strictness of JSON and the ease of reading of YAML.  However, in our opinion,
this tradeoff comes at the expense of a normal hierarchical
structure.  This tradeoff can be mitigated by one of the examples shown in the last
section, but that mitigation would have to be enforced by the team, not any TOML
tooling.

### Which One Is Best?

The honest answer is that it depends.  Each of the three file formats has its strengths
and weaknesses.  If you and your team have a choice of which file format is best,
we strongly encourage you to look at the above examples and decide which one resonates
the most with your team. If comments are important to you, then JSON is out unless
you enable JSON5 support. If a clearly visible
hierarchy is important to you, TOML is probably out.  If you do not want to remember
the rules for typing strings, YAML is out.

We hope we have done a decent job of showing you the different file formats that
you can use for configuration.  The rest is up to you and your team.  And if you
change your mind in the future, sites like [this one](https://transform.tools/yaml-to-toml)
allow you to change the file format (with caveats) with ease.

## History of Configuration File Support

For those that are interested, this is the journey that our team went on in
providing expansive support for configuration files in multiple roles.
Note that most of this journey was in support of the [PyMarkdown](https://github.com/jackdewinter/pymarkdown)
linter.  However, before making the decision to include that support into
`application_properties`, we evaluated whether the support was a PyMarkdown
feature or a feature that could apply more generally to configuration requirements
from other systems.

### Starting Simple

As with all projects, our team started simply when working on the "parent"
of `application_properties`, the [PyMarkdown](https://github.com/jackdewinter/pymarkdown)
application.  During initial development, we used simple flags and variables to
control what we worked on.  That soon became unwieldy, leading to the development
of the first iteration of `application_properties`.  That is when we started
moving those "flags and variables" into configuration files.

### Specified Configuration Files

The first version of `application_properties` only supported the `--set` command
line option and a single JSON configuration file specified using `--config` on
the command line.  On all projects that our team has worked on, this is
usually the first step towards a more complex configuration system.  The `--set`
option allowed for command line overrides and the `--config` option allowed for
a baseline configuration that could be easily shared.  This also made testing
easier, as we were able to reuse the setup and keep our command lines shorter.

As the users of PyMarkdown got exposure to the singular configuration file, they
requested more types of configuration files.  After making sure that the YAML
and TOML file formats fit our design requirements for `application_properties`
(that any configuration files we support must support string, boolean, and
integer types), we incorporated those file types into `application_properties`.

### Default Configuration Files

Once our team got used to having configuration files, we immediately started wondering
if there was a better way to load the configuration files than using the command
line.  As our primary development was on the PyMarkdown linter, we looked at
other linters, such as PyLint and Flake8.
In most cases, the linters have configuration files that are a single `.` character
followed by their name.  If
these files are present
in the directory where the linter is executed from, it uses the configuration file
without any need for the `--config` argument.

Agreeing with that pattern, we added default configuration file support for
the filename `.pymarkdown` in the current directory.  At that time, we only had
support for JSON file formats, so the
`.pymarkdown` configuration file uses the JSON format.  After implementing that
feature, we received feedback from users that having a default YAML configuration
file would be useful to them.  As such, we added support for the filenames
`.pymarkdown.yml` and `.pymarkdown.yaml` that are YAML configuration files. Because
the configuration file is a default configuration file, our team felt that it was
important to highlight to the user that this default file is a YAML file, not
a JSON file.

### Project Configuration File

Support for the `pyproject.toml` file was added at the request of our users
as a more generic way to support
PyMarkdown configuration.  Depending on the number of tools used by the project
team, the team may feel that their project's root directory has too many configuration
files. The math is simple. If even half the tools have their own default configuration
file
and you are using ten or more tools, your project will contain at least five tool-based
configuration files.  At that point, an alternative project level configuration
file starts to look attractive.

The `pyproject.toml` file is a standard TOML file that uses the `tool.pymarkdown`
section to contain any PyMarkdown configuration items.  The only difference between
using the `pyproject.toml` and a normal TOML configuration file is that the user
must place all configuration items within the `tool.pymarkdown` section.
Therefore, in all cases, the [flattened hierarchical](./getting-started.md#flattened-hierarchical)
form of the configuration item name must be used.

```toml
[tool.pymarkdown]
plugins.md007.enabled = true
plugins.md007.code_block_line_length = 160
extensions.front-matter.enabled = true
```
