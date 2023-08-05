from . import _text_processing


class JsonProperties:
    """
    Allows for loading JSON files into Python objects of type JsonProperties.
    JSON key-value pairs can be thus accessed through the "." notation as this object's fields.

    :param json_data: required if the constructor gets called not by some child that has already loaded the raw data
    :type json_data: dict

    :param pythonify_entry_keys: whether json file camel-cased keys should reflect python naming recommendations
    when accessing them through the "." notation
    :type pythonify_entry_keys: bool

    :param title: usually a key at which this object was stored in json data
    :type title: str
    """

    _loaded_json_data: dict
    _pythonify_entry_keys: bool
    _title: str

    def __init__(self, json_data: dict = None, pythonify_entry_keys=True, title=""):
        if json_data is None and not self._loaded_json_data:
            json_data = {}

        self._loaded_json_data = json_data or self._loaded_json_data
        self._pythonify_entry_keys = pythonify_entry_keys
        self._title = title

        self._absorb_data()

    @property
    def properties_title(self):
        return self._title

    def _absorb_data(self, clear_raw_data=True):
        """
        Absorbs raw json data into itself making key-value pairs accessible through python's . notation.

        :param clear_raw_data: whether raw data memory should be freed up after absorption. Does not affect source file!
        :type clear_raw_data: bool
        """

        assert self._loaded_json_data is not None, "Unable to absorb a None-object's data"

        for entry_key in self._loaded_json_data:
            if entry_key.startswith("_"):
                print(f"Aborted loading the entry '{entry_key}': underscore entry keys aren't allowed!")

            entry = self._loaded_json_data[entry_key]

            if self._pythonify_entry_keys:
                entry_key = _text_processing.pythonify_name(entry_key)

            if isinstance(entry, dict):
                entry = JsonProperties(entry, title=entry_key)

            if isinstance(entry, list):
                entry = [JsonProperties(el, title=f"{entry_key}:{i}") if isinstance(el, dict) else el
                         for i, el in enumerate(entry)]

            self.__dict__[entry_key] = entry

        if clear_raw_data:
            self._loaded_json_data = {}
    def __contains__(self, item):
        if self._pythonify_entry_keys:
            item = _text_processing.pythonify_name(item)

        return item in self.__dict__

    def __getitem__(self, item):
        if self._pythonify_entry_keys:
            item = _text_processing.pythonify_name(item)

        if item in self:
            return self.__dict__[item]

        return None

    def __setitem__(self, key, value):
        if self._pythonify_entry_keys:
            key = _text_processing.pythonify_name(key)

        self.__dict__[key] = value

    def __str__(self) -> str:
        return f"JsonProperties('{self._title}', {self._loaded_json_data})"
