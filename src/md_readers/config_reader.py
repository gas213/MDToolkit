import configparser
import os.path

class ConfigReader:
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        if not os.path.isfile(config_path): raise Exception(f"Config file not found at path: {config_path}")
        self.config.read(config_path)
        self._data_path = self.config["DEFAULT"]["DataPath"]

    @property
    def data_path(self):
        return self._data_path