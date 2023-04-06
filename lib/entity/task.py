from lib.db.entity import EntityManager
from dataclasses import dataclass
from lib.entity.bem import BaseEntityModel, EM
from datetime import date, datetime
from typing import List, Dict, Any, Type, Optional

from lib.entity.user import UserModel


@dataclass
class TaskStatusModel(BaseEntityModel):
    id: int
    name: str
    description: str
    default_next_task_status_id: int
    default_next_task_status: Optional['TaskStatusModel'] = None


@dataclass
class TaskTaskLabelPivotModel(BaseEntityModel):
    id: int
    name: str
    description: str
    rgb_color: str


@dataclass
class TaskLabelModel(BaseEntityModel):
    id: int
    name: str
    description: str
    rgb_color: str


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
    author: Optional[UserModel] = None
    task_status: Optional[TaskStatusModel] = None


@dataclass
class TaskAssignmentModel(BaseEntityModel):
    id: int
    user_id: int
    task_id: int
    user: Optional[UserModel] = None
    task: Optional[TaskModel] = None


@dataclass
class TodoItemModel(BaseEntityModel):
    id: int
    name: str
    description: str
    deadline: date
    priority: int
    created_at: datetime
    updated_at: datetime
    done: bool
    author_id: int
    task_id: int
    author: Optional[UserModel] = None
    task: Optional[TaskModel] = None


class TasksManager(EntityManager):
    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose,
                         work_directory_path=work_directory_path)

    @property
    def EM(self) -> Type[TaskModel]:
        return TaskModel

    @property
    def table_name(self) -> str:
        return "task"


class TaskStatusManager(EntityManager):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose, work_directory_path=work_directory_path)

    @property
    def EM(self) -> Type[TaskStatusModel]:
        return TaskStatusModel

    @property
    def table_name(self) -> str:
        return "task_status"


class TodoItemsManager(EntityManager):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose, work_directory_path=work_directory_path)

    @property
    def table_name(self) -> str:
        return "todo_list"

    @property
    def EM(self) -> Type[TodoItemModel]:
        return TodoItemModel


class TaskLabelsManager(EntityManager):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose,
                         work_directory_path=work_directory_path)

    @property
    def table_name(self) -> str:
        return "task_label"

    @property
    def EM(self) -> Type[TaskLabelModel]:
        return TaskLabelModel


class TaskAssignmentsManager(EntityManager):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose,
                         work_directory_path=work_directory_path)

    @property
    def table_name(self) -> str:
        return "task_assignment"

    @property
    def EM(self) -> Type[TaskAssignmentModel]:
        return TaskAssignmentModel
