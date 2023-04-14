from dataclasses import dataclass
from lib.db.entity.task import TaskStatusModel, TaskModel, TaskStatusManager, TasksManager
from typing import List
from lib.utils.logger import Logger
from lib.utils.mixin.dcparser import DCToDictMixin


@dataclass
class DashboardModel(DCToDictMixin):
    task_status: List[TaskStatusModel]
    default_task_status_id: int
    tasks: List[TaskModel]


class DashboardService:

    def __init__(self, tasks_manager: TasksManager, task_status_manager: TaskStatusManager, verbose: bool = False):
        self.__tasks_manager = tasks_manager
        self.__task_status_manager = task_status_manager
        self.verbose = verbose

    def get_data(self) -> DashboardModel:
        """
        Get data for (frontend) dashboard

        :return:
        :rtype DashboardModel:
        """

        # Logger.log_info(msg="dashboard get data...")

        return DashboardModel(task_status=self.__task_status_manager.all_as_model(),
                              default_task_status_id=self.__task_status_manager.todo_task_status_id,
                              tasks=[])
