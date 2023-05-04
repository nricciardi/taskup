import os
from lib.settings.settings import SettingsManager
from lib.db.db import DBManager
from lib.utils.utils import Utils
from lib.utils.logger import Logger
from typing import Tuple


class ProjectManager:
    def __init__(self):

        Logger.log_info(msg="project manager init...", is_verbose=True)

        # instance settings manager to take project configuration settings
        Logger.log_info(msg="Read settings...", is_verbose=True)
        self.__settings_manager = SettingsManager()

        # take and set settings
        self.verbose = self.settings.verbose  # set verbose

        self.check_project_path()

        # create work directory inside app if it does NOT exist
        self.create_work_directory()

        # load db manager
        self.__db_manager = None        # it's going to override by next method
        self.load_db_manager()

    @property
    def settings(self) -> SettingsManager:
        return self.__settings_manager

    @property
    def project_path(self):
        return self.settings.project_directory_path

    @property
    def db_manager(self) -> DBManager:
        return self.__db_manager

    def check_project_path(self) -> None:
        """
        Check project path to prevent future errors

        :return:
        """

        project_path = self.settings.project_directory_path

        if not Utils.exist_dir(project_path):
            Logger.log_error(msg=f"selected project path '{project_path}' NOT found", is_verbose=self.verbose)

            Utils.exit()

    def load_db_manager(self) -> None:
        """
        Load database manager for project

        :return:
        """

        try:
            # get app settings
            db_name = self.__settings_manager.db_name
            use_localtime = self.__settings_manager.get(self.__settings_manager.KEY_DB_LOCALTIME)
            work_directory_path = self.__settings_manager.work_directory_path

            if isinstance(self.__db_manager, DBManager):
                self.__db_manager.close_connection()        # close prev connection

            # this generates db base structure if db doesn't exist
            self.__db_manager = DBManager(db_name=db_name,
                                          work_directory_path=work_directory_path,
                                          verbose=self.verbose,
                                          use_localtime=use_localtime)

        except Exception as exception:
            Logger.log_error(msg="error while retrieving app settings", is_verbose=self.verbose)

    def create_work_directory(self) -> None:
        """
        Create work directory in the app if it doesn't exist

        :rtype None:
        """

        work_directory_path: str = self.__settings_manager.work_directory_path

        try:

            if not Utils.exist_dir(work_directory_path):
                Logger.log_info(msg="create work directory", is_verbose=self.verbose)

                os.mkdir(work_directory_path)

        except Exception as e:
            Logger.log_error(msg=f"error during creation of work directory in project ({work_directory_path})")
            Utils.exit()
