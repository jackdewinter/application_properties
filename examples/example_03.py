import os
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()))  # isort:skip

from application_properties import (
    ApplicationProperties,
    ApplicationPropertiesJsonLoader,
)

properties = ApplicationProperties()
ApplicationPropertiesJsonLoader.load_and_set(
    properties, os.path.join(os.path.dirname(__file__), "example_data.json")
)
print(properties.get_string_property("my_other_property", default="2"))
