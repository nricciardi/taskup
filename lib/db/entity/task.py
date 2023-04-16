from lib.db.db import TableNamesMixin, BaseTaskStatusIdMixin
from lib.db.entity.entity import EntitiesManager
from dataclasses import dataclass, field
from lib.db.entity.bem import BaseEntityModel
from datetime import date, datetime
from typing import Type, Optional, List
from lib.db.entity.relation import Relation, OneRelation, ManyRelation
from lib.db.entity.user import UserModel
from lib.db.component import WhereCondition
from lib.utils.logger import Logger


# ================== DATACLASS ==========================
@dataclass
class TaskStatusModel(BaseEntityModel):
    id: int
    name: str
    default_next_task_status_id: int
    default_prev_task_status_id: int
    default_next_task_status: Optional['TaskStatusModel'] = field(default=None)
    default_prev_task_status: Optional['TaskStatusModel'] = field(default=None)
    description: Optional[str] = field(default=None)

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
    rgb_color: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)

    # @property
    # def table_name(self) -> str:
    #     return "task_label"


@dataclass
class TaskModel(BaseEntityModel):
    id: int
    name: str
    priority: int
    created_at: datetime
    updated_at: datetime
    author_id: int
    task_status_id: int
    description: Optional[str] = field(default=None)
    deadline: Optional[datetime] = field(default=None)

    author: Optional[UserModel] = field(default=None)
    task_status: Optional[TaskStatusModel] = field(default=None)
    labels: Optional[List[TaskLabelModel]] = field(default=None)
    users: Optional[List[UserModel]] = field(default=None)

    # @property
    # def table_name(self) -> str:
    #     return "task"


@dataclass
class TaskAssignmentModel(BaseEntityModel):
    id: int
    assigned_at: datetime
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
    priority: int
    created_at: datetime
    updated_at: datetime
    done: bool
    author_id: int
    task_id: int
    author: Optional[UserModel] = field(default=None)
    task: Optional[TaskModel] = field(default=None)
    deadline: Optional[datetime] = field(default=None)

    # @property
    # def table_name(self) -> str:
    #     return "todo_item"


# ================================== MANAGER ========================
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

    @property
    def relations(self) -> list[Relation]:
        return [
            OneRelation(fk_model=TaskStatusModel, of_table=self.task_status_table_name,
                        fk_field="default_next_task_status_id", to_attr="default_next_task_status"),

            OneRelation(fk_model=TaskStatusModel, of_table=self.task_status_table_name,
                        fk_field="default_prev_task_status_id", to_attr="default_prev_task_status"),
        ]


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

    def removeAssignment(self, task_id: int, user_id: int):
        """
        Remove an assignment from task

        :param task_id:
        :type task_id: int
        :param user_id:
        :type user_id: type

        :return: result
        :rtype bool:
        """

        return self.delete(
            WhereCondition(col="user_id", operator="=", value=user_id),
            WhereCondition(col="task_id", operator="=", value=task_id),
        )

    def addAssignment(self, task_id: int, user_id: int):
        """
        Add an assignment from task

        :param task_id:
        :type task_id: int
        :param user_id:
        :type user_id: type

        :return: result
        :rtype bool:
        """

        self.create_from_dict({
            "user_id": user_id,
            "task_id": task_id
        })


class TasksManager(EntitiesManager, TableNamesMixin):
    def __init__(self, db_name: str, work_directory_path: str, task_assignment_manager: TaskAssignmentsManager,
                 verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        self.__task_assignment_manager = task_assignment_manager
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
            ManyRelation(fk_model=TaskLabelModel, of_table=self.task_label_table_name,
                         pivot_model=TaskTaskLabelPivotModel,
                         pivot_table=self.task_task_label_pivot_table_name, to_attr="labels"),
            ManyRelation(fk_model=UserModel, of_table=self.user_table_name, pivot_model=TaskAssignmentModel,
                         pivot_table=self.task_assignment_table_name, to_attr="users")
        ]

    def removeAssignment(self, task_id: int, user_id: int, safe: bool = True) -> bool:
        """
        Remove an assignment from task

        :param task_id:
        :type task_id: int
        :param user_id:
        :type user_id: type
        :param safe: if it is a safe operation
        :type safe: bool

        :return: result
        :rtype bool:
        """

        try:

            self.__task_assignment_manager.removeAssignment(task_id, user_id)

            return True

        except Exception as exception:

            Logger.log_error(msg=exception, full=True, is_verbose=self.verbose)

            if not safe:
                raise exception

            return False

    def addAssignment(self, task_id: int, user_id: int, safe: bool = True) -> bool:
        """
        Add an assignment from task

        :param task_id:
        :type task_id: int
        :param user_id:
        :type user_id: type
        :param safe: if it is a safe operation
        :type safe: bool

        :return: result
        :rtype bool:
        """

        try:

            past_assignment: List[TaskAssignmentModel] = self.__task_assignment_manager.where_as_model(
                WhereCondition(col="task_id", operator="=", value=task_id),
                WhereCondition(col="user_id", operator="=", value=user_id),
            )

            if len(past_assignment) > 0:
                msg: str = f"task (id: {task_id}) already assign (user_id: {user_id})"

                Logger.log_warning(msg=msg, is_verbose=self.verbose)

                return True

            self.__task_assignment_manager.addAssignment(task_id, user_id)

            return True

        except Exception as exception:

            Logger.log_error(msg=exception, full=True, is_verbose=self.verbose)

            if not safe:
                raise exception

            return False


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
