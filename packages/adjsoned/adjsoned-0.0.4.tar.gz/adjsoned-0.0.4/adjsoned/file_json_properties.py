import json
import os

from .json_properties import JsonProperties


class FileJsonProperties(JsonProperties):
    """
    Initializes a JsonProperties object with raw data loaded from file.

    :param filepath: properties file path
    :type filepath: str
    """

    _filepath: str

    def __init__(self, filepath="some_properties.json"):
        self._filepath = filepath
        self.load_file_data()
        super().__init__()

    def load_file_data(self):
        """
        Loads raw json into this object's private temporary member in order for the super class to absorb it.
        """

        with open(self._filepath, "r") as file:
            loaded_json_data = json.load(file)
            assert isinstance(loaded_json_data, dict), "Root JSON-Object of your properties should be a dictionary"
            self._loaded_json_data = loaded_json_data

    def update(self, new_filepath: str = None):
        """
        Reloads and reabsorbs raw json data from the associated file.

        :param new_filepath: new properties file path that overrides the existing one if passed and exists
        :type new_filepath: str
        """

        if new_filepath and os.path.exists(new_filepath):
            self._filepath = new_filepath

        self.load_file_data()
        super()._absorb_data()
