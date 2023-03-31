from lib.utils.base import Base
import json
from lib.file.file_manager import FileManger
import os
from typing import Any


class SettingsBase:
    WORK_DIRECTORY_NAME = "work"
    SETTINGS_FILE_NAME = "settings.json"

    KEY_DB_NAME = "db_name"
    VALUE_BASE_DB_NAME = "database.db"

    KEY_VERBOSE = "verbose"
    VALUE_BASE_VERBOSE = True

    KEY_PROJECT_PATH = "project_path"
    VALUE_BASE_PROJECT_PATH = os.path.join(os.path.curdir, "..")

    KEY_DB_LOCALTIME = "localtime"
    VALUE_BASE_DB_LOCALTIME = False

    KEY_DEBUG_MODE = "debug"
    VALUE_BASE_DEBUG_MODE = True

    KEY_FRONTEND_DIRECTORY = "frontend"
    VALUE_BASE_FRONTEND_DIRECTORY = os.path.join(os.path.curdir, "../frontend/dist/frontend")

    KEY_FRONTEND_START = "start"
    VALUE_BASE_FRONTEND_START = "index.html"

    KEY_APP_PORT = "port"
    VALUE_BASE_APP_PORT = 8000

    BASE_SETTINGS = {
        KEY_DB_NAME: VALUE_BASE_DB_NAME,
        KEY_VERBOSE: VALUE_BASE_VERBOSE,
        KEY_PROJECT_PATH: VALUE_BASE_PROJECT_PATH,
        KEY_DB_LOCALTIME: VALUE_BASE_DB_LOCALTIME,
        KEY_DEBUG_MODE: VALUE_BASE_DEBUG_MODE,
        KEY_FRONTEND_DIRECTORY: VALUE_BASE_FRONTEND_DIRECTORY,
        KEY_FRONTEND_START: VALUE_BASE_FRONTEND_START,
        KEY_APP_PORT: VALUE_BASE_APP_PORT
    }

    @staticmethod
    def settings_path() -> str:
        """
        Return the settings path of the app

        :rtype: str
        """

        return os.path.join(Base.base_directory(), SettingsBase.SETTINGS_FILE_NAME)


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
            self.get(self.KEY_PROJECT_PATH)

        except KeyError as key_error:
            print(f"'{self.KEY_PROJECT_PATH}' is mandatory setting")
            Base.exit()

    def override_settings(self) -> None:
        """
        Override app settings with settings configuration file
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

    def verbose(self) -> bool:
        """
        Return verbose mode

        :return: verbose
        :rtype bool:
        """

        return self.get(SettingsBase.KEY_VERBOSE)

    def project_directory_path(self) -> str:
        """
        Return the app directory

        :rtype: str
        """

        return os.path.abspath(self.get(self.KEY_PROJECT_PATH))

    def work_directory_path(self) -> str:
        """
        Return the work directory path inside the app

        :return:
        """

        return os.path.join(self.project_directory_path(), self.WORK_DIRECTORY_NAME)

    def db_name(self) -> str:
        """
        Return the database name

        :rtype: str
        """

        return self.get(self.KEY_DB_NAME)

    def db_path(self) -> str:
        """
        Return the database path of the app

        :rtype: str
        """

        return os.path.join(self.work_directory_path(), self.get(self.KEY_DB_NAME))

    def debug_mode(self) -> bool:
        """
        Return True if app is in debug mode

        :return: Mode
        :rtype bool:
        """

        return self.get(SettingsBase.KEY_DEBUG_MODE)

    def frontend_directory(self) -> str:
        """
        Return frontend directory of app

        :return: directory
        :rtype str:
        """

        return self.get(SettingsBase.KEY_FRONTEND_DIRECTORY)

    def frontend_start(self) -> str:
        """
        Return the start file of frontend.
        If app is in debug mode return { 'port': 4200 } to use Angular in dev mode

        :rtype str:
        """

        if self.debug_mode():
            return { 'port': 4200 }

        return self.get(SettingsBase.KEY_FRONTEND_START)

    def port(self) -> int:
        """
        Return the port to use (in Eel)

        :rtype int:
        """

        return self.get(SettingsBase.KEY_APP_PORT)

