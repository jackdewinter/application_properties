# Basic Concepts

In this document, we define the concepts that we believe are important
in the `application_properties` package.
This document is meant to be bridge between the [Index](./index.md), where we talk
about this package at a high level, and the [User Guide](./user-guide.md),
where we walked you through the code required to interact with this package from
your project.

Note that while it is possible to jump ahead to the [User Guide](./user-guide.md),
we strongly encourage you to at least scan this document to gain familiarity
with the nomenclature and ideas presented here.  As the other documents use
terminology specified in this document, even a cursory scan of this document may
avoid
future trips back to this document.  But in the end, please use these documents
in a manner that works for you and how you learn.

## Nomenclature

Before progressing through the rest of the documentation, we feel that it is necessary
to clearly describe the more important words and phrases we will be using.

### Configuration Item

A pairing of the rank and name of the configuration item along with its value. This
is the fundamental unit of configuration data. Its name is inherently **hierarchical**,
describing its context, while its value component is a typed value. This pairing
can be thought of as a `key-value` pair, as that is how these configuration items
will typically be represented. At its core, the configuration item represents the
user's logical intent for configuring the application.

### Configuration Data Sources

The physical files or inputs that contain zero or more configuration items. The
currently supported data sources are configuration files (JSON, TOML, and YAML),
and command-line values in `key=value` format.

### Configuration Manager

A component that takes care of managing multiple configuration data
sources and represents them as a logical and coherent set of configuration items.
For this package, the configuration manager is the `ApplicationProperties` class.

### Configuration Loader

This is a component that obfusicates the boilerplate code that is required to load
each type of configuration data, presenting a single point of entry for loading
configuration data of a given type. These configuration loaders break down Configuration
Data Sources into a structured and indexable format that
the `ApplicationProperties` class is capable of processing as an input.

### Getter Methods

These are methods of the `ApplicationProperties` class that look for a given key
stored within
the configuration manager. By default, if the specified configuration item is present
and
of the correct type, the value associated with the key is returned as a property.
If that
value is not present, then the returned property is the default value provided to
the getter method.

### Property

This is the value rendered as a typed value in Python by using the getter methods
from an instance of the `ApplicationProperties` class.

## Our Philosophy of "Work By Default"

After taking stock of the requirements that we needed from a configuration manager,
our team set out to create a configuration manager that we could feel proud of.
Given
our internal list of requirements, we
worked to balance the need for multiple sources of truth with the ability
to efficiently present that data to the application.  In the end, we are
pleased that we built a solid configuration manager that
meets our needs and has room for future extension.

While a lot of the decisions were easy, it took us a while to arrive at
the decision that we wanted our configuration manager to "work by default".
We use the phrase "work by default" as we have seen systems designed with
configuration managers that are extremely strict about what they accept. When
evaluating certain configuration packages, we found that we spent 5-10 minutes
setting various configuration items
before we
were able to figure out if that package worked for us.  We wanted to avoid giving
our users that sense of exasperation, if possible.

The choice of whether to be strict on the configuration data being used is both
an application decision and a personal decision. Some applications require their
configuration to be just-so, and some people have had configuration issues in their
past that make them wary of "hidden" defaults. Therefore, by default, `application_properties`
starts off "working by default", but has both global-based and getter-based settings
to enable strict mode.

## Structure and Composition

**Note:** The information in this section is complimented by the
[Quick Start: Configuration Hierarchy](./quick-starts/hierarchy.md) page.

### Hierarchical

The word [hierarchy](https://www.merriam-webster.com/dictionary/hierarchy) has many
definitions.  The one that comes closest to our use of it is:

> a ruling body of clergy organized into orders or ranks each subordinate to the
> one above it

Our configuration manager is hierarchical because it organizes its data into ranks,
where each rank determines the context of the rank below it.  For example, each
group
of top-level items has a subordinate group of items below them, and those subordinate
items may also have their own subordinate items.

### Flattened Hierarchical

While a tradition hierarchy is often expressed in a form such as:

```text title="traditional hierarchy"
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

```text title="flattened hierarchy"
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
**The name component of any Configuration Item is represented using this flattened
format.**

### Layered

The word `layered` implies that something has multiple distinct parts to it.  For
our configuration manager, we designed a data store that can manage input from various
sources, assigning each of those types of data sources to a given "layer".  When
viewed from an external point of view, these layers collapse to provide a single
view of the configuration data.

## Primitve Elements

When referencing the 'value' component of any configuration item, the default assumption
for its type is a **String Value**, as defined earlier. This default remains true
unless the mechanism used to retrieve the value (i.e., a specific getter method implemented
on the `ApplicationProperties` object) explicitly enforces a different type, such
as a `boolean` or `integer`.

Keep in mind that here we are talking about the `value` part of a `key-value`
pair.
It is only when a getter function renders the value that it becomes a property.

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

#### Case-insensitive

This refers to a comparison that is done without respect to the case of any
characters in the given string.  Using a case-insensitive comparison,
`False`, `false`, `FALSE`, and `FaLsE` are all equal.

### String List Value

A string list value is a value that is a list of zero or more strings. These values
are useful in situations where a single string does not accurately specify the configuration
item.

Note that this value is currently unique in that it accepts two forms of values
derived from the configuration data. The first form is a string value, as outlined
above,
that has a defined separateor that defines where one string in the list stops and
where
the next string begins.  Depending on whether the source of the configuration data
supports it, a second form is a list of objects in that data source's native format.

For example, this example of the first form using a YAML format:

```yaml title="string list - string form"
item: value1,value2
```

can also be represented by the following YAML format:

```yaml title="string list - list form"
item:
    - value1
    - value2
```
