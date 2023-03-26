from lib.db.entity_manager import EntityManager
from dataclasses import dataclass
from lib.entity.bem import BaseEntityModel
from lib.settings.settings_manager import SettingsManager
from datetime import date, datetime


@dataclass
class TaskModel(BaseEntityModel):
    id: int
    name: str
    description: str
    deadline: date
    priority: int
    created_at: datetime
    updated_at: datetime
    author_id: int
    task_status_id: int


class TasksManager(EntityManager):
    __table_name = "task"
    __settings_manager = SettingsManager()

    def __init__(self):
        verbose = self.__settings_manager.get(self.__settings_manager.VERBOSE_KEY)
        db_name = self.__settings_manager.get(self.__settings_manager.DB_NAME_KEY)
        work_directory_path = self.__settings_manager.work_directory_path()

        super().__init__(db_name=db_name, table_name=self.__table_name, verbose=verbose,
                         work_directory_path=work_directory_path)

    def find(self, task_id: int) -> TaskModel:
        """
        Find the task status with specified id

        :param task_id: task status id
        :type task_id: int

        :return: TaskModel
        :rtype TaskModel:
        """

        data = super().find(task_id)

        return TaskModel.from_tuple(data)

    def create(self, data: dict) -> TaskModel:
        """
        Create the task from data

        :param data: task data
        :type data: dict

        :return: TaskModel
        :rtype TaskModel:
        """

        data = super().create(data)

        return data


@dataclass
class TaskStatusModel(BaseEntityModel):
    id: int
    name: str
    description: str
    default_next_task_status_id: int


class TaskStatusManager(EntityManager):
    __table_name = "task_status"
    __settings_manager = SettingsManager()

    def __init__(self):
        verbose = self.__settings_manager.get(self.__settings_manager.VERBOSE_KEY)
        db_name = self.__settings_manager.get(self.__settings_manager.DB_NAME_KEY)
        work_directory_path = self.__settings_manager.work_directory_path()

        super().__init__(db_name=db_name, table_name=self.__table_name, verbose=verbose,
                         work_directory_path=work_directory_path)

    def find(self, task_status_id: int) -> TaskStatusModel:
        """
        Find the task status with specified id

        :param task_status_id: task status id
        :type task_status_id: int

        :return: TaskStatusModel
        :rtype TaskStatusModel:
        """

        data = super().find(task_status_id)

        return TaskStatusModel.from_tuple(data)

    def create(self, data: dict) -> TaskStatusModel:
        """
        Create the task status from data

        :param data: task status data
        :type data: dict

        :return: TaskStatusModel
        :rtype TaskStatusModel:
        """

        data = super().create(data)

        return data
