import eel
from lib.utils.base import Base
from lib.db.entity.task import TasksManager
from lib.db.entity.user import UsersManager


class ExposerService:
    """
    Class to expose py method to js

    """

    def __init__(self, verbose: bool = False):
        self.__verbose = verbose

    def test(self, *args, **kwargs):
        """
        Method to test connection with frontend

        :param p:
        :return:
        """

        Base.log_eel(msg="Called by JS", is_verbose=self.__verbose)

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
            eel._expose(prefix + k, to_expose[k])

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
                eel._expose(prefix + method.__name__, method)

    def __expose_task_methods(self, db_name: str, work_directory_path: str, verbose: bool) -> None:
        """
        Expose task methods

        :return: None
        """

        try:
            tasks_manager = TasksManager(db_name=db_name, work_directory_path=work_directory_path, verbose=verbose)

            self.expose_all_from_list(to_expose=[
                tasks_manager.all_as_tuple,
                tasks_manager.all_as_dict,
                tasks_manager.create_from_dict,
                tasks_manager.find,
            ], prefix="task_")

        except Exception as excepetion:
            Base.log_error(msg="Task exposure error", is_verbose=self.__verbose, full=True)

    def __expose_user_methods(self, db_name: str, work_directory_path: str, verbose: bool) -> None:
        """
        Expose user methods

        :return: None
        """

        try:
            users_manager = UsersManager(db_name=db_name, work_directory_path=work_directory_path, verbose=verbose)

            self.expose_all_from_list(to_expose=[
                users_manager.all_as_tuple,
                users_manager.all_as_dict,
                users_manager.create_from_dict,
                users_manager.find,
            ], prefix="user_")


        except Exception as excepetion:
            Base.log_error(msg="User exposure error", is_verbose=self.__verbose, full=True)

    def expose_methods(self, db_name: str, work_directory_path: str, verbose: bool) -> None:
        """
        Expose py method.

        :rtype None:
        """

        try:
            Base.log_info(msg="Expose py methods...", is_verbose=self.__verbose, end=" ")

            eel.expose(self.test)

            self.__expose_task_methods(db_name, work_directory_path, verbose)
            self.__expose_user_methods(db_name, work_directory_path, verbose)

        except Exception as excepetion:
            Base.log_error(msg="Eel exposure error", is_verbose=self.__verbose, full=True)
