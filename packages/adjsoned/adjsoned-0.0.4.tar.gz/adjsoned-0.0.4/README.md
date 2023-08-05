# Adjsoned
This Python library can help you easily load your program's configuration/properties
from a json file to a Python runtime object making key-value data accessible via
python's "." syntax—as these key-value pairs were fields of this object.

### Installation
```
pip install adjsoned
```

### Get started
Instantiate a FileJsonProperties object giving it your config file's path and it will just work:

```Python
from adjsoned import FileJsonProperties


properties = FileJsonProperties(filepath="examples/some_properties.json")

# We can now access key-value/arrays data stored in our JSON file the following way:
# (NB: the ROOT element of your JSON file MUST be a DICT!)

if properties.debug_mode:
    print("We're in debug mode!")
    print("P.S. Properties told me that :)")

# 'properties' is an instance of FileJsonProperties (as well as JsonProperties — a parent class)
# 'properties.app_version' is also a JsonProperties instance, so we can access its fields like that:
print(properties.app_version.code)  # prints '4.1.2'

# arrays are interpreted as regular Python lists, you can just normally iterate through them:
for section in properties.project_settings.ignored_sections:
    print("Ignoring section", section)

# if an array element is a dictionary, it gets interpreted as a JsonProperties object as well:
print(properties.messages[1].title)  # prints: 'Hello again.'
```

The JSON file used in this example:
```json
{
  "debugMode": true,

  "appVersion": {
    "code": "4.1.2",
    "build": 2
  },

  "projectSettings": {
    "frameRate": 60,
    "ignoredSections": [2, 6, 9]
  },

  "messages": [
    {
      "title": "Hello!",
      "description": "This is the first message."
    },
    {
      "title": "Hello again.",
      "description": "This is the second one. Nice to see you again!"
    }
  ]
}
```