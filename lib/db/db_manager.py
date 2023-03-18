import sqlite3


class DBManager:
    def __int__(self, db_name: str):
        self.db_name = db_name
        self.db_connection = sqlite3.connect(self.db_name)
        self.db_cursor = self.db_connection.cursor()

