from lib.settings.settings import SettingsManager, SettingsBase
from lib.db.db import DBManager
from lib.utils.utils import Utils
from lib.utils.logger import Logger
from typing import Dict, Optional
import os
from lib.db.entity.user import UsersManager, RolesManager, FuturePMData
from lib.db.entity.task import TasksManager, TaskStatusManager, TaskAssignmentsManager, TaskTaskLabelPivotManager, TaskLabelsManager, TodoItemsManager
from lib.repo.repo import RepoManager


class ProjectManager:

    def __init__(self, settings_manager: SettingsManager):
        """
        Init project manager, a ProjectManager manages the initialized projects that can be opened
        """

        Logger.log_info(msg="project manager init...", is_verbose=True)

        # AppManager conceded settings manager to ProjectManager, so it can be used to each entity
        self.settings = settings_manager

        self.verbose = self.settings.verbose  # set verbose

        # instance (only one) DBManager
        try:
            # get app settings
            use_localtime = self.settings.get_setting_by_key(self.__settings_manager.KEY_DB_LOCALTIME)

            self.__db_manager: DBManager = DBManager(db_path=self.settings.db_path,
                                                     verbose=self.verbose,
                                                     use_localtime=use_localtime)

        except Exception as exception:
            Logger.log_error(msg="error while instance dbmanager", is_verbose=self.verbose)

        # load entities
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

        # load repo manager
        self.repo_manager = RepoManager(verbose=self.verbose,
                                        # DEPRECATED: users_models=self.users_manager.all_as_model(with_relations=False, safe=True),
                                        # DEPRECATED: tasks_models=self.tasks_manager.all_as_model(with_relations=False, safe=True)
                                        )

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

    def create_work_directory(self, path: Optional[str] = None) -> str:
        """
        Create work directory in the project if it doesn't exist

        :rtype None:
        """

        if path is not None:
            work_directory_path: str = os.path.join(path, SettingsBase.WORK_DIRECTORY_NAME)
        else:
            work_directory_path: str = self.settings.work_directory_path

        try:

            if not Utils.exist_dir(work_directory_path):
                Logger.log_info(msg=f"create work directory '{work_directory_path}'", is_verbose=self.verbose)

                os.mkdir(work_directory_path)

        except Exception as e:
            Logger.log_error(msg=f"error during creation of work directory in project ({work_directory_path})")

        return work_directory_path

    @staticmethod
    def already_initialized(project_path: str, verbose: bool = False) -> bool:
        """
        Return True if in path there is the work directory

        :param verbose:
        :param project_path: project path which will be checked
        :return:
        """

        if not Utils.exist_dir(project_path):
            Logger.log_warning(msg=f"selected project path '{project_path}' NOT found", is_verbose=verbose)
            return False

        is_init: bool = SettingsBase.WORK_DIRECTORY_NAME in os.listdir(project_path)

        if is_init:
            Logger.log_info(msg=f"project '{project_path}' initialized", is_verbose=verbose)
        else:
            Logger.log_warning(msg=f"project '{project_path}' not initialized", is_verbose=verbose)

        return is_init

    def project_information(self) -> Dict | None:
        """
        Return key-value project information

        :return:
        """

        if not ProjectManager.already_initialized(self.__settings_manager.project_directory_path):
            return None

        return {
            "path": self.__settings_manager.project_directory_path,
            "database_path": self.__db_manager.db_path
        }

    def refresh(self) -> None:
        """
        Refresh project managed refreshing database manager

        :return:
        """

        Logger.log_info(msg="refreshing project...", is_verbose=self.verbose)

        # refresh db manager connection with (new) settings
        self.__db_manager.refresh_connection(db_path=self.settings.db_path,
                                             use_localtime=self.__settings_manager.get_setting_by_key(self.__settings_manager.KEY_DB_LOCALTIME))

        self.repo_manager.open_repo(self.settings.project_directory_path)

    def remove(self, project_path: str) -> bool:
        """
        Remove app from project

        :param project_path:
        :return:
        """

        try:

            if not ProjectManager.already_initialized(project_path):
                Logger.log_error(msg=f"project not found in path: '{project_path}'", is_verbose=self.verbose)
                return False

            work_directory_path = SettingsManager.assemble_work_directory_path(project_path)

            import shutil

            shutil.rmtree(work_directory_path)      # remove all files in work directory recursively

            Logger.log_success(msg=f"project '{project_path}' removed", is_verbose=self.verbose)

            return True

        except Exception as e:
            Logger.log_error(msg=f"{e}", is_verbose=self.verbose)

            return False

    def init_new(self, project_path: str, future_pm_data: FuturePMData, force_init: bool = False) -> bool:
        """
        Initialized a new project in path with pm as project manager

        :param future_pm_data:
        :param force_init: flag which indicates if overwrite previously init
        :param project_path:
        :return:
        """

        try:
            # list of controls to check if dir exists and the project is already initialized
            if Utils.exist_dir(project_path) is False:
                Logger.log_error(msg=f"directory '{project_path}' not found", is_verbose=self.verbose)

                if force_init:
                    os.makedirs(project_path)
                else:
                    return False

            if ProjectManager.already_initialized(project_path, verbose=False) and not force_init:
                Logger.log_error(msg=f"project '{project_path}' already initialized", is_verbose=self.verbose)
                return False
            else:
                Logger.log_warning(msg=f"project '{project_path}' will be initialized again", is_verbose=self.verbose)
                self.remove(project_path=project_path)       # remove project installation, so re-init it

            # end of controls list...

            # create work directory inside project if it does NOT exist
            work_dir = self.create_work_directory(project_path)

            # instance specific DBManager to create new db
            db_manager = DBManager.creating_database(db_path=SettingsManager.assemble_db_path(work_dir_path=work_dir),
                                                     verbose=self.verbose,
                                                     use_localtime=self.settings.get_setting_by_key(SettingsManager.KEY_DB_LOCALTIME))

            if db_manager is None:      # check error
                return False

            db_manager.generate_base_db_structure(strict=False)       # generate base structure

            # create project manager of initialized project
            users_manager = UsersManager(db_manager=db_manager)
            users_manager.create_from_dict(dict(**future_pm_data, role_id=db_manager.project_manager_role_id))

            Logger.log_info(msg=f"'{project_path}' project have been initialized", is_verbose=self.verbose)
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

            # a project which is NOT initialized cannot be opened
            if not ProjectManager.already_initialized(project_path=path, verbose=self.verbose):
                return False

            res = self.settings.set_project_path(path)      # set path of project which must be opened

            if res is False:        # log if settings' set have failed
                Logger.log_error(msg=f"invalid path: {path}")
                return False

            self.refresh()      # refresh project managed by the current ProjectManager instance

            Logger.log_info(msg=f"'{path}' project opened", is_verbose=self.verbose)
            return True

        except Exception as e:

            Logger.log_error(msg=f"{e}", full=True, is_verbose=self.verbose)

            return False
