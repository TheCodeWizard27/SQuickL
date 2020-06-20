from Config import Config
from pathlib import Path
from MSSQLHandler import *
from ParameterReader import *
from Controllers import *
from getpass import getpass
import sys

class SQuickLHandler:
    _configPath = "config.json"
    _sqlHandler = None

    def __init__(self):
        self.config = Config(self._configPath)
        self.paramReader = ParameterReader(
            "SQuickl (-f=<filePath> | -q=<query>) [-u=<username> -p=<password] [-s=<dbServer>] [-n=<dbName>]",
            {
            "-f": ParameterDefinition("File to be executed."),
            "-lq": ParameterDefinition("Listed Query to be executed. Can be defined under queryList"),
            "-q": ParameterDefinition("Query string to be executed."),
            "-u": ParameterDefinition("Database Username."),
            "-p": ParameterDefinition("Database Password. (requires -u)", ["-u"]),
            "-s": ParameterDefinition("Server address."),
            "-n": ParameterDefinition("Database name."),
            "-t": ParameterDefinition("Enable Trusted Connection Flag.", [], False)
        })

    def run(self):
        try:
            self.paramReader.parse(sys.argv)
            self._sqlHandler = self.build_MSSQLHandler()

            if(self.paramReader.has_value("-f", "-q", "-lq")):
                self.try_executing_file()
                self.try_executing_listed_query()
                self.try_executing_query()                
                return

            self.run_ui_mode()

        except ParameterException as e:
            print(e)
            self.paramReader.print_usage()

    def build_MSSQLHandler(self):
        connectionString = ConnectionStringBuilder()
        connectionString.set_base(self.config.try_get_value("baseConnectionString", "Driver={ODBC Driver 17 for SQL Server};"))
        connectionString.set_server(self.request_database_server())
        
        # If trusted connection is active skip login and return mssqlhandler.
        if(self.request_trusted_connection()):
            connectionString.enable_trusted_connection()
            return MSSQLHandler(connectionString)

        # Request credentials until connection test succeedes or the keyboardinterrupt exception is raised.
        while(True):
            connectionString.set_credentials(self.request_login())
            mssqlHandler = MSSQLHandler(connectionString)
            try:
                mssqlHandler.test_connection()
                return mssqlHandler
            except pyodbc.Error as err:
                print(err)
                print("Failed to log in")

    def run_query(self, query):
        output = self._sqlHandler.execute_query(query)
        print("Results:")
        input(output)

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

    def try_executing_file(self):
        file = self.paramReader.try_get_value("-f", None)
        if(not file): return

        with Path(file).open() as file:
            self.run_query(file.read())
    
    # Executes a query that is defined in the set query list.
    def try_executing_listed_query(self):
        queryKey = self.paramReader.try_get_value("-lq", None)
        
        if(not queryKey): return
        self.run_query(self.config.get_value("queryList")[queryKey])

    def try_executing_query(self):
        query = self.paramReader.try_get_value("-q", None)
        if(not query): return

        self.run_query(query)
