from abc import ABC
from typing import Any, List
from lib.db.component import WhereCondition
from lib.utils.mixin.sql import ToSqlInterface


class QueryBuilder(ToSqlInterface, ABC):
    table_name: str
    query: str
    binding: bool
    data_bound: List[Any]

    def __init__(self, table_name: str, binding_mode: bool = False):
        self.table_name = table_name
        self.binding = binding_mode
        self.data_bound = []

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


class SelectQueryBuilder(QueryBuilder):

    __has_where: bool = False

    def __init__(self, table_name: str, alias: str | None = None):
        if alias is not None:
            table_name = f"{table_name} as {alias}"

        super().__init__(table_name)

    @classmethod
    def from_table(cls, table_name: str, alias: str | None = None) -> 'SelectQueryBuilder':
        """
        More expressive constructor alias

        :param table_name:
        :type table_name: str
        :param alias: table alias
        :type alias: str
        :return:
        """

        return cls(table_name, alias)

    def enable_binding(self) -> 'SelectQueryBuilder':

        self.binding = True

        return self

    def disable_binding(self) -> 'SelectQueryBuilder':

        self.binding = False

        return self

    def apply_conditions(self, *conditions: WhereCondition) -> 'SelectQueryBuilder':
        """
        Apply the list of where conditions

        :param conditions:
        :type conditions: WhereCondition
        :return:
        """

        for condition in conditions:
            self.where(*condition.to_tuple())

        return self

    def where(self, col: str, operator: str, value: Any, of_table: str | None = None) -> 'SelectQueryBuilder':
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

        else:       # if in binding, sqlite3 also implements append of ''
            if isinstance(value, str):
                value = f"'{value}'"

        self.query += f"{table}.{col} {operator} {value}"

        return self

    def select(self, *columns: str) -> 'SelectQueryBuilder':
        """
        Select the columns to get.
        None => *

        :param columns: fields of table
        :type columns: str
        :return:
        """

        if len(columns) == 0:
            columns = '*'

        self.query = f"""
        Select {", ".join(columns)}
        From {self.table_name}"""

        return self
