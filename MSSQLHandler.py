import pyodbc

class Credentials:
    username = None
    password = None

    def unfinished(self): return not self.username or not self.password

class ConnectionStringBuilder:
    _credentials = None
    _enableTrustedConnection = False
    _server = None

    def set_credentials(self, credentials):
        self.credentials = credentials
        return self
    def enable_trusted_connection(self):
        self._enable_trusted_connection = True
        return self
    def set_server(self, serverName):
        self._server = serverName
        return self

    def build(self):
        connectionString = "Driver={SQL Server}"
        connectionString += self._write_if_true(self._server, f"Server={self._server};")
        connectionString += self._write_if_true(self._enableTrustedConnection, "Trusted_Connection=yes;")
        connectionString += f"User Id={self._credentials.username};Password={self._credentials.password};" if self._credentials else ""
        return connectionString

    def _write_if_true(self, condition, output): return output if condition else ""

class MSSQLHandler:

    def __init__(self, connectionStringBuilder):
        self._connectionString = connectionStringBuilder.build()
        self.serverName = connectionStringBuilder._server
        self.credentialInfoString = connectionStringBuilder._credentials.username if connectionStringBuilder._credentials else "No user"

    def _execute_query(self, query):
        connection = self._connect()
        results = connection.execute(query)
        connection.close()

        return results

    def _connect(self): return pyodbc.connect(self._connectionString)
