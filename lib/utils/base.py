import os
import pathlib
import sys


class Base:

    def __init__(self):
        pass

    @staticmethod
    def exit():
        print("Exit...")
        sys.exit()

    @staticmethod
    def settings_file_name() -> str:
        """
        Return the settings file name

        :rtype: str
        """

        return "settings.json"

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
    def settings_path() -> str:
        """
        Return the settings path of the project

        :rtype: str
        """

        return os.path.join(Base.base_directory(), Base.settings_file_name())

    @staticmethod
    def setting_db_name():
        """
        Return the db name property name

        :rtype: str
        """

        return "db_name"

    @staticmethod
    def base_db_name() -> str:
        """
        Return the base db name

        :rtype: str
        """

        return "database.db"

    @staticmethod
    def setting_project_path() -> str:
        """
        Return project path (to manage) property name

        :rtype: str
        """

        return "path"

    @staticmethod
    def base_settings() -> dict:
        """
        Return base settings

        :rtype: dict
        """

        return {
            Base.setting_db_name(): Base.base_db_name()
        }
