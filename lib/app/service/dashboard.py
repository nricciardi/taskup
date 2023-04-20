from dataclasses import dataclass
from lib.db.entity.task import TaskStatusModel, TaskModel, TaskStatusManager, TasksManager
from lib.db.entity.user import UserModel, RoleModel, RolesManager
from typing import List, Callable
from lib.utils.logger import Logger
from lib.utils.mixin.dcparser import DCToDictMixin
from lib.app.service.auth import AuthService
from lib.db.component import WhereCondition


@dataclass
class DashboardModel(DCToDictMixin):
    task_status: List[TaskStatusModel]
    default_task_status_id: int
    tasks: List[TaskModel]
    of_user: UserModel     # to impersonate other user


class DashboardService:

    def __init__(self, tasks_manager: TasksManager, task_status_manager: TaskStatusManager,
                 auth_service: AuthService, roles_manager: RolesManager, verbose: bool = False):

        self.__tasks_manager = tasks_manager
        self.__task_status_manager = task_status_manager
        self.__auth_service = auth_service
        self.__roles_manager = roles_manager
        self.verbose = verbose

    def get_data(self) -> DashboardModel:
        """
        Get data for (frontend) dashboard

        :return:
        :rtype DashboardModel:
        """

        if self.__auth_service.is_logged():  # take list of logged user task
            logged_user: UserModel = self.__auth_service.me()

            if logged_user is not None:
                logged_user_role: RoleModel | None = self.__roles_manager.find(logged_user.role_id)

                tasks: List[TaskModel] = self.__tasks_manager.all_as_model(with_relations=True)

                if logged_user_role is None or bool(logged_user_role.permission_read_all) is False:
                    Logger.log_info(msg="Take only user assigned task...", is_verbose=self.verbose)

                    def filter_by_assignment(t: TaskModel) -> bool:
                        """
                        Filter function to take only the tasks t with the logged user in users (assignment)

                        :param t: task
                        :type t: TaskModel
                        :return:
                        :rtype: bool
                        """

                        if t.users is not None:
                            for u in t.users:
                                if u.id == logged_user.id:
                                    return True

                        return False

                    tasks: List[TaskModel] = list(filter(filter_by_assignment, tasks))

                dm = DashboardModel(task_status=self.__task_status_manager.all_as_model(),
                                    default_task_status_id=self.__task_status_manager.doing_task_status_id,
                                    tasks=tasks,
                                    of_user=self.__auth_service.me())

                Logger.log_info(msg=f"dashboard get {len(dm.tasks)} task(s)", is_verbose=self.verbose)

                return dm
