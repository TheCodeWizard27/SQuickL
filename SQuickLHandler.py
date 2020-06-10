from Config import Config
from MSSQLHandler import *
from ParameterReader import *
from Getch import getChar
from SelectionHandler import *
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
            "-t": ParameterDefinition("Enable Trusted Connection Flag.", [], False)
        })

    def run(self):
        try:
            connectionString = ConnectionStringBuilder()
            self.paramReader.parse(sys.argv)

            connectionString.setServer(self.requestDatabaseServer())

            if(self.requestTrustedConnection()):
                connectionString.enableTrustedConnection()
            else:
                connectionString.setCredentials(self.requestLogin())
            
            sqlHandler = MSSQLHandler(connectionString)
            self.requestAction(sqlHandler)    

        except ParameterException as e:
            print(e)
            self.paramReader.printUsage()

    def requestAction(self, sqlHandler):
        handler = SelectionHandler([
            SelectableItem("Execute Query", "s"),
            SelectableItem("Manual", "s"),
            SelectableItem("Quit", "s")
        ])

        while(True):
            self._clearScreen()
            print(F"SQuickL [{sqlHandler.credentialInfo}@{sqlHandler.serverName}]")
            
            handler.draw()
            key = getChar()

            if(key == b'\r'): return # Enter
            if(key == b'P'): handler.selectNext() # Arrow Up
            if(key == b'H'): handler.selectPrev() # Arrow Down
            if(key == b'\x03'): raise Exception() # Return ctrl+c functionality.

    def requestTrustedConnection(self):
        setTrustedConnection = self.config.tryGetValue("trustedConnection", False)
        setTrustedConnection = self.paramReader.tryGetValue("-t", setTrustedConnection)

        return setTrustedConnection

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
        databaseServer = self.config.tryGetValue("server", None)
        databaseServer = self.paramReader.tryGetValue("-s", databaseServer)

        if(databaseServer): return databaseServer
        return input("Db Server:")

    def requestInputIfNone(self, ref, displayText):
        return ref if ref else input(displayText) # Request input if not already defined.

    def _clearScreen(self): print(chr(27) + "[2J")
