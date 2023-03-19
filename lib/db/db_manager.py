import sqlite3


class DBManager:
    def __init__(self, db_name: str):

        self.__db_name: str = db_name

        self.__db_connection = sqlite3.connect(self.__db_name)
        self.__db_cursor = self.__db_connection.cursor()

    @property
    def db_name(self) -> str:
        return self.__db_name

    @db_name.setter
    def db_name(self, name: str) -> None:
        self.__db_name = name

    @db_name.deleter
    def db_name(self):
        raise Exception("db_name cannot be deleted")
