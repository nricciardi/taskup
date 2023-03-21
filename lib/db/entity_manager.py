from lib.db.db_manager import DBManager
from abc import ABC, abstractmethod


class EntityManager(DBManager, ABC):
    """
    Abstract class to manage DB's entities
    """

    def __init__(self, table_name: str, db_name: str, work_directory_path: str, verbose: bool = False):

        self.__table_name = table_name
        self.__db_name = db_name

        super().__init__(db_name=self.__db_name, work_directory_path=work_directory_path, verbose=verbose)

    @property
    def table_name(self) -> str:
        """
        Return table name

        :rtype: str
        """

        return self.__table_name

    @table_name.setter
    def table_name(self, value) -> None:
        """
        Change entity

        :param value: table name of entity
        """

        self.__table_name = value

    def all(self) -> list:
        """
        Return all records from db table

        :return: All records from db table
        :rtype: list
        """

        res = self.__db_cursor.execute(f"Select * From {self.table_name}")

        return res.fetchall()

    def find(self, entity_id: int) -> dict:
        """
        Return the record requested

        :param entity_id: the record's id
        :type entity_id: int
        :return:
        """

        res = self.__db_cursor.execute(f"Select * From {self.table_name} Where {self.table_name}.id = {entity_id}")

        return res.fetchone()

    def insert(self,):
        pass