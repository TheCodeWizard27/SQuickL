import pyodbc

class Credentials:
    username = None
    password = None

    def unfinished(self): return not self.username or not self.password

class ConnectionStringBuilder:
    _credentials = None
    _enableTrustedConnection = False
    _server = None

    def setCredentials(self, credentials):
        self.credentials = credentials
        return self
    def enableTrustedConnection(self):
        self._enableTrustedConnection = True
        return self
    def setServer(self, serverName):
        self._server = serverName
        return self

    def build(self):
        connectionString = "Driver={SQL Server}"
        connectionString += self._writeIfTrue(self._server, f"Server={self._server};")
        connectionString += self._writeIfTrue(self.enableTrustedConnection, "Trusted_Connection=yes;")
        connectionString += f"User Id={self._credentials.username};Password={self._credentials.password};" if self._credentials else ""
        return connectionString

    def _writeIfTrue(self, condition, output): return output if condition else ""

class MSSQLHandler:

    def __init__(self, connectionStringBuilder):
        self._connectionString = connectionStringBuilder.build()
        self.serverName = connectionStringBuilder._server
        self.credentialInfo = connectionStringBuilder._credentials.username if connectionStringBuilder._credentials else "No user"

    def executeQuery(self, query):
        connection = self._connect()
        results = connection.execute(query)
        connection.close()

        return results

    def _connect(self):
        return pyodbc.connect(self._connectionString)
