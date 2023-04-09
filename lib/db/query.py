from abc import ABC, abstractmethod
from typing import Any, List


class QueryBuilder(ABC):
    table_name: str
    query: str

    def __init__(self, table_name: str):
        self.table_name = table_name

    def to_sql(self):
        """
        Return sql query

        :return: query
        :rtype str:
        """

        return self.query.rstrip() + ";"


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

    def where(self, field: str, operator: str, value: Any, of_table: str | None = None) -> 'SelectQueryBuilder':
        """
        Add (and) where clause on query.

        :param field:
        :type field: str
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

            self.query += "Where "

        else:
            self.query += "And "

        table = of_table if of_table is not None else self.table_name

        if isinstance(value, str):
            value = f"'{value}'"

        self.query += f"{table}.{field} {operator} {value}"

        return self

    def select(self, columns: List[str] | None = None) -> 'SelectQueryBuilder':
        """
        Select the columns to get.
        None => *

        :param columns: fields of table
        :type columns: List[str] | None
        :return:
        """

        if columns is None:
            columns = ['*']

        self.query = f"""
        Select {", ".join(columns)}
        From {self.table_name}
        """

        return self
