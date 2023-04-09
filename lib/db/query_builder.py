from abc import ABC, abstractmethod
from typing import Any, List


class QueryBuilder(ABC):
    table_name: str
    query: str

    def __init__(self, table_name: str):
        self.table_name = table_name

    @abstractmethod
    def to_sql(self):
        raise NotImplementedError


class SelectQueryBuilder(QueryBuilder):

    __columns = ['*']

    def __init__(self, table_name: str, alias: str | None = None):

        if alias is not None:
            table_name = f"{table_name} as {alias}"

        super().__init__(table_name)

    @property
    def columns(self) -> List[str]:
        return self.__columns

    @columns.setter
    def columns(self, cols: List[str]) -> None:
        self.__columns = cols

    def where(self, field: str, operator: str, value: Any):
        raise NotImplementedError

    def to_sql(self):
        return f"""
        Select {", ".join(self.columns)}
        From {self.table_name}
        """
