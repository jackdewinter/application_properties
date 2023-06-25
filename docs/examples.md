# Examples

Before we get into some examples, we need to talk about property names.

## Property Names

There are many ways, both linear and hierarchical, of specifying the name of a
given property.  Instead of trying to integrate multiple models of property names,
this package instead maps any hierarchical model onto a normalized linear property
name.

What does that mean?  A simple property name like `log.file` is a linear property
names as it can clearly be expressed using a simple linear format.  For this project,
those property names are composed of one or more "property name parts" that are
joined together with a `.` character.  Therefore, the `log.file` property name
references a `file` property that occurs within a `log` context.  We also refer
to this format as a flattened hierarchical context, as it squashes a more complex
hierarchy into a simplce linear string.

From a naming point of view, this format helps to group similar settings together
under a given context.  There is nothing stopping people from using `log_file` as
the property name, forgoing any benefits of a joint context.  On the other hand,
there is also nothing preventing people from using a property name like
`assembly.namespace.class.method.line` if they wish to represent a more complex
hierarchical configuration.  The choice of how to use our flattened hierarchical
context is up to the writer of the application.

parts
" ", "\t", "\n", "=" and of course "."

## XXX

property_names
property_names_under
number_of_properties
clear

valid value
strict mode

get_boolean_property
get_integer_property

## Example 1: Getting Properties

The simplest example of this package is the following code:

```python
properties = ApplicationProperties()
value = application_properties.get_property("something", str)
assert value == None
```

While the code is somewhat meaningless, it helps to talk about what is going on
behind the scenes.  The `ApplicationProperties` class holds information about the
configuration names and values.  Without any method calls to populate the instance
of that class with any manner of information, every valid attempt to retrieve a
property from that instance will return a `None` value.

However, if we make a small change to that code:

```python
properties = ApplicationProperties()
value = application_properties.get_property("something", str, "(None)")
assert value == "(None)"
```

the returned value is now the string `(None)`.  This is because the third value
to the `get_property` method is the `default_value` parameter.  This parameter
specifies the value to use if no value is found in the `ApplicationProperties`
instance.

## Example 2: Setting Properties Manually

To make Example 1 a bit more interesting, we can add property information to the
`ApplicationProperties` instance with the following code:

```python
properties = ApplicationProperties()

properties_to_set = ["something=else", "someone=2love"]
properties.set_manual_property(properties_to_set)

value = application_properties.get_string_property("something")
assert value == "else"
```

The first thing to point out with this code is that we substituted the call to
the `get_property` method with a call to the `get_string_property`.  Under the
covers, the `get_string_property` method calls into the `get_property` method with
the `property_type` parameter set to `str`.  This method is provied as a convenient
shorthand for the users.

The second thing of note is that the variable `properties_to_set` is set with a list
of two strings, each one in the form of `name=value`.  This variable is then passed
into the `set_manual_property` method.  The `set_manual_property` accepts both
a single string in this format and a list of strings in the format.  While this
may be cumbersome for large amounts of information, we find it works well for setting
one or more property values from the command line.

## Example 3: Loading Values From A Dictionary + Required

While the use of the `set_manual_property` method in Example 2 works, its flat format
is cumbersome and hard to use.  To that end, this example introduces the `load_from_dict`
method:

```python
properties = ApplicationProperties()

config_map = {"enabled": True}
properties.load_from_dict(config_map)

value = application_properties.get_boolean_property("enabled", required=True)
assert value == True
```

That method takes as its parameter a normal Python `dict` object and uses that object
to populate the provided instance of the `ApplicationProperties` class.  Any dictionary
object can be used as long as all keys in the dictionary and sub-dictionaries are of
type `str`.

## XX

```python
properties = ApplicationProperties()
config_map = {"feature": {"enabled": True}}
properties.load_from_dict(config_map)
value = application_properties.get_property("feature.enabled", bool)
assert value == True
```

## XX

```python
def __sample_string_validation_function(property_value):
    """
    Simple string validation that throws an error if not "1" or "2".
    """
    if property_value not in ["1", "2"]:
        raise ValueError(f"Value '{str(property_value)}' is not '1' or '2'")

properties = ApplicationProperties()
config_map = {"property": "3"}
properties.load_from_dict(config_map)
application_properties.get_property(
    "property",
    str,
    valid_value_fn=__sample_string_validation_function,
    )
```

## XX - ApplicationPropertiesJsonLoader

## XX - ApplicationPropertiesConfigLoader

## XX - ApplicationPropertiesTomlLoader

## XX - Facade

## strict mode

xxxx
