import os
import pathlib
import sys


class Base:

    WORK_DIRECTORY_NAME = ".work"

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

