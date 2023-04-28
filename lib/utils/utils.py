import sys
import os


class Utils:

    @staticmethod
    def exit():
        print("Forced Exit...")
        sys.exit()

    @staticmethod
    def exist_dir(dir_path: str) -> bool:
        """
        Check if dir passed exists or not

        :param dir_path: directory's path
        :type dir_path: str
        :return:
        :rtype: bool
        """

        # check if exist
        return os.path.isdir(dir_path)


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

        return f"""strftime('{formatter}', {"'" if strict_string else ""}{datetime}{", 'localtime'" if use_localtime else ""}{"'" if strict_string else ""})"""

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

    @staticmethod
    def datetime_strf_now(use_localtime: bool = False) -> str:
        """
        String format to now (datetime)

        :param use_localtime:
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.datetime_str_format('now', strict_string=True, use_localtime=use_localtime)

    @staticmethod
    def date_strf_now(use_localtime: bool = False) -> str:
        """
        String format to now (date)

        :param use_localtime:
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.date_str_format('now', strict_string=True, use_localtime=use_localtime)

    @staticmethod
    def time_strf_now(use_localtime: bool = False) -> str:
        """
        String format to now (date)

        :param use_localtime:
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.time_str_format('now', strict_string=True, use_localtime=use_localtime)
