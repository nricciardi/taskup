from dataclasses import dataclass
from lib.db.entity.task import TaskStatusModel, TaskModel, TaskStatusManager, TasksManager
from lib.db.entity.user import UserModel
from typing import List
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

        tasks = []

        if self.__auth_service.is_logged():         # take list of user logged task
            user_logged: UserModel = self.__auth_service.me()

            if user_logged is not None:
                tasks = self.__tasks_manager.where_as_model(
                    WhereCondition(col="author_id", operator="=", value=user_logged.id)
                )

            # Logger.log_info(msg=f"dashboard get tasks... {tasks}", is_verbose=self.verbose)       too computationally demanding

        return DashboardModel(task_status=self.__task_status_manager.all_as_model(),
                              default_task_status_id=self.__task_status_manager.todo_task_status_id,
                              tasks=tasks)
