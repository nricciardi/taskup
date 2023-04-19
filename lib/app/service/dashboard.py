from dataclasses import dataclass
from lib.db.entity.task import TaskStatusModel, TaskModel, TaskStatusManager, TasksManager
from lib.db.entity.user import UserModel
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


class DashboardService:

    def __init__(self, tasks_manager: TasksManager, task_status_manager: TaskStatusManager, auth_service: AuthService, verbose: bool = False):
        self.__tasks_manager = tasks_manager
        self.__task_status_manager = task_status_manager
        self.__auth_service = auth_service
        self.verbose = verbose

    def get_data(self) -> DashboardModel:
        """
        Get data for (frontend) dashboard

        :return:
        :rtype DashboardModel:
        """

        if self.__auth_service.is_logged():         # take list of user logged task
            user_logged: UserModel = self.__auth_service.me()

            if user_logged is not None:
                tasks: List[TaskModel] = self.__tasks_manager.all_as_model(with_relations=True)

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
                            if u.id == user_logged.id:
                                return True

                    return False

                tasks: List[TaskModel] = list(filter(filter_by_assignment, tasks))

                dm = DashboardModel(task_status=self.__task_status_manager.all_as_model(),
                                    default_task_status_id=self.__task_status_manager.doing_task_status_id,
                                    tasks=tasks)

                Logger.log_info(msg=f"dashboard get {len(dm.tasks)} task(s)", is_verbose=self.verbose)

                return dm
