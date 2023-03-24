import sqlite3
from lib.db.db_manager import DBManager
from abc import ABC, abstractmethod
from lib.utils.base import Base
from lib.entity.bem import BaseEntityModel
from typing import Any


class EntityManager(DBManager, ABC):
    """
    Abstract class to manage DB's entities
    """

    def __init__(self, table_name: str, db_name: str, work_directory_path: str, verbose: bool = False):

        self.__table_name = table_name
        self.__db_name = db_name
        self.__verbose = verbose

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

    def __is_valid_model_data_type(self, data: Any) -> bool:
        """
        Return True if data is a subclass of BaseEntityModel, otherwise False

        :param data: data to check
        :type data: Any

        :return: result of check
        :rtype bool:
        """

        return issubclass(data.__class__, BaseEntityModel)

    def __validate_model_data_type(self, data: Any):
        """
        Raise exception if param data is not a subclass of BaseEntityModel

        :param data: data to check
        :type data: Any

        :return:
        """

        if not self.__is_valid_model_data_type(data):

            error = f"{data} must be an implementation of BaseEntityModel"

            if self.__verbose:
                Base.log_error(error)

            raise TypeError(error)

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

    def create(self, data: dict) -> BaseEntityModel:
        """
        Create a new record

        :param data: dict represent entity data
        :type data: Entity dataclass

        :return: Creation result
        :rtype bool:
        """

        query = self.__generate_create_query(data)

        try:

            self.cursor.execute(query, data)

            self.connection.commit()

        except sqlite3.Error as exception:

            if self.__verbose:
                Base.log_error(f"{exception} during execute: {query} \n\twith {data}")

            raise exception

        return True

    def __generate_create_query(self, data: dict) -> str:
        """
        Generate the query for create method

        :param data: key-value data of entity
        :type data: dict

        :return: SQL query
        :rtype str:
        """

        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in range(len(data))])

        query = f"""
                                INSERT INTO {self.table_name} VALUES ({keys})
                                ({placeholders})
                            """

        return query
