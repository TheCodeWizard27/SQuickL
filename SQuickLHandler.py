from Config import Config
from MSSQLHandler import *
from ParameterReader import *
import sys

class SQuickLHandler:
    _configPath = "config.json"

    def __init__(self):
        self.config = Config(self._configPath)
        self.paramReader = ParameterReader(
            "SQuickl (-f=<filePath> | -q=<query>) [-u=<username> -p=<password] [-s=<dbServer>] [-n=<dbName>]",
            {
            "-f": ParameterDefinition("File to be executed."),
            "-q": ParameterDefinition("Query to be executed."),
            "-u": ParameterDefinition("Database Username."),
            "-p": ParameterDefinition("Database Password. (requires -u)", ["-u"]),
            "-s": ParameterDefinition("Server address."),
            "-n": ParameterDefinition("Database name."),
        })

    def run(self):
        try:
            self.paramReader.parse(sys.argv)
            databaseServer = self.requestDatabaseServer()
            credentials = self.requestLogin()
            MSSQLHandler()

        except Exception as e:
            print(e)
            self.paramReader.printUsage()

    def requestLogin(self):

        credentials = Credentials()
        inputFunctions = []

        credentials.username = self.paramReader.tryGetValue("-u", None)
        credentials.password = self.paramReader.tryGetValue("-p", None)
        
        if(not credentials.unfinished()): return credentials # If Credentials are already set by other methods just return them.

        print("[ Please Login ]")
        credentials.username = self.requestInputIfNone(credentials.username, "Username: ")
        credentials.password = self.requestInputIfNone(credentials.password, "Password: ")
        return credentials

    def requestDatabaseServer(self):
        databaseServer = self.paramReader.tryGetValue("-s", None)

        if(databaseServer): return databaseServer
        return input("Database Server:")


    def requestInputIfNone(self, ref, displayText):
        return ref if ref else input(displayText) # Request input if not already defined.
