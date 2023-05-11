import sys
import os
from random import randint
from typing import Dict
import hashlib
import webbrowser
from lib.utils.logger import Logger


class Utils:

    @staticmethod
    def exit():
        """
        Force exit

        :return:
        """
        Logger.log_warning(msg="force exit...")

        sys.exit()

    @staticmethod
    def open_in_webbrowser(path: str) -> None:
        """
        Open path in web browser with webbrowser

        :param path:
        :return:
        """

        webbrowser.open(path)

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

    @staticmethod
    def random_hex() -> str:
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        # "#RRGGBB"
        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

        return hex_color

    @staticmethod
    def disguise(value: str) -> str:
        """
        Disguise value (sha)

        :return:
        """

        return hashlib.sha512(value.encode()).hexdigest()

    @staticmethod
    def disguise_value_of_dict(d: Dict, *keys: str) -> None:
        """
        Disguise all dictionary value of keys

        :param d: dictionary
        :param keys:
        :return:
        """

        for key in keys:

            value = d.get(key)

            if value is not None:
                d[key] = Utils.disguise(value)


class SqlUtils:

    UPDATED_AT_FIELD_NAME: str = "updated_at"

    DATETIME_FORMATTER: str = '%Y-%m-%d %H:%M:%S'
    DATE_FORMATTER: str = '%Y-%m-%d'
    TIME_FORMATTER: str = '%H:%M:%S'

    @staticmethod
    def custom_datetime_str_format(formatter: str, datetime: str, strict_string: bool = False, use_localtime: bool = True) -> str:
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

        if strict_string:
            datetime: str = f"'{datetime}'"

        localtime: str = ""

        if use_localtime:
            localtime = f", 'localtime'"

        return f"""strftime('{formatter}', {datetime}{localtime})"""

    @staticmethod
    def datetime_str_format(value: str, strict_string: bool = False, use_localtime: bool = True) -> str:
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
    def date_str_format(value: str, strict_string: bool = False, use_localtime: bool = True) -> str:
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
    def time_str_format(value: str, strict_string: bool = False, use_localtime: bool = True) -> str:
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
    def datetime_strf_now(use_localtime: bool = True) -> str:
        """
        String format to now (datetime)

        :param use_localtime:
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.datetime_str_format('now', strict_string=True, use_localtime=use_localtime)

    @staticmethod
    def date_strf_now(use_localtime: bool = True) -> str:
        """
        String format to now (date)

        :param use_localtime:
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.date_str_format('now', strict_string=True, use_localtime=use_localtime)

    @staticmethod
    def time_strf_now(use_localtime: bool = True) -> str:
        """
        String format to now (date)

        :param use_localtime:
        :type use_localtime: bool
        :return:
        """

        return SqlUtils.time_str_format('now', strict_string=True, use_localtime=use_localtime)
