import os
from lib.utils.base import Base


class SettingsBase:
    WORK_DIRECTORY_NAME = "work"
    SETTINGS_FILE_NAME = "settings.json"

    DB_NAME_KEY = "db_name"
    BASE_DB_NAME_VALUE = "database.db"

    VERBOSE_KEY = "verbose"
    BASE_VERBOSE_VALUE = True

    PROJECT_PATH_KEY = "project_path"

    BASE_SETTINGS = {
        DB_NAME_KEY: BASE_DB_NAME_VALUE,
        VERBOSE_KEY: BASE_VERBOSE_VALUE
    }

    @staticmethod
    def settings_path() -> str:
        """
        Return the settings path of the project

        :rtype: str
        """

        return os.path.join(Base.base_directory(), SettingsBase.SETTINGS_FILE_NAME)

