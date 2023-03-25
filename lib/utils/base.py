import os
import pathlib
import sys
import colorama
from colorama import Fore, Back, Style
import traceback


# Initialising Colorama (Important)
colorama.init(autoreset=True)

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
    def log_error(error, full: bool = False):

        error = f"{Fore.RED}ERROR: {error}"

        if full:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            line_num = exc_traceback.tb_lineno
            file_name = traceback.extract_tb(exc_traceback)[-1][0]

            error += f" -> line {line_num} in {file_name}"

        print(error)


    @staticmethod
    def log_success(success: str):
        print(f"{Fore.GREEN}SUCCESS: {success}")

    @staticmethod
    def log_info(info: str):
        print(f"{Fore.CYAN}INFO: {info}")

