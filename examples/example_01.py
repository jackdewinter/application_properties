import os
import sys

sys.path.insert(0, os.path.abspath(os.getcwd()))  # isort:skip

from application_properties import ApplicationProperties

properties = ApplicationProperties()
print(properties.get_string_property("my_property"))
