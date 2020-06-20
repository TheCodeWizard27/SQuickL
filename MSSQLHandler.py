import pyodbc

class Credentials:
    username = None
    password = None

    def unfinished(self): return not self.username or not self.password

class ConnectionStringBuilder:
    _credentials = None
    _enableTrustedConnection = False
    _server = None
    _base = ""

    def set_base(self, base):
        self._base = base
        return self
    def set_credentials(self, credentials):
        self._credentials = credentials
        return self
    def enable_trusted_connection(self):
        self._enableTrustedConnection = True
        return self
    def set_server(self, serverName):
        self._server = serverName
        return self

    def build(self):
        connectionString = self._base #"Driver={ODBC Driver 17 for SQL Server};"
        connectionString += self._write_if_true(self._server, f"Server={self._server};")
        connectionString += self._write_if_true(True, "DATABASE=test;")
        connectionString += self._write_if_true(self._enableTrustedConnection, "Trusted_Connection=yes;")
        connectionString += f"UID={self._credentials.username};PWD={self._credentials.password};" if self._credentials else ""
        return connectionString

    def _write_if_true(self, condition, output): return output if condition else ""

class MSSQLHandler:

    def __init__(self, connectionStringBuilder):
        self._connectionString = connectionStringBuilder.build()
        self.serverName = connectionStringBuilder._server
        self.credentialInfoString = connectionStringBuilder._credentials.username if connectionStringBuilder._credentials else "No user"

    def execute_query(self, query):
        connection = self._connect()
        results = None

        try:
            cursor = connection.execute(query)
            results = cursor.fetchall() 
        except pyodbc.Error as err:
            results = err
        finally:
            connection.close()

        return results

    # Will do a basic version query to check if the connection works.
    def test_connection(self): self.execute_query("SELECT @@version;")

    def _connect(self): return pyodbc.connect(self._connectionString)
