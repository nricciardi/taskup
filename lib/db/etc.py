from abc import ABC


class ToSqlMixin(ABC):

    def to_sql(self) -> str:
        """
        Return string sql query

        :return: query
        :rtype str:
        """

        raise NotImplementedError
