from Config import Config
from MSSQLHandler import *
from ParameterReader import *
from Controllers import *
from getpass import getpass
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
            "-qs": ParameterDefinition("Query string to be executed."),
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

            connectionString.set_server(self.request_database_server())

            if(self.request_trusted_connection()):
                connectionString.enable_trusted_connection()
            else:
                connectionString.set_credentials(self.request_login())
            
            sqlHandler = MSSQLHandler(connectionString)

            if(self.paramReader.has_value("-f", "-q", "-qs")):
                return

            self.run_ui_mode()

        except ParameterException as e:
            print(e)
            self.paramReader.print_usage()

    def run_ui_mode(self):
        controller = MainController(self)

        while(True):
            if(not controller): return # Quit program if no controller available.
            controller = controller.control_input()

    def request_trusted_connection(self):
        setTrustedConnection = self.config.try_get_value("trustedConnection", False)
        setTrustedConnection = self.paramReader.try_get_value("-t", setTrustedConnection)

        return setTrustedConnection

    def request_login(self):

        credentials = Credentials()
        inputFunctions = []

        credentials.username = self.paramReader.try_get_value("-u", None)
        credentials.password = self.paramReader.try_get_value("-p", None)
        
        if(not credentials.unfinished()): return credentials # If Credentials are already set by other methods just return them.

        print("[ Please Login ]")
        credentials.username = self.request_input_if_none(credentials.username, "Username: ")
        credentials.password = self.request_input_if_none(credentials.password, "Password: ", getpass)
        return credentials

    def request_database_server(self):
        databaseServer = self.config.try_get_value("server", None)
        databaseServer = self.paramReader.try_get_value("-s", databaseServer)

        if(databaseServer): return databaseServer
        return input("Db Server:")

    def request_input_if_none(self, ref, displayText, inputFunc = input):
        return ref if ref else inputFunc(displayText) # Request input if not already defined.
