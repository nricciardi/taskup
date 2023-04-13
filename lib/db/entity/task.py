from lib.db.db import TableNamesMixin, BaseTaskStatusIdMixin
from lib.db.entity.entity import EntitiesManager
from dataclasses import dataclass
from lib.db.entity.bem import BaseEntityModel
from datetime import date, datetime
from typing import Type, Optional, List
from lib.db.entity.relation import Relation, OneRelation, ManyRelation
from lib.db.entity.user import UserModel


# ================== DATACLASS ==========================
@dataclass
class TaskStatusModel(BaseEntityModel):
    id: int
    name: str
    description: str
    default_next_task_status_id: int
    default_next_task_status: Optional['TaskStatusModel'] = None

    # @property
    # def table_name(self) -> str:
    #     return "task_status"


@dataclass
class TaskTaskLabelPivotModel(BaseEntityModel):
    id: int
    task_id: int
    task_label_id: int

    # @property
    # def table_name(self) -> str:
    #     return "task_task_label_pivot"


@dataclass
class TaskLabelModel(BaseEntityModel):
    id: int
    name: str
    description: str
    rgb_color: str

    # @property
    # def table_name(self) -> str:
    #     return "task_label"


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
    labels: Optional[List[TaskLabelModel]] = None

    # @property
    # def table_name(self) -> str:
    #     return "task"


@dataclass
class TaskAssignmentModel(BaseEntityModel):
    id: int
    user_id: int
    task_id: int

    # @property
    # def table_name(self) -> str:
    #     return "task_assignment"


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

    # @property
    # def table_name(self) -> str:
    #     return "todo_item"


# ================================== MANAGER ========================
class TasksManager(EntitiesManager, TableNamesMixin):
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
        return self.task_table_name

    @property
    def relations(self) -> list[Relation]:
        return [
            OneRelation(fk_model=UserModel, of_table=self.user_table_name, fk_field="author_id", to_attr="author"),
            OneRelation(fk_model=TaskStatusModel, of_table=self.task_status_table_name, fk_field="task_status_id",
                        to_attr="task_status"),
            ManyRelation(fk_model=TaskLabelModel, of_table=self.task_label_table_name, pivot_model=TaskTaskLabelPivotModel,
                         pivot_table=self.task_task_label_pivot_table_name, to_attr="labels")
        ]


class TaskStatusManager(EntitiesManager, TableNamesMixin, BaseTaskStatusIdMixin):

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
        return self.task_status_table_name


class TodoItemsManager(EntitiesManager, TableNamesMixin):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose, work_directory_path=work_directory_path)

    @property
    def table_name(self) -> str:
        return self.todo_item_table_name

    @property
    def EM(self) -> Type[TodoItemModel]:
        return TodoItemModel


class TaskLabelsManager(EntitiesManager, TableNamesMixin):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose,
                         work_directory_path=work_directory_path)

    @property
    def table_name(self) -> str:
        return self.task_label_table_name

    @property
    def EM(self) -> Type[TaskLabelModel]:
        return TaskLabelModel


class TaskAssignmentsManager(EntitiesManager, TableNamesMixin):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose,
                         work_directory_path=work_directory_path)

    @property
    def table_name(self) -> str:
        return self.task_assignment_table_name

    @property
    def EM(self) -> Type[TaskAssignmentModel]:
        return TaskAssignmentModel
