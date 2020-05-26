from Config import Config
from MSSQLHandler import MSSQLHandler
from ParameterReader import *
import sys

class SQuickLHandler:
    _configPath = "config.json"

    def __init__(self):
        self.config = Config(self._configPath)
        self.paramReader = ParameterReader({
            "-a": ParameterDefinition(),
            "-b": ParameterDefinition()
        })
        print(sys.argv)
        self.requestLogin()

    def requestLogin(self):
        print("[ Please Enter Your Username ]")
        username = input("Username: ")
        password = input("Password: ")

