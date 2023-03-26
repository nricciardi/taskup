import sqlite3
from lib.db.db_manager import DBManager
from abc import ABC, abstractmethod
from lib.utils.base import Base, BEM
from lib.entity.bem import BaseEntityModel
from typing import Any


class EntityManager(DBManager, ABC):
    """
    Abstract class to manage DB's entities
    """

    db_use_localtime: bool = False

    def __init__(self, table_name: str, db_name: str, work_directory_path: str, verbose: bool = False):

        self.__table_name = table_name
        self.__db_name = db_name
        self.__verbose = verbose

        super().__init__(db_name=self.__db_name, work_directory_path=work_directory_path, verbose=verbose,
                         use_localtime=self.db_use_localtime)

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

            msg = f"{data} must be an implementation of BaseEntityModel"

            Base.log_error(message=msg, is_verbose=self.__verbose)

            raise TypeError(msg)

    def all(self) -> list:
        """
        Return all records from db table

        :return: All records from db table
        :rtype: list
        """

        res = self.__db_cursor.execute(f"Select * From {self.table_name};")

        return res.fetchall()

    def find(self, entity_id: int) -> tuple:
        """
        Return the record requested

        :param entity_id: the record's id
        :type entity_id: int

        :return: entity record
        :rtype tuple:
        """

        res = self.cursor.execute(f"Select * From {self.table_name} Where {self.table_name}.id = {entity_id};")

        data = res.fetchone()

        return data

    def create(self, data: dict) -> BEM:
        """
        Create a new record

        :param data: dict represent entity data
        :type data: Entity dataclass

        :return: entity created
        :rtype BEM:
        """

        query = self.__generate_create_query(data)      # it is here to use its in except

        try:

            values = list(data.values())
            self.cursor.execute(query, values)

            self.connection.commit()

            # call explicitly find to prevent use of override
            entity = EntityManager.find(self, self.cursor.lastrowid)

            return entity

        except Exception as exception:

            Base.log_error(message=f"{exception} during execute: {query}\nwith {data}", is_verbose=self.__verbose)

            raise exception

    def __generate_create_query(self, data: dict) -> str:
        """
        Generate the query for create method

        :param data: key-value data of entity
        :type data: dict

        :return: SQL query
        :rtype str:
        """

        # Extract the keys and values from the dictionary
        keys = list(data.keys())
        values = list(data.values())

        # Construct the query string with placeholders for the values
        fields = ','.join(keys)
        placeholders = ','.join(['?'] * len(values))

        query_string = f"Insert Into {self.table_name} ({fields}) Values ({placeholders})"

        return query_string
