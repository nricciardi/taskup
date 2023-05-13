from lib.utils.logger import Logger
import json
from lib.file.file_manager import FileManger
import os
from typing import Any, List, Optional
from lib.utils.base import Base
from lib.utils.utils import Utils


class SettingsBase:
    WORK_DIRECTORY_NAME = ".taskup"
    SETTINGS_FILE_NAME = "settings.json"
    VAULT_FILE_NAME = "vault.json"
    DB_NAME = "database.db"

    KEY_VERBOSE = "verbose"
    VALUE_BASE_VERBOSE = True

    KEY_PROJECT_PATH = "current_project_path"
    VALUE_BASE_PROJECT_PATH = ""

    KEY_VAULT_PATH = "vault_path"
    VALUE_BASE_VAULT_PATH = os.getcwd()

    KEY_DB_LOCALTIME = "use_localtime"
    VALUE_BASE_DB_LOCALTIME = True

    KEY_DEBUG_MODE = "debug"
    VALUE_BASE_DEBUG_MODE = False

    KEY_FRONTEND_DIRECTORY = "frontend"
    VALUE_BASE_FRONTEND_DIRECTORY = os.path.join(Base.base_directory(), "frontend", "dist", "frontend")

    KEY_FRONTEND_START = "frontend_start"
    VALUE_BASE_FRONTEND_START = "index.html"

    KEY_APP_PORT = "port"
    VALUE_BASE_APP_PORT = 8000

    KEY_FRONTEND_DEBUG_PORT = "frontend_debug_port"
    VALUE_BASE_FRONTEND_DEBUG_PORT = 4200

    KEY_PROJECT_PATHS_STORED = "projects_paths_stored"
    VALUE_BASE_PROJECT_PATHS_STORED = []

    KEY_BACKUP = "backup"
    VALUE_BASE_BACKUP = True

    BASE_SETTINGS = {
        KEY_VERBOSE: VALUE_BASE_VERBOSE,
        KEY_PROJECT_PATH: VALUE_BASE_PROJECT_PATH,
        KEY_DB_LOCALTIME: VALUE_BASE_DB_LOCALTIME,
        KEY_DEBUG_MODE: VALUE_BASE_DEBUG_MODE,
        KEY_FRONTEND_DIRECTORY: VALUE_BASE_FRONTEND_DIRECTORY,
        KEY_FRONTEND_START: VALUE_BASE_FRONTEND_START,
        KEY_APP_PORT: VALUE_BASE_APP_PORT,
        KEY_VAULT_PATH: VALUE_BASE_VAULT_PATH,
        KEY_FRONTEND_DEBUG_PORT: VALUE_BASE_FRONTEND_DEBUG_PORT,
        KEY_PROJECT_PATHS_STORED: VALUE_BASE_PROJECT_PATHS_STORED,
        KEY_BACKUP: VALUE_BASE_BACKUP,
    }

    @staticmethod
    def settings_path() -> str:
        """
        Return the settings path of the app

        :rtype: str
        """

        return os.path.join(Base.base_directory(), SettingsBase.SETTINGS_FILE_NAME)


