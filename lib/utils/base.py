import os
import pathlib
import sys
import colorama
from colorama import Fore, Back, Style

# Initialising Colorama (Important)
colorama.init(autoreset=True)

class Base:


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
    def log_error(error):
        print(f"{Fore.RED}ERROR: {error}")

    @staticmethod
    def log_success(success: str):
        print(f"{Fore.GREEN}ERROR: {success}")

    @staticmethod
    def log_info(info: str):
        print(f"{Fore.CYAN}ERROR: {info}")

