import pyodbc

class Credentials:
    username = None
    password = None

    def unfinished(self): return not self.username or not self.password

class MSSQLHandler:
    def __init__(self):
        print("asd""sd")