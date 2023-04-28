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


class SqlUtils:

    DATETIME_FORMATTER: str = '%Y-%m-%d %H:%M:%S'
    DATE_FORMATTER: str = '%Y-%m-%d'
    TIME_FORMATTER: str = '%H:%M:%S'

    @staticmethod
    def custom_datetime_str_format(formatter: str, datetime: str, strict_string: bool = False, use_localtime: bool = False) -> str:
        """
        Return sqlite string formatted based on formatter passed

        :param formatter: string formatter
        :type formatter: str
        :param use_localtime: db localtime flag
        :type use_localtime: bool
        :param datetime: datetime
        :type datetime: str
        :param strict_string: strict string flag
        :type strict_string: bool
        :return:
        """

        return f"""strftime({formatter}, {"'" if strict_string else ""}{datetime}{", 'localtime'" if use_localtime else ""}{"'" if strict_string else ""})"""

    @staticmethod
    def datetime_str_format(value: str, strict_string: bool = False, use_localtime: bool = False) -> str:
        """
        Return sqlite string format for datetime passed

        :param value: datetime
        :type value: str
        :param strict_string: strict string flag
        :type strict_string: str
        :param use_localtime: db localtime flag
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.custom_datetime_str_format(SqlUtils.DATETIME_FORMATTER, value, strict_string, use_localtime)

    @staticmethod
    def date_str_format(value: str, strict_string: bool = False, use_localtime: bool = False) -> str:
        """
        Return sqlite string format for datetime passed

        :param value: datetime
        :type value: str
        :param strict_string: strict string flag
        :type strict_string: str
        :param use_localtime: db localtime flag
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.custom_datetime_str_format(SqlUtils.DATE_FORMATTER, value, strict_string, use_localtime)

    @staticmethod
    def time_str_format(value: str, strict_string: bool = False, use_localtime: bool = False) -> str:
        """
        Return sqlite string format for datetime passed

        :param value: datetime
        :type value: str
        :param strict_string: strict string flag
        :type strict_string: str
        :param use_localtime: db localtime flag
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.custom_datetime_str_format(SqlUtils.TIME_FORMATTER, value, strict_string, use_localtime)
