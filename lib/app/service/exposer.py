import eel
from lib.utils.logger import Logger
from lib.db.entity.task import TasksManager, TaskStatusManager, TaskAssignmentsManager, TaskTaskLabelPivotManager, TaskLabelsManager, TodoItemsManager
from lib.db.entity.user import UsersManager, RolesManager
from lib.app.service.auth import AuthService, login_required, permission_required
from lib.app.service.dashboard import DashboardService
from typing import Callable
from lib.utils.mixin.dcparser import to_dict
import json
from lib.utils.utils import Utils


def jsonify(func: Callable):
    """
    Decorator to dumps returned values of func

    :param func:
    :type func: Callable
    :return: values as json
    :rtype str:
    """

    def wrapped():
        return json.dumps(func())

    return wrapped


class ExposerService:
    """
    Class to expose py method to js

    """

    def __init__(self, app_manager, verbose: bool = False):
        self.verbose = verbose

        self.__app_manager = app_manager

        db_manager = self.__app_manager.project_manager.db_manager
        vault_path = self.__app_manager.project_manager.settings.vault_path

        self.__project_manager = self.__app_manager.project_manager

        self.__task_status_manager = TaskStatusManager(db_manager=db_manager,
                                                       verbose=self.verbose)

        self.__todo_items_manager = TodoItemsManager(db_manager=db_manager,
                                                     verbose=self.verbose)

        self.__task_assignment_manager = TaskAssignmentsManager(db_manager=db_manager,
                                                                verbose=self.verbose)

        self.__task_task_label_pivot_manager = TaskTaskLabelPivotManager(db_manager=db_manager,
                                                                         verbose=self.verbose)

        self.__task_labels_manager = TaskLabelsManager(db_manager=db_manager,
                                                       verbose=self.verbose)

        self.__tasks_manager = TasksManager(db_manager=db_manager,
                                            task_assignment_manager=self.__task_assignment_manager,
                                            task_task_label_pivot_manager=self.__task_task_label_pivot_manager,
                                            verbose=self.verbose)

        self.__users_manager = UsersManager(db_manager=db_manager,
                                            verbose=self.verbose)

        self.__roles_manager = RolesManager(db_manager=db_manager,
                                            verbose=self.verbose)

        self.__auth_service = AuthService(users_manager=self.__users_manager, vault_path=vault_path,
                                          verbose=self.verbose)

        self.__dashboard_service = DashboardService(tasks_manager=self.__tasks_manager,
                                                    task_status_manager=self.__task_status_manager,
                                                    auth_service=self.__auth_service,
                                                    roles_manager=self.__roles_manager,
                                                    verbose=self.verbose)

    def test(self, *args, **kwargs):
        """
        Method to test connection with frontend

        :param p:
        :return:
        """

        Logger.log_eel(msg="test called by JS", is_verbose=self.verbose)

        print(args, kwargs)

        return args, kwargs

    @staticmethod
    def expose_all_from_dict(to_expose: dict, prefix: str = "") -> None:
        """
        Expose all method passed in a dict

        :param to_expose: alias-method dictionary
        :type to_expose: dict
        :param prefix: prefix to add in alias
        :type prefix: str

        :return: None
        """

        for k in to_expose.keys():
            ExposerService.expose(to_expose[k], alias=prefix + k)

    @staticmethod
    def expose_all_from_list(to_expose: list, prefix: str = "") -> None:
        """
        Expose all method passed in a list

        :param to_expose: methods
        :type to_expose: list
        :param prefix: prefix to add in alias
        :type prefix: str

        :return: None
        """

        for method in to_expose:
            if callable(method):
                ExposerService.expose(method, alias=prefix + method.__name__)

    @staticmethod
    def expose(method: Callable, alias: str | None = None):

        if alias is None:
            eel.expose(method)

        elif alias is not None:
            eel._expose(alias, method)

    def __expose_task_methods(self) -> None:
        """
        Expose task methods

        :return: None
        """

        try:

            # expose task
            self.expose_all_from_list(to_expose=[
                self.__tasks_manager.remove_assignment,
                self.__tasks_manager.add_assignment,
                self.__tasks_manager.delete_by_id,
                self.__tasks_manager.add_label,
                self.__tasks_manager.remove_label,
                self.__tasks_manager.check_already_used,
            ], prefix="task_")

            self.expose(to_dict(self.__tasks_manager.create_from_dict, self.verbose), "task_create")
            self.expose(to_dict(self.__tasks_manager.find, self.verbose), "task_find")
            self.expose(login_required(self.__tasks_manager.all_as_dict, self.__auth_service, self.verbose), "task_all")
            self.expose(login_required(to_dict(self.__tasks_manager.update_from_dict), self.__auth_service, self.verbose), "task_update")

        except Exception as excepetion:
            Logger.log_error(msg="task exposure error", is_verbose=self.verbose, full=True)

    def __expose_todo_items_methods(self) -> None:
        """
        Expose to-do items methods

        :return: None
        """

        try:
            # expose to-do
            self.expose_all_from_list(to_expose=[
                self.__todo_items_manager.delete_by_id,
                self.__todo_items_manager.check_already_used,
            ], prefix="todo_")

            self.expose(to_dict(self.__todo_items_manager.create_from_dict, self.verbose), "todo_create")
            self.expose(to_dict(self.__todo_items_manager.find, self.verbose), "todo_find")
            self.expose(login_required(to_dict(self.__todo_items_manager.all_as_dict), self.__auth_service, self.verbose), "todo_all")
            self.expose(login_required(to_dict(self.__todo_items_manager.all_of), self.__auth_service, self.verbose), "todo_all_of")
            self.expose(login_required(to_dict(self.__todo_items_manager.update_from_dict), self.__auth_service, self.verbose), "todo_update")

        except Exception as excepetion:
            Logger.log_error(msg="todo items exposure error", is_verbose=self.verbose, full=True)

    def __expose_task_label_methods(self) -> None:
        """
        Expose task labels methods

        :return: None
        """

        try:
            # expose task label
            self.expose_all_from_list(to_expose=[
                self.__task_labels_manager.delete_by_id,
                self.__task_labels_manager.check_already_used,
            ], prefix="task_label_")

            self.expose(to_dict(self.__task_labels_manager.create_from_dict, self.verbose), "task_label_create")
            self.expose(to_dict(self.__task_labels_manager.find, self.verbose), "task_label_find")
            self.expose(login_required(to_dict(self.__task_labels_manager.all_as_dict), self.__auth_service, self.verbose), "task_label_all")
            self.expose(login_required(to_dict(self.__task_labels_manager.update_from_dict), self.__auth_service, self.verbose), "task_label_update")

        except Exception as excepetion:
            Logger.log_error(msg="task labels exposure error", is_verbose=self.verbose, full=True)

    def __expose_task_status_methods(self) -> None:
        """
        Expose task labels methods

        :return: None
        """

        try:
            # expose task status
            self.expose_all_from_list(to_expose=[
                self.__task_status_manager.create_from_dict,
                self.__task_status_manager.delete_by_id,
                self.__task_status_manager.check_already_used,

            ], prefix="task_status_")

            self.expose(to_dict(self.__task_status_manager.create_from_dict, self.verbose), "task_status_create")
            self.expose(to_dict(self.__task_status_manager.find, self.verbose), "task_status_find")
            self.expose(login_required(to_dict(self.__task_status_manager.all_as_dict), self.__auth_service, self.verbose), "task_status_all")
            self.expose(login_required(to_dict(self.__task_status_manager.update_from_dict), self.__auth_service, self.verbose), "task_status_update")

        except Exception as excepetion:
            Logger.log_error(msg="task status exposure error", is_verbose=self.verbose, full=True)

    def __expose_task_assignments_methods(self) -> None:
        """
        Expose task labels methods

        :return: None
        """

        try:
            # expose task status
            self.expose_all_from_list(to_expose=[
                self.__task_assignment_manager.delete_by_id,
                self.__task_assignment_manager.check_already_used,

            ], prefix="task_assignment_")

            self.expose(to_dict(self.__task_assignment_manager.create_from_dict, self.verbose), "task_assignment_create")
            self.expose(to_dict(self.__task_assignment_manager.find, self.verbose), "task_assignment_find")
            self.expose(login_required(to_dict(self.__task_assignment_manager.all_as_dict), self.__auth_service, self.verbose), "task_assignment_all")
            self.expose(login_required(to_dict(self.__task_assignment_manager.update_from_dict), self.__auth_service, self.verbose), "task_assignment_update")
            self.expose(login_required(to_dict(self.__task_assignment_manager.update_by_task_user_id_from_dict), self.__auth_service, self.verbose), "task_assignment_update_by_task_user_id_from_dict")

        except Exception as excepetion:
            Logger.log_error(msg="roles exposure error", is_verbose=self.verbose, full=True)

    def __expose_role_methods(self) -> None:
        """
        Expose task labels methods

        :return: None
        """

        try:
            # expose task status
            self.expose_all_from_list(to_expose=[
                self.__roles_manager.delete_by_id,
                self.__roles_manager.check_already_used,

            ], prefix="role_")

            self.expose(to_dict(self.__roles_manager.create_from_dict, self.verbose), "role_create")
            self.expose(to_dict(self.__roles_manager.find, self.verbose), "role_find")
            self.expose(login_required(to_dict(self.__roles_manager.all_as_dict), self.__auth_service, self.verbose), "role_all")
            self.expose(login_required(to_dict(self.__roles_manager.update_from_dict), self.__auth_service, self.verbose), "role_update")

        except Exception as excepetion:
            Logger.log_error(msg="roles exposure error", is_verbose=self.verbose, full=True)

    def __expose_auth_methods(self) -> None:
        """
        Expose auth methods

        :return: None
        """

        try:

            self.expose_all_from_list(to_expose=[
                self.__auth_service.is_logged,
                self.__auth_service.logout,
                self.__auth_service.refresh_me,
                self.__auth_service.update_last_visit
            ], prefix="auth_")

            self.expose(to_dict(self.__auth_service.login, self.verbose), "auth_login")
            self.expose(to_dict(self.__auth_service.me, self.verbose), "auth_me")

        except Exception as excepetion:
            Logger.log_error(msg="auth exposure error", is_verbose=self.verbose, full=True)

    def __expose_project_manager_methods(self) -> None:
        """
        Expose project manager methods

        :return: None
        """

        try:

            self.expose_all_from_list(to_expose=[
                self.__project_manager.get_projects_paths_stored,
                self.__project_manager.set_project_path,
                self.__project_manager.project_information,
            ], prefix="project_")

        except Exception as excepetion:
            Logger.log_error(msg="project manager exposure error", is_verbose=self.verbose, full=True)

    def __expose_app_methods(self) -> None:
        """
        Expose app methods

        :return: None
        """

        try:

            self.expose_all_from_list(to_expose=[
                self.__app_manager.open_settings,
                self.__app_manager.version
            ], prefix="app_")

        except Exception as excepetion:
            Logger.log_error(msg="app exposure error", is_verbose=self.verbose, full=True)

    def __expose_utils_methods(self) -> None:
        """
        Expose utils methods

        :return: None
        """

        try:

            self.expose_all_from_list(to_expose=[
                Utils.exit,
                Utils.open_in_webbrowser,
            ], prefix="utils_")

        except Exception as excepetion:
            Logger.log_error(msg="utils exposure error", is_verbose=self.verbose, full=True)

    def __expose_dashboard_methods(self) -> None:
        """
        Expose auth methods

        :return: None
        """

        try:

            self.expose(to_dict(self.__dashboard_service.get_data, self.verbose), "dashboard_get_data")

        except Exception as excepetion:
            Logger.log_error(msg="dashboard exposure error", is_verbose=self.verbose, full=True)

    def __expose_user_methods(self) -> None:
        """
        Expose user methods

        :return: None
        """

        try:

            self.expose_all_from_list(to_expose=[
                self.__users_manager.delete_by_id,
                self.__users_manager.check_already_used,
            ], prefix="user_")

            self.expose(to_dict(self.__users_manager.find, self.verbose), "user_find")
            self.expose(to_dict(self.__users_manager.create_from_dict, self.verbose), "user_create")
            self.expose(login_required(self.__users_manager.all_as_dict, self.__auth_service, self.verbose), "user_all")
            self.expose(login_required(to_dict(self.__users_manager.update_from_dict), self.__auth_service, self.verbose), "user_update")

        except Exception as excepetion:
            Logger.log_error(msg="user exposure error", is_verbose=self.verbose, full=True)

    def expose_methods(self) -> None:
        """
        Expose py method.

        :rtype None:
        """

        try:
            Logger.log_info(msg="expose py methods...", is_verbose=self.verbose)

            self.expose(self.test)

            self.__expose_task_methods()
            self.__expose_task_label_methods()
            self.__expose_todo_items_methods()
            self.__expose_task_status_methods()
            self.__expose_task_assignments_methods()
            self.__expose_user_methods()
            self.__expose_role_methods()
            self.__expose_auth_methods()
            self.__expose_dashboard_methods()
            self.__expose_project_manager_methods()
            self.__expose_app_methods()
            self.__expose_utils_methods()

            Logger.log_success(msg="methods exposed", is_verbose=self.verbose)

        except Exception as excepetion:
            Logger.log_error(msg="eel exposure error", is_verbose=self.verbose, full=True)
