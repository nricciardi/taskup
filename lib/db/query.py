from abc import ABC
from typing import Any, List, Generic, TypeVar, Dict, Tuple, Optional
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

    def query_raw(self, raw: str) -> 'QueryBuilder':
        """
        Append to query a raw content

        :param raw: raw content
        :type raw: str
        :return:
        """

        self.query += raw

        return self

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

    def update_from_dict(self, data: Dict) -> 'QueryBuilder':
        """
        Update query from dict

        :param data:
        :return:
        """

        self.query = f"Update {self.table_name}\nSet "

        if self.binding:
            keys = []
            values = []
            for key in data.keys():
                keys.append(key)
                values.append(data[key])

            self.query += ",\n".join(str(key) + " = ?" for key in keys)
            self.data_bound = values

        else:
            self.query += ",\n".join(str(key) + " = " + str(data[key]) for key in data.keys())

        return self

    def insert_from_dict(self, *values: Dict, columns: List[str] | None = None) -> 'QueryBuilder':
        """
        Insert data from dict

        :return:
        """

        q = []
        for value in values:

            # make cols
            if columns is not None and isinstance(columns, list):
                columns = ", ".join(columns)

                cols = f"({columns})"

            else:
                cols = ", ".join(value.keys())
                cols = f"({cols})"

            # make data
            if self.binding:
                data: str = ','.join(['?'] * len(value.values()))

                for v in value.values():
                    self.data_bound.append(v)

            else:
                data: str = ','.join(value.values())

            q.append(f"""\
            Insert into {self.table_name}{cols} \
            Values ({data})
            """)

        self.query = ";\n\n".join(q)

        return self

    def insert_from_tuple(self, *values: Tuple, columns: Optional[List[str] | Tuple[str]] = None) -> 'QueryBuilder':
        """
        Insert data from tuple

        :return:
        """

        if isinstance(columns, list) or isinstance(columns, tuple):
            columns: str = ", ".join(columns)
            columns = f"({columns})"
        else:
            columns: str = ""

        if self.binding:
            data: List[str] = []
            for value in values:
                data.append(", ".join(['?'] * len(value)))
                self.data_bound.append(value)
            data: str = ", ".join(data)

        else:
            data: List[str] = [str(value) for value in values]
            data: str = ", ".join(data)

        self.query = f"""\
        Insert into {self.table_name}{columns}
        Values {data}\
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
