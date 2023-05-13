import sys
import colorama
from colorama import Fore, Back, Style
import traceback
from typing import Any, TypeVar

# Initialising Colorama (Important)
colorama.init(autoreset=True)


class Logger:
    """
    Logger

    """

    capitalize: bool = True

    @staticmethod
    def log_error(msg: Any, full: bool = False, is_verbose: bool = True, prefix: bool = True, msg_row: bool = False) -> None:
        """
        Log pre-formatted error

        :param msg_row: prevent manipulation on msg
        :type msg_row: bool
        :param msg: message to print
        :type msg: Any
        :param full: include trace bock
        :type full: bool
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool
        :param prefix: if be must be the prefix
        :type prefix: bool

        :return: None
        """

        if not is_verbose:
            return

        if msg_row is False and Logger.capitalize:
            msg = str(msg).capitalize()

        msg = f"{Fore.RED}{'ERROR: ' if prefix else ''}{str(msg)}"
        print(msg)

        try:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            line_num = exc_traceback.tb_lineno
            file_name = traceback.extract_tb(exc_traceback)[-1][0]

            print(f"{Fore.RED}-> line {line_num} in {file_name}")

            if full:
                tb_str = traceback.format_exc()
                print(f"{Fore.RED}\nFull traceback: {tb_str}")

        except Exception as exception:
            pass

    @staticmethod
    def log_success(msg: Any, is_verbose: bool = True, prefix: bool = True, msg_row: bool = False) -> None:
        """
        Log pre-formatted success

        :param msg_row: prevent manipulation on msg
        :type msg_row: bool
        :param msg: message to print
        :type msg: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool
        :param prefix: if must be the prefix
        :type prefix: bool

        :return: None
        """

        if not is_verbose:
            return

        if msg_row is False and Logger.capitalize:
            msg = str(msg).capitalize()

        print(f"{Fore.GREEN}{'SUCCESS: ' + Fore.RESET if prefix else ''}{str(msg)}")

    @staticmethod
    def log_info(msg: Any, is_verbose: bool = True, end: str = "\n", prefix: bool = True, msg_row: bool = False) -> None:
        """
        Log pre-formatted info

        :param msg_row: prevent manipulation on msg
        :type msg_row: bool
        :param msg: info to print
        :type msg: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool
        :param end: print() end
        :type end: str
        :param prefix: if must be the prefix
        :type prefix: bool

        :return: None
        """
        if not is_verbose:
            return

        if msg_row is False and Logger.capitalize:
            msg = str(msg).capitalize()

        print(f"{Fore.CYAN}{'INFO: ' + Fore.RESET if prefix else ''}{str(msg)}", end=end)

    @staticmethod
    def log_warning(msg: Any, is_verbose: bool = True, prefix: bool = True, msg_row: bool = False) -> None:
        """
        Log pre-formatted warning

        :param msg_row: prevent manipulation on msg
        :type msg_row: bool
        :param msg: info to print
        :type msg: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool
        :param prefix: if must be the prefix
        :type prefix: bool

        :return: None
        """
        if not is_verbose:
            return

        if msg_row is False and Logger.capitalize:
            msg = str(msg).capitalize()

        print(f"{Fore.YELLOW}{'WARNING: ' + Fore.RESET if prefix else ''}{str(msg)}")

    @staticmethod
    def log(msg: Any, is_verbose: bool = True, msg_row: bool = False, truncate: int | None = None) -> None:
        """
        Log pre-formatted text

        :param truncate: max length of message
        :type truncate: int
        :param msg_row: prevent manipulation on msg
        :type msg_row: bool
        :param msg: message to print
        :type msg: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool

        :return: None
        """
        if not is_verbose:
            return

        if msg_row is False and Logger.capitalize:
            msg = str(msg).capitalize()

        msg: str = str(msg)

        if isinstance(truncate, int):
            append_warning: bool = False
            if len(msg) > truncate:
                append_warning = True

            msg = msg[0:truncate]

            if append_warning:
                msg += "... [message truncates]"

        print(f"{msg}")

    @staticmethod
    def log_custom(msg: Any, is_verbose: bool = True, prefix: str = None, color: colorama = Fore.MAGENTA, capitalize: bool = True) -> None:
        """
        Pre-formatted custom log

        :param capitalize: if true capitalize msg
        :type capitalize: bool
        :param msg: message to print
        :type msg: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool
        :param prefix: if there has to be the prefix
        :type prefix: bool
        :param color: color

        :return: None
        """

        if not is_verbose:
            return

        if capitalize:
            msg = str(msg).capitalize()

        print(f"{color}{prefix + ': ' + Fore.RESET if not prefix is None else ''}{str(msg)}")

    @staticmethod
    def log_eel(msg: Any, is_verbose: bool = True) -> None:
        """
        Log pre-formatted eel

        :param msg: info to print
        :type msg: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool

        :return: None
        """

        Logger.log_custom(msg=msg, is_verbose=is_verbose, prefix="EXPOSED", color=Fore.MAGENTA)
