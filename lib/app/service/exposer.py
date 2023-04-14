import eel
from lib.utils.logger import Logger
from lib.db.entity.task import TasksManager, TaskStatusManager
from lib.db.entity.user import UsersManager
from lib.app.service.auth import AuthService
from lib.app.service.dashboard import DashboardService
from typing import Callable
from lib.utils.mixin.dcparser import to_dict


class ExposerService:
    """
    Class to expose py method to js

    """

    def __init__(self, db_name: str, work_directory_path: str, vault_path: str, verbose: bool = False):
        self.verbose = verbose

        self.__tasks_manager = TasksManager(db_name=db_name, work_directory_path=work_directory_path,
                                            verbose=self.verbose)

        self.__task_status_manager = TaskStatusManager(db_name=db_name, work_directory_path=work_directory_path,
                                                       verbose=self.verbose)

        self.__users_manager = UsersManager(db_name=db_name, work_directory_path=work_directory_path,
                                            verbose=self.verbose)

        self.__auth_service = AuthService(users_manager=self.__users_manager, vault_path=vault_path,
                                          verbose=self.verbose)

        self.__dashboard_service = DashboardService(tasks_manager=self.__tasks_manager,
                                                    task_status_manager=self.__task_status_manager,
                                                    auth_service=self.__auth_service,
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

            self.expose_all_from_list(to_expose=[
                self.__tasks_manager.create_from_dict,
            ], prefix="task_")

            self.expose(to_dict(self.__tasks_manager.find), "task_find")
            self.expose(to_dict(self.__tasks_manager.all_as_dict), "task_all")

        except Exception as excepetion:
            Logger.log_error(msg="task exposure error", is_verbose=self.verbose, full=True)

    def __expose_auth_methods(self) -> None:
        """
        Expose auth methods

        :return: None
        """

        try:

            self.expose_all_from_list(to_expose=[
                self.__auth_service.is_logged,
                self.__auth_service.logout,
            ], prefix="auth_")

            self.expose(to_dict(self.__auth_service.login), "auth_login")
            self.expose(to_dict(self.__auth_service.me), "auth_me")

        except Exception as excepetion:
            Logger.log_error(msg="auth exposure error", is_verbose=self.verbose, full=True)

    def __expose_dashboard_methods(self) -> None:
        """
        Expose auth methods

        :return: None
        """

        try:

            self.expose(to_dict(self.__dashboard_service.get_data), "dashboard_get_data")

        except Exception as excepetion:
            Logger.log_error(msg="dashboard exposure error", is_verbose=self.verbose, full=True)

    def __expose_user_methods(self) -> None:
        """
        Expose user methods

        :return: None
        """

        try:

            self.expose_all_from_list(to_expose=[
                self.__users_manager.create_from_dict,
            ], prefix="user_")

            self.expose(to_dict(self.__users_manager.find), "user_find")
            self.expose(to_dict(self.__users_manager.all_as_model), "user_all")

        except Exception as excepetion:
            Logger.log_error(msg="user exposure error", is_verbose=self.verbose, full=True)

    def expose_methods(self) -> None:
        """
        Expose py method.

        :rtype None:
        """

        try:
            Logger.log_info(msg="expose py methods...", is_verbose=self.verbose, end=" ")

            self.expose(self.test)

            self.__expose_task_methods()
            self.__expose_user_methods()
            self.__expose_auth_methods()
            self.__expose_dashboard_methods()

            Logger.log_success(msg="OK", is_verbose=self.verbose, prefix=False, msg_row=True)

        except Exception as excepetion:
            Logger.log_error(msg="eel exposure error", is_verbose=self.verbose, full=True)
