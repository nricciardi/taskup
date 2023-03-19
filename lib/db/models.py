from lib.db.db_manager import DBManager
from abc import ABC, abstractmethod, abstractproperty


class Model(DBManager, ABC):
    table_name: str = ""

    def __init__(self):
        pass

    def all(self) -> list:
        """
        Return all records from db table

        :return: All records from db table
        :rtype: list
        """

        res = self.db_cursor.execute(f"Select * From {self.table_name}")

        return res.fetchall()

    def find(self, id: int) -> dict:
        """
        Return the record requested

        :param id: the record's id
        :type id: int
        :return:
        """

        res = self.db_cursor.execute(f"Select * From {self.table_name} Where {self.table_name}.id = {id}")

        return res.fetchone()


class Task(Model):

    def __int__(self):
        pass


class User(Model):
    table_name: str = "user"

    def __int__(self):
        super().__int__()
