# Advanced Examples

## Property Names

- strings separated by "."

```Python
self.__properties.get_string_property("log.file")
```

## Property Value Types

- default are strings
- integers and boolans currently available

<!-- pyml disable-next-line no-multiple-space-atx-->
## Property Value Modifiers

```Python
    default_value=None,
    valid_value_fn=None,
    is_required=False,
    strict_mode=None,
```

```Python
            effective_log_level = self.__properties.get_string_property(
                "log.level", valid_value_fn=PyMarkdownLint.log_level_type
            )
```

## Hierarchical

- facades

```Python
    section_facade_candidate = ApplicationPropertiesFacade(
        properties, plugin_section_title
    )
```

- property_names and property_names_under

## Other

strict mode

```Python
    effective_strict_configuration = self.__properties.get_boolean_property(
        "mode.strict-config", strict_mode=True
    )
    self.__properties.enable_strict_mode()
```

## Loaders

- properties_object.load_from_dict(configuration_map)
