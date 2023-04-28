import os
from lib.settings.settings import SettingsManager
from lib.db.db import DBManager
from lib.utils.utils import Utils
from lib.utils.logger import Logger
from typing import Tuple


class ProjectManager:
    def __init__(self):
        self.__settings_manager: SettingsManager = SettingsManager()
        self.verbose = self.__settings_manager.verbose()

        db_name, use_localtime, project_path, work_directory_path = self.get_settings()

        if not Utils.exist_dir(project_path):
            Logger.log_error(msg=f"selected project path '{project_path}' NOT found", is_verbose=self.verbose)

            Utils.exit()

        # create work directory inside app if it does NOT exist
        if not Utils.exist_dir(work_directory_path):
            self.create_work_directory()

        # generate db base structure if db doesn't exist
        self.__db_manager = DBManager(db_name=db_name,
                                      work_directory_path=work_directory_path,
                                      verbose=self.verbose,
                                      use_localtime=use_localtime)

    def get_settings(self) -> Tuple:
        """
        Load from settings securely and return them

        :return: tuple of settings
        :rtype tuple:
        """

        try:
            # get app settings
            db_name = self.__settings_manager.get(self.__settings_manager.KEY_DB_NAME)
            use_localtime = self.__settings_manager.get(self.__settings_manager.KEY_DB_LOCALTIME)
            project_path = self.__settings_manager.project_directory_path()
            work_directory_path = self.__settings_manager.work_directory_path()

            return db_name, use_localtime, project_path, work_directory_path

        except Exception as exception:
            Logger.log_error(msg="error while retrieving app settings", is_verbose=self.verbose)

            Utils.exit()

    def create_work_directory(self) -> None:
        """
        Create work directory in the app

        :rtype None:
        """

        work_directory_path: str = self.__settings_manager.work_directory_path()

        try:
            os.mkdir(work_directory_path)

        except Exception as e:
            Logger.log_error(msg=f"error during creation of work directory in project ({work_directory_path})")
            Utils.exit()

    @property
    def project_path(self):
        return self.__settings_manager.project_directory_path()
