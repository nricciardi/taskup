import os
from lib.settings.settings import SettingsManager
from lib.db.db import DBManager
from lib.utils.utils import Utils
from lib.utils.logger import Logger
from typing import List, Dict, Optional
import os
from lib.db.entity.user import UserModel


class ProjectManager:
    def __init__(self, settings_manager: SettingsManager):
        """
        Init project manager, a ProjectManager manages the initialized projects that can be opened

        :param load_new_db: flag which indicates if PM have to load a new db or not (it is used to prevent lost reference of DBManager in entities if project is reloaded, so DBManager can be reloaded)
        """

        Logger.log_info(msg="project manager init...", is_verbose=True)

        # AppManager conceded settings manager to ProjectManager, so it can be used to each entity
        self.settings = settings_manager

        # take and set settings
        self.verbose = self.settings.verbose  # set verbose

        check_result = self.check_project_path()

        # load db manager
        if check_result:
            self.__db_manager: Optional[DBManager] = None        # it's going to override by next method
            self.load_new_db_manager()

    @property
    def settings(self) -> SettingsManager:
        return self.__settings_manager

    @settings.setter
    def settings(self, settings_manager) -> None:
        self.__settings_manager = settings_manager

    @property
    def project_path(self) -> str:
        return self.settings.project_directory_path

    @property
    def db_manager(self) -> DBManager:
        return self.__db_manager

    def check_project_path(self, path: Optional[str] = None, force_exit: bool = True) -> bool:
        """
        Check project path to prevent future errors

        :return:
        """

        project_path = self.settings.project_directory_path

        if isinstance(path, str):
            project_path = path

        if not Utils.exist_dir(project_path) or not self.already_init(project_path):
            Logger.log_error(msg=f"selected project path '{project_path}' NOT found", is_verbose=self.verbose)

            if force_exit:
                Utils.exit()

            return False

        return True

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

    def already_init(self, path: str) -> bool:
        """
        Return True if in path there is the work directory

        :param path:
        :return:
        """

        work_directory_name: str = self.settings.WORK_DIRECTORY_NAME

        return work_directory_name in os.listdir(path) and os.path.isdir(os.path.join(path, work_directory_name))

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
        """
        Refresh project managed refreshing database manager

        :return:
        """

        self.check_project_path()

        # refresh db manager connection with (new) settings
        self.__db_manager.refresh_connection(db_name=self.settings.db_name,
                                             work_directory_path=self.settings.work_directory_path,
                                             verbose=self.verbose,
                                             use_localtime=self.__settings_manager.get_setting_by_key(self.__settings_manager.KEY_DB_LOCALTIME))

    def remove(self, path: str) -> bool:
        """
        Remove project

        :param path:
        :return:
        """

        try:

            if not self.already_init(path):
                Logger.log_error(msg=f"project not found in path: '{path}'", is_verbose=self.verbose)
                return False

            work_directory_path = os.path.join(path, self.settings.WORK_DIRECTORY_NAME)

            import shutil

            shutil.rmtree(work_directory_path)

        except Exception as e:
            Logger.log_error(msg=f"{e}", is_verbose=self.verbose)

            return False

    def init_new(self, path: str, pm: UserModel, force_init: bool = False) -> bool:
        """
        Initialized a new project in path with pm as project manager

        :param force_init: flag which indicates if overwrite previously init
        :param path:
        :param pm:
        :return:
        """

        try:
            if self.already_init(path) and not force_init:
                Logger.log_error(msg=f"project '{path}' already initialized", is_verbose=self.verbose)
                return False
            else:
                self.remove(path)       # remove project installation, so re-init it

            res = self.settings.set_project_path(path)  # set path of project which must be initialized

            # create work directory inside app if it does NOT exist
            self.create_work_directory()

            if res is False:
                return False

            self.refresh()      # refresh project managed by ProjectManager instance

            Logger.log_info(msg=f"'{path}' project opened", is_verbose=self.verbose)
            return True

        except Exception as e:

            Logger.log_error(msg=f"{e}", full=True, is_verbose=self.verbose)

            return False
