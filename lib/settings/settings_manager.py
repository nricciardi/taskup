from lib.utils.base import Base
import json
from lib.file.file_manager import FileManger
from lib.settings.settings_base import SettingsBase
import os
from typing import Any


class SettingsManager(SettingsBase):
    create_settings_file_if_not_exist = True

    def __init__(self):

        self.settings: dict = self.BASE_SETTINGS  # set base settings

        try:
            self.override_settings()

        except IOError as io_error:
            print(f"Configuration file {self.SETTINGS_FILE_NAME} not found")

            if SettingsManager.create_settings_file_if_not_exist:
                self.create_settings_file()
                self.override_settings()

        except json.JSONDecodeError as json_decode_error:
            print(f"Configuration file {self.SETTINGS_FILE_NAME} JSON syntax error")
            Base.exit()

        finally:
            self.verify_mandatory_settings()

    def verify_mandatory_settings(self) -> None:
        """
        Verify mandatory settings and throw exceptions
        """

        try:
            self.get(self.PROJECT_PATH_KEY)

        except KeyError as key_error:
            print(f"'{self.PROJECT_PATH_KEY}' is mandatory setting")
            Base.exit()

    def override_settings(self) -> None:
        """
        Override project settings with settings configuration file
        """

        self.settings.update(FileManger.read_json(self.settings_path()))

    def create_settings_file(self) -> None:
        """
        Create settings file if it does not exist with base settings
        """

        FileManger.write_json(self.settings_path(), self.settings_path())

    def set(self, key: str, value: str) -> None:
        """
        Modify settings

        :param key: settings' key
        :param value: key's value

        :rtype: None
        """
        self.settings[key] = value

    def get(self, key: str) -> Any:
        """
        Return the value of key passed

        :param key: A key of settings
        :type key: str

        :rtype: str
        """

        return self.settings[key]

    def project_directory_path(self) -> str:
        """
        Return the project directory

        :rtype: str
        """

        return os.path.abspath(self.get(self.PROJECT_PATH_KEY))

    def work_directory_path(self) -> str:
        """
        Return the work directory path inside the project

        :return:
        """

        return os.path.join(self.project_directory_path(), self.WORK_DIRECTORY_NAME)

    def db_path(self) -> str:
        """
        Return the database path of the project

        :rtype: str
        """

        return os.path.join(self.work_directory_path(), self.get(self.DB_NAME_KEY))
