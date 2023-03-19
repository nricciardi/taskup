import os
from lib.utils.base import Base


class SettingsBase:

    SETTINGS_FILE_NAME = "settings.json"

    DB_NAME_KEY = "db_name"
    BASE_DB_NAME_VALUE = "database.db"

    PROJECT_PATH_KEY = "project_path"

    BASE_SETTINGS = {
        DB_NAME_KEY: BASE_DB_NAME_VALUE
    }

    @staticmethod
    def settings_path() -> str:
        """
        Return the settings path of the project

        :rtype: str
        """

        return os.path.join(Base.base_directory(), SettingsBase.SETTINGS_FILE_NAME)

