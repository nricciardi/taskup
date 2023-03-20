import sqlite3
from lib.utils.base import Base


class DBManager:
    def __init__(self, db_name: str, work_directory: str = ".", verbose: bool = False):

        self.verbose = verbose
        self.__db_name: str = db_name
        self.__work_directory: str = work_directory

        try:
            print(self.__db_name)
            self.__db_connection = sqlite3.connect(self.__db_name)
            self.__db_cursor = self.__db_connection.cursor()

        except Exception as error:
            print("Connection with database failed...")

            if self.verbose:
                Base.log_error(error)

            Base.exit()

    @property
    def db_name(self) -> str:
        return self.__db_name

    @db_name.setter
    def db_name(self, name: str) -> None:
        self.__db_name = name

    @db_name.deleter
    def db_name(self):
        raise Exception("db_name cannot be deleted")
