from pathlib import Path
import json

# Enables loading through a config.json File.
class Config:
    _configValues = {}

    def __init__(self, configPath):
        self.try_loading(configPath)

    def try_loading(self, configPath):
        configFile = Path(configPath)
        if(not configFile.exists()): return

        with configFile.open() as file:
            configJson = json.loads(file.read())
            for key, value in configJson.items():
                self._configValues[key] = value

    def get_value(self, path):
        return self._configValues[path]

    def try_get_value(self, path, default):
        if(path not in self._configValues): return default
        return self._configValues[path]