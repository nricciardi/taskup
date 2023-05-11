import os

from lib.app.service.auth import AuthService
from lib.app.service.dashboard import DashboardService
from lib.settings.settings import SettingsManager, SettingsBase
from lib.db.db import DBManager
from lib.utils.utils import Utils
from lib.utils.logger import Logger
from typing import List, Dict, Optional
import os
from lib.db.entity.user import UsersManager, RolesManager, FuturePMData
from lib.db.entity.task import TasksManager, TaskStatusManager, TaskAssignmentsManager, TaskTaskLabelPivotManager, TaskLabelsManager, TodoItemsManager


class ProjectManager:

    def __init__(self, settings_manager: SettingsManager):
        """
        Init project manager, a ProjectManager manages the initialized projects that can be opened
        """

        Logger.log_info(msg="project manager init...", is_verbose=True)

        # AppManager conceded settings manager to ProjectManager, so it can be used to each entity
        self.settings = settings_manager

        # take and set settings
        self.verbose = self.settings.verbose  # set verbose

        # load db manager and entities managers
        if ProjectManager.already_initialized(self.settings.project_directory_path, verbose=self.verbose):
            self.__db_manager: Optional[DBManager] = None        # it's going to override by next method
            self.load_new_db_manager()

            self.task_status_manager = None
            self.roles_manager = None
            self.users_manager = None
            self.tasks_manager = None
            self.task_labels_manager = None
            self.task_task_label_pivot_manager = None
            self.task_assignment_manager = None
            self.todo_items_manager = None
            self.load_entities_managers()

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

    def load_entities_managers(self) -> None:
        """
        Load entities managers

        :return:
        """

        self.task_status_manager = TaskStatusManager(db_manager=self.__db_manager,
                                                     verbose=self.verbose)

        self.todo_items_manager = TodoItemsManager(db_manager=self.__db_manager,
                                                   verbose=self.verbose)

        self.task_assignment_manager = TaskAssignmentsManager(db_manager=self.__db_manager,
                                                              verbose=self.verbose)

        self.task_task_label_pivot_manager = TaskTaskLabelPivotManager(db_manager=self.__db_manager,
                                                                       verbose=self.verbose)

        self.task_labels_manager = TaskLabelsManager(db_manager=self.__db_manager,
                                                     verbose=self.verbose)

        self.tasks_manager = TasksManager(db_manager=self.__db_manager,
                                          task_assignment_manager=self.task_assignment_manager,
                                          task_task_label_pivot_manager=self.task_task_label_pivot_manager,
                                          verbose=self.verbose)

        self.users_manager = UsersManager(db_manager=self.__db_manager,
                                          verbose=self.verbose)

        self.roles_manager = RolesManager(db_manager=self.__db_manager,
                                          verbose=self.verbose)

    def create_work_directory(self, work_directory_path: Optional[str] = None) -> None:
        """
        Create work directory in the app if it doesn't exist

        :rtype None:
        """

        if work_directory_path is None:
            work_directory_path: str = self.__settings_manager.work_directory_path

        try:

            if not Utils.exist_dir(work_directory_path):
                Logger.log_info(msg="create work directory", is_verbose=self.verbose)

                os.mkdir(work_directory_path)

        except Exception as e:
            Logger.log_error(msg=f"error during creation of work directory in project ({work_directory_path})")
            Utils.exit()

    @staticmethod
    def already_initialized(path: str, verbose: bool = False) -> bool:
        """
        Return True if in path there is the work directory

        :param verbose:
        :param path: project path which will be checked
        :return:
        """

        if not Utils.exist_dir(path):
            Logger.log_warning(msg=f"selected project path '{path}' NOT found", is_verbose=verbose)
            return False

        work_directory_name: str = SettingsBase.WORK_DIRECTORY_NAME

        is_init: bool = work_directory_name in os.listdir(path) and os.path.isdir(os.path.join(path, work_directory_name))

        if is_init is False:
            Logger.log_warning(msg=f"project '{path}' not initialized", is_verbose=verbose)

        return is_init

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

        Logger.log_info(msg="refresh project...", is_verbose=self.verbose)

        if ProjectManager.already_initialized(self.settings.project_directory_path):
            return

        # refresh db manager connection with (new) settings
        self.__db_manager.refresh_connection(db_name=self.settings.db_name,
                                             work_directory_path=self.settings.work_directory_path,
                                             use_localtime=self.__settings_manager.get_setting_by_key(self.__settings_manager.KEY_DB_LOCALTIME))

    def remove(self, path: str) -> bool:
        """
        Remove project

        :param path:
        :return:
        """

        try:

            if not ProjectManager.already_initialized(path):
                Logger.log_error(msg=f"project not found in path: '{path}'", is_verbose=self.verbose)
                return False

            work_directory_path = os.path.join(path, self.settings.WORK_DIRECTORY_NAME)

            import shutil

            shutil.rmtree(work_directory_path)

        except Exception as e:
            Logger.log_error(msg=f"{e}", is_verbose=self.verbose)

            return False

    def init_new(self, path: str, future_pm_data: FuturePMData, force_init: bool = False) -> bool:
        """
        Initialized a new project in path with pm as project manager

        :param future_pm_data:
        :param force_init: flag which indicates if overwrite previously init
        :param path:
        :return:
        """

        try:
            if ProjectManager.already_initialized(path) and not force_init:
                Logger.log_error(msg=f"project '{path}' already initialized", is_verbose=self.verbose)
                return False
            else:
                self.remove(path)       # remove project installation, so re-init it

            res = self.settings.set_project_path(path)  # set path of project which must be initialized

            if res is False:
                return False

            # create work directory inside app if it does NOT exist
            self.create_work_directory()

            self.refresh()      # refresh project managed by ProjectManager instance => after this, ProjectManager points to initialized project

            # create project manager of initialized project
            self.users_manager.create_from_dict(dict(**future_pm_data, role_id=self.__db_manager.project_manager_role_id))

            Logger.log_info(msg=f"'{path}' project opened", is_verbose=self.verbose)
            return True

        except Exception as e:

            Logger.log_error(msg=f"{e}", full=True, is_verbose=self.verbose)

            return False

    def open(self, path: str) -> bool:
        """
        Open a project

        :param path:
        :return:
        """

        try:

            if not ProjectManager.already_initialized(path=path):
                return False

            res = self.settings.set_project_path(path)      # set path of project which must be opened

            if res is False:
                return False

            self.refresh()      # refresh project managed by ProjectManager instance

            Logger.log_info(msg=f"'{path}' project opened", is_verbose=self.verbose)
            return True

        except Exception as e:

            Logger.log_error(msg=f"{e}", full=True, is_verbose=self.verbose)

            return False
