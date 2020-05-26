from pathlib import Path
import json

class Config:
    
    _configValues = {
        "testValue": True
    }

    def __init__(self, configPath):
        self.tryLoading(configPath)

    def tryLoading(self, configPath):
        configFile = Path(configPath)
        if(not configFile.exists()): return

        with configFile.open() as file:
            configJson = json.loads(file.read())
            for key, value in configJson.items(): 
                self._configValues[key] = value

    def getValue(self, path):
        return self._configValues[path]

    def tryGetValue(self, path, default):
        if(path not in self._configValues): return default
        return self._configValues[path]