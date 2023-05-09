import os
from lib.settings.settings import SettingsManager
from lib.db.db import DBManager
from lib.utils.utils import Utils
from lib.utils.logger import Logger
from typing import List, Dict, Optional
import os


class ProjectManager:
    def __init__(self, load_db: bool = True):
        """
        Init project manager

        :param load_db: flag which indicates if PM have to load a new db or not (it is used to prevent lost reference of DBManager in entities if project is reloaded, so DBManager can be reloaded)
        """

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
        if load_db:
            self.__db_manager: Optional[DBManager] = None        # it's going to override by next method
            self.load_new_db_manager()

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

    def load_new_db_manager(self) -> None:
        """
        Load database manager for project

        :return:
        """

        try:
            # get app settings
            db_name = self.__settings_manager.db_name
            use_localtime = self.__settings_manager.get_setting_by_key(self.__settings_manager.KEY_DB_LOCALTIME)
            work_directory_path = self.__settings_manager.work_directory_path

            if isinstance(self.__db_manager, DBManager):
                self.__db_manager.close_connection()        # close prev connection

            # this generates db base structure if db doesn't exist
            self.__db_manager: DBManager = DBManager(db_name=db_name,
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

    def get_projects_paths_stored(self) -> List[str]:
        """
        Get all projects paths stored

        :return: projects paths
        """

        paths_stored: List[str] = self.__settings_manager.projects_paths_stored

        return paths_stored

    def project_information(self) -> Dict:
        """
        Return key-value project information

        :return:
        """

        return {
            "path": self.__settings_manager.project_directory_path,
            "database_path": self.__db_manager.db_path
        }

    def refresh(self) -> None:
        self.__init__(load_db=False)

        self.__db_manager.refresh_connection(db_name=self.settings.db_name,
                                             work_directory_path=self.settings.work_directory_path,
                                             verbose=self.verbose,
                                             use_localtime=self.__settings_manager.get_setting_by_key(self.__settings_manager.KEY_DB_LOCALTIME))