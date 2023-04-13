from lib.db.entity.task import TasksManager
from dataclasses import dataclass
from lib.db.entity.task import TaskStatusModel, TaskModel
from typing import List
from lib.utils.logger import Logger
from lib.mixin.dcparser import DCToDictMixin


@dataclass
class DashboardModel(DCToDictMixin):
    task_status: List[TaskStatusModel]
    default_task_status_id: int
    tasks: List[TaskModel]



class DashboardService:

    def __init__(self, tasks_manager: TasksManager, verbose: bool = False):
        self.__tasks_manager = tasks_manager
        self.verbose = verbose

    def get_data(self):

        Logger.log_info(msg="dashboard get data...")

        return DashboardModel(task_status=[], default_task_status_id=self.__tasks_manager.todo_task_status_id, tasks=[])



