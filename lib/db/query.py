from abc import ABC
from typing import Any, List, Generic, TypeVar, Dict, Tuple
from lib.db.component import WhereCondition
from lib.utils.mixin.sql import ToSqlInterface


class QueryBuilder(ToSqlInterface, ABC):
    query: str = ""
    __has_where: bool = False
    __binding: bool = False

    @property
    def binding(self) -> bool:
        return self.__binding

    @binding.setter
    def binding(self, value: bool):
        self.__binding = value

    def __init__(self, table_name: str, alias: str | None = None, binding_mode: bool = False):
        if alias is not None:
            table_name = f"{table_name} as {alias}"

        self.table_name = table_name
        self.binding = binding_mode
        self.data_bound = []

    @classmethod
    def from_table(cls, table_name: str, alias: str | None = None, binding_mode: bool = __binding) -> 'QueryBuilder':
        """
        More expressive constructor alias

        :param binding_mode:
        :type binding_mode: bool
        :param table_name:
        :type table_name: str
        :param alias: table alias
        :type alias: str
        :return:
        """

        return cls(table_name, alias, binding_mode)

    def select(self, *columns: str) -> 'QueryBuilder':
        """
        Select the columns to get.
        None => *

        :param columns: fields of table
        :type columns: str
        :return:
        """

        if len(columns) == 0:
            columns = '*'

        self.query = f"""\
        Select {", ".join(columns)}
        From {self.table_name}"""

        return self

    def delete(self) -> 'QueryBuilder':
        """
        Delete data from table

        :return:
        """
        self.query = f"Delete from {self.table_name}"

        return self

    def insert(self, columns: List[str] | None = None, values: List[Tuple | Dict]) -> 'QueryBuilder':
        """
        Insert data

        :return:
        """

        cols = ""
        if columns is not None and isinstance(columns, list):
            columns = ", ".join(columns)

            cols = f"({columns})"

        values =

        self.query = f"""\
        Insert into {self.table_name}{cols} \
        Values 
        """

        return self

    def enable_binding(self) -> 'QueryBuilder':

        self.__binding = True

        return self

    def disable_binding(self) -> 'QueryBuilder':

        self.__binding = False

        return self

    def apply_conditions(self, *conditions: WhereCondition) -> 'QueryBuilder':
        """
        Apply the list of where conditions

        :param conditions:
        :type conditions: WhereCondition
        :return:
        """

        for condition in conditions:
            self.where(*condition.to_tuple())

        return self

    def where(self, col: str, operator: str, value: Any, of_table: str | None = None) -> 'QueryBuilder':
        """
        Add (and) where clause on query.

        :param col:
        :type col: str
        :param operator:
        :type operator: str
        :param value:
        :type value: Any
        :param of_table: table of 'field', default self.table_name
        :type of_table: str
        :return:
        """

        if not self.__has_where:
            self.__has_where = True

            self.query += "\nWhere "

        else:
            self.query += "\nAnd "

        table = of_table if of_table is not None else self.table_name

        if self.binding:
            self.data_bound.append(value)
            value = "?"

        else:  # if in binding, sqlite3 also implements append of ''
            if isinstance(value, str):
                value = f"'{value}'"

        self.query += f"{table}.{col} {operator} {value}"

        return self

    def to_sql(self, verbose: bool = False):
        """
        Return sql query

        :param verbose: if True also print sql
        :type verbose: bool

        :return: query
        :rtype str:
        """

        query = self.query.rstrip() + ";"

        if verbose:
            print(query)

        return query
