from abc import ABC, abstractmethod


class ToSqlInterface(ABC):

    @abstractmethod
    def to_sql(self) -> str:
        """
        Return string sql query

        :return: query
        :rtype str:
        """

        raise NotImplementedError
