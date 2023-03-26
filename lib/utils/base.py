import os
import pathlib
import sys
import colorama
from colorama import Fore, Back, Style
import traceback
from typing import Any, TypeVar

# Initialising Colorama (Important)
colorama.init(autoreset=True)

# Types
BEM = TypeVar('BEM', bound='BaseEntityModel')


class Base:
    """
    Base class contains utilities

    """

    @staticmethod
    def exit():
        print("Exit...")
        sys.exit()

    @staticmethod
    def base_directory() -> str:
        """
        Return the base directory path

        :rtype: str
        """

        this_file_path = os.path.abspath(__file__)
        path = pathlib.Path(this_file_path)
        project_path = path.parent.parent.parent.absolute()

        return str(project_path)

    @staticmethod
    def log_error(message: Any, full: bool = False, is_verbose: bool = True) -> None:
        """
        Log pre-formatted error

        :param message: message to print
        :type message: Any
        :param full: include trace bock
        :type full: bool
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool

        :return: None
        """

        if not is_verbose:
            return

        exc_type, exc_value, exc_traceback = sys.exc_info()
        line_num = exc_traceback.tb_lineno
        file_name = traceback.extract_tb(exc_traceback)[-1][0]

        message = f"{Fore.RED}ERROR: {str(message)} -> line {line_num} in {file_name}"

        if full:
            tb_str = traceback.format_exc()
            message += f"\nFull traceback: {tb_str}"

        print(message)

    @staticmethod
    def log_success(message: Any, is_verbose: bool = True) -> None:
        """
        Log pre-formatted success

        :param message: message to print
        :type message: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool

        :return: None
        """

        if not is_verbose:
            return

        print(f"{Fore.GREEN}SUCCESS: {str(message)}")

    @staticmethod
    def log_info(message: Any, is_verbose: bool = True):
        """
        Log pre-formatted info

        :param message: info to print
        :type message: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool

        :return: None
        """
        if not is_verbose:
            return

        print(f"{Fore.CYAN}INFO: {str(message)}")

    @staticmethod
    def log_warning(message: Any, is_verbose: bool = True):
        """
        Log pre-formatted warning

        :param message: info to print
        :type message: Any
        :param is_verbose: it used to check if it is verbose
        :type is_verbose: bool

        :return: None
        """
        if not is_verbose:
            return

        print(f"{Fore.YELLOW}WARNING: {str(message)}")