class SettingsManager(SettingsBase):
    CREATE_SETTINGS_FILE_IF_NOT_EXIST = True
    ICON_FILE_NAME = "icon.ico"

    def __init__(self):

        self.settings: dict = self.BASE_SETTINGS  # set base settings

        try:
            self.override_settings()

        except IOError as io_error:
            Logger.log_error(msg=f"configuration file {self.SETTINGS_FILE_NAME} not found", is_verbose=self.verbose)

            if SettingsManager.CREATE_SETTINGS_FILE_IF_NOT_EXIST:
                self.create_settings_file()
                self.override_settings()

        except json.JSONDecodeError as json_decode_error:
            Logger.log_error(msg=f"configuration file {self.SETTINGS_FILE_NAME} JSON syntax error", is_verbose=self.verbose)

            Utils.exit()

        finally:
            self.verify_mandatory_settings()

            # write settings in file
            self.dumps_settings()

    def verify_mandatory_settings(self) -> None:
        """
        Verify mandatory settings and throw exceptions
        """

        try:
            self.get_setting_by_key(self.KEY_PROJECT_PATH)

        except KeyError as key_error:
            Logger.log_error(msg=f"'{self.KEY_PROJECT_PATH}' is mandatory setting", is_verbose=self.verbose)

            Utils.exit()

    def override_settings(self) -> None:
        """
        Override app settings with settings configuration file
        """

        self.settings.update(FileManger.read_json(self.settings_path()))
        self.dumps_settings()

    def create_settings_file(self) -> None:
        """
        Create settings file if it does not exist with base settings
        """

        FileManger.write_json(self.settings_path(), self.BASE_SETTINGS)

    def set(self, key: str, value: Any) -> None:
        """
        Modify settings

        :param key: settings' key
        :param value: key's value

        :rtype: None
        """

        self.settings[key] = value
        self.dumps_settings()

    def dumps_settings(self) -> None:
        """
        Dumps settings in file

        :return:
        """

        FileManger.write_json(self.settings_path(), self.settings)

    def get_setting_by_key(self, key: str) -> Any:
        """
        Return the value of key passed

        :param key: A key of settings
        :type key: str

        :rtype: str
        """

        return self.settings[key]

    @property
    def verbose(self) -> bool:
        """
        Return verbose mode

        :return: verbose
        :rtype bool:
        """

        return self.get_setting_by_key(SettingsBase.KEY_VERBOSE)

    @property
    def project_directory_path(self) -> str:
        """
        Return the project directory

        :rtype: str
        """

        path = os.path.abspath(self.get_setting_by_key(self.KEY_PROJECT_PATH))

        self.add_path_to_stored(path)

        return path

    @property
    def projects_paths_stored(self) -> List[str]:
        """
        Return list of projects paths stored, erasing invalid paths

        :return:
        """

        self.clear_paths_stored()

        return self.get_setting_by_key(self.KEY_PROJECT_PATHS_STORED)

    @property
    def work_directory_path(self) -> str:
        """
        Return the work directory path inside the app

        :return:
        """

        return SettingsManager.assemble_work_directory_path(self.project_directory_path)

    @staticmethod
    def assemble_work_directory_path(project_path: str) -> str:
        """
        Assemble and return work directory path from passed path

        :param project_path:
        :return:
        """

        return os.path.join(project_path, SettingsBase.WORK_DIRECTORY_NAME)

    @property
    def db_name(self) -> str:
        """
        Return the database name

        :rtype: str
        """

        return SettingsBase.DB_NAME

    @property
    def db_path(self) -> str:
        """
        Return the database path of the app

        :rtype: str
        """

        return SettingsManager.assemble_db_path(work_dir_path=self.work_directory_path)

    @staticmethod
    def assemble_db_path(work_dir_path: Optional[str] = None, project_path: Optional[str] = None) -> str:
        """
        Assemble database path

        :param project_path:
        :param work_dir_path:
        :return:
        """

        if isinstance(work_dir_path, str):
            return os.path.join(work_dir_path, SettingsBase.DB_NAME)

        if isinstance(project_path, str):
            work_dir_path = SettingsManager.assemble_work_directory_path(project_path)

            return os.path.join(work_dir_path, SettingsBase.DB_NAME)

        raise ValueError()

    @property
    def vault_path(self) -> str:
        """
        Return the vault path of the app.
        Vault is the file where are stored login information

        :rtype: str
        """

        vault_path_generator = lambda: os.path.join(self.get_setting_by_key(self.KEY_VAULT_PATH), SettingsBase.VAULT_FILE_NAME)

        if not os.path.isfile(vault_path_generator()):
            self.set(self.KEY_VAULT_PATH, self.VALUE_BASE_VAULT_PATH)

        return vault_path_generator()

    @property
    def debug_mode(self) -> bool:
        """
        Return True if app is in debug mode

        :return: Mode
        :rtype bool:
        """

        return bool(self.get_setting_by_key(SettingsBase.KEY_DEBUG_MODE))

    @property
    def icon_path(self) -> str:
        """
        Return the icon's path

        :return:
        """

        return os.path.join(Base.base_directory(), self.ICON_FILE_NAME)

    @property
    def frontend_directory(self) -> str:
        """
        Return frontend directory of app

        :return: directory
        :rtype str:
        """

        return self.get_setting_by_key(SettingsBase.KEY_FRONTEND_DIRECTORY)

    @property
    def frontend_start(self) -> str:
        """
        Return the start file of frontend.
        If app is in debug mode return { 'port': 4200 } to use Angular in dev mode

        :rtype str:
        """

        if self.debug_mode:

            return { 'port': int(self.get_setting_by_key(SettingsBase.KEY_FRONTEND_DEBUG_PORT))}

        return self.get_setting_by_key(SettingsBase.KEY_FRONTEND_START)

    @property
    def port(self) -> int:
        """
        Return the port to use (in Eel)

        :rtype int:
        """

        return self.get_setting_by_key(SettingsBase.KEY_APP_PORT)

    def add_path_to_stored(self, path: str) -> None:
        """
        Add the passed path to projects paths stored

        :param path: path
        :type path: str
        :return:
        """

        if path not in self.projects_paths_stored:
            paths_stored = self.get_setting_by_key(self.KEY_PROJECT_PATHS_STORED)

            paths_stored.append(path)
            self.dumps_settings()

    def set_project_path(self, path) -> bool:
        """
        Set project path

        :param path:
        :return:
        """

        if not Utils.exist_dir(path):
            Logger.log_warning(msg=f"project: '{path}' not found", is_verbose=self.verbose)
            return False

        self.set(self.KEY_PROJECT_PATH, path)  # set path in settings.
        self.add_path_to_stored(path)

        return True

    def clear_paths_stored(self) -> None:
        """
        Remove invalid paths from paths stored

        :return:
        """

        paths_stored: List[str] = self.get_setting_by_key(self.KEY_PROJECT_PATHS_STORED)

        paths_checked = set()
        for path in paths_stored:
            if Utils.exist_dir(path):
                paths_checked.add(path)

        paths_checked = sorted(list(paths_checked))

        self.set(self.KEY_PROJECT_PATHS_STORED, paths_checked)
