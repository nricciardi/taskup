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

    @staticmethod
    def log_error(msg: Any, full: bool = False, is_verbose: bool = True, prefix: bool = True) -> None:
        """
        Log pre-formatted error

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
    def log_success(msg: Any, is_verbose: bool = True, prefix: bool = True) -> None:
        """
        Log pre-formatted success

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

        print(f"{Fore.GREEN}{'SUCCESS: ' + Fore.RESET if prefix else ''}{str(msg)}")

    @staticmethod
    def log_info(msg: Any, is_verbose: bool = True, end: str = "\n", prefix: bool = True) -> None:
        """
        Log pre-formatted info

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

        print(f"{Fore.CYAN}{'INFO: ' + Fore.RESET if prefix else ''}{str(msg)}", end=end)

    @staticmethod
    def log_warning(msg: Any, is_verbose: bool = True, prefix: bool = True) -> None:
        """
        Log pre-formatted warning

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

        print(f"{Fore.YELLOW}{'WARNING: ' + Fore.RESET if prefix else ''}{str(msg)}")

    @staticmethod
    def log(msg: Any, is_verbose: bool = True) -> None:
        """
        Log pre-formatted text

        :param msg: message to print
        :type msg: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool

        :return: None
        """
        if not is_verbose:
            return

        print(f"{str(msg)}")

    @staticmethod
    def log_custom(msg: Any, is_verbose: bool = True, prefix: str = None, color: colorama = Fore.MAGENTA) -> None:
        """
        Pre-formatted custom log

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
