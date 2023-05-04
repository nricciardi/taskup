import sqlite3
from lib.db.query import QueryBuilder
from lib.utils.logger import Logger
import os
from typing import List, Tuple, Dict, Any
from lib.db.component import Table, Field, FKConstraint, WhereCondition, Trigger
from lib.db.seeder import Seeder
from lib.utils.utils import Utils, SqlUtils


def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> Dict:
    """
    Row factory for sqlite3

    :param cursor: sqlite3 cursor
    :type cursor: sqlite3.Cursor
    :param row: row as tuple
    :type row: tuple

    :return:
    """

    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


class TableNamesMixin:
    """
    Provide the table names

    """

    @property
    def user_table_name(self) -> str:
        return "user"

    @property
    def role_table_name(self) -> str:
        return "role"

    @property
    def task_table_name(self) -> str:
        return "task"

    @property
    def task_assignment_table_name(self) -> str:
        return "task_assignment"

    @property
    def todo_item_table_name(self) -> str:
        return "todo_item"

    @property
    def task_label_table_name(self) -> str:
        return "task_label"

    @property
    def task_task_label_pivot_table_name(self) -> str:
        return "task_task_label_pivot"

    @property
    def task_status_table_name(self) -> str:
        return "task_status"


class BaseTaskStatusIdMixin:
    @property
    def ideas_task_status_id(self) -> int:
        return 1

    @property
    def backlog_task_status_id(self) -> int:
        return 2

    @property
    def todo_task_status_id(self) -> int:
        return 3

    @property
    def doing_task_status_id(self) -> int:
        return 4

    @property
    def done_task_status_id(self) -> int:
        return 5

    @property
    def testing_task_status_id(self) -> int:
        return 6

    @property
    def bug_fixing_task_status_id(self) -> int:
        return 7

    @property
    def release_task_status_id(self) -> int:
        return 8


class DBManager(TableNamesMixin, BaseTaskStatusIdMixin):

    def __init__(self, db_name: str, work_directory_path: str = ".", verbose: bool = False,
                 use_localtime: bool = False):
        """
        Create a DBManager

        :param db_name: db name
        :param work_directory_path: work directory path
        :param verbose: verbose
        :param use_localtime: if db must use local in date
        """
        super().__init__()

        # get and set locally variables
        self.verbose = verbose
        self.use_localtime = use_localtime

        self.__db_name: str = db_name
        self.__work_directory_path: str = work_directory_path
        self.__db_path = os.path.join(self.__work_directory_path, self.__db_name)

        # open a new connection
        self.__db_connection = None     # initialized in __init__ to use it in open_connection()
        self.__db_cursor = None         # initialized in __init__ to use it in open_connection()
        self.open_connection()

    def __del__(self):
        self.close_connection()

    def open_connection(self) -> None:
        """
        Open a new connection with DB

        :return:
        """

        # check if db already exists
        db_exists = os.path.exists(self.__db_path)  # if False => database structure must be created

        # log if verbose
        if db_exists:
            Logger.log_info(msg=f"database {self.__db_path} found", is_verbose=self.verbose)
        else:
            Logger.log_warning(msg=f"database {self.__db_path} not found, will be generate...", is_verbose=self.verbose)

        try:
            self.__db_connection = sqlite3.connect(self.__db_path)  # connect to db
            self.__db_connection.row_factory = dict_factory  # set row factory to get dict instead of tuple
            self.__db_cursor = self.__db_connection.cursor()  # set cursor as attr

            Logger.log_success(msg=f"Connection successful with db: {self.__db_path}", is_verbose=self.verbose)

            if not db_exists:
                self.generate_base_db_structure(strict=True)

        except Exception as exception:
            print("Connection with database failed...")

            Logger.log_error(exception, is_verbose=self.verbose)

            Utils.exit()

    def refresh_connection(self) -> None:
        """
        Refresh DB connection

        :return:
        """

        self.open_connection()

    def close_connection(self) -> None:
        """
        Close DB connection

        :return:
        """
        Logger.log_info(msg="closing db connection...", is_verbose=self.verbose)
        self.__db_connection.close()

    @property
    def tables(self) -> Dict[str, Table]:
        """
        Return dict of tables

        :return: tables
        :rtype dict:
        """

        return {
            self.user_table_name: Table(self.user_table_name, [
                Field.id_field(),
                Field(name="username", type="VARCHAR(256)", unique=True),
                Field(name="name", type="VARCHAR(256)", nullable=True),
                Field(name="surname", type="VARCHAR(256)", nullable=True),
                Field(name="email", type="VARCHAR(256)", unique=True),
                Field(name="password", type="VARCHAR(256)", unique=False),
                Field(name="avatar_hex_color", type="VARCHAR(6)", default="'cfcfcf'", nullable=False),
                Field(name="phone", type="VARCHAR(30)", nullable=True),
                Field.fk_field(name="role_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="role_id", on_table=self.role_table_name)
            ]),

            self.role_table_name: Table(self.role_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field(name="permission_create", type="INTEGER", default='1'),
                Field(name="permission_read_all", type="INTEGER", default='0'),
                Field(name="permission_move_backward", type="INTEGER", default='1'),
                Field(name="permission_move_forward", type="INTEGER", default='1'),
                Field(name="permission_edit_own", type="INTEGER", default='1'),
                Field(name="permission_edit_all", type="INTEGER", default='0'),
                Field(name="permission_change_role", type="INTEGER", default='0'),
                Field(name="permission_change_assignment", type="INTEGER", default='0'),
                Field(name="permission_delete_own", type="INTEGER", default='1'),
                Field(name="permission_delete_all", type="INTEGER", default='0'),
            ]),

            self.task_status_table_name: Table(self.task_status_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field.description_field(),
                Field(name="hex_color", type="VARCHAR(6)", nullable=True),
                Field.fk_field(name="default_next_task_status_id", nullable=True),
                Field.fk_field(name="default_prev_task_status_id", nullable=True)
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="default_next_task_status_id", on_table=self.task_status_table_name),
                FKConstraint.on_id(fk_field="default_prev_task_status_id", on_table=self.task_status_table_name)
            ]),

            self.task_table_name: Table(self.task_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field.description_field(),
                Field.nullable_datetime_with_now_check_field(name="deadline"),
                Field(name="priority", type="INTEGER", default="0"),
                Field.created_at_field(),
                Field.updated_at_field(),
                Field.fk_field(name="author_id"),
                Field.fk_field(name="task_status_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="author_id", on_table=self.user_table_name),
                FKConstraint.on_id(fk_field="task_status_id", on_table=self.task_status_table_name),
            ], with_triggers=Trigger(
                name=f"{self.task_table_name}_updater_trigger",
                on_action=f"Update On {self.task_table_name}",
                script=f"Update {self.task_table_name} Set {SqlUtils.UPDATER_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where id = new.id"
            )),

            self.task_label_table_name: Table(self.task_label_table_name, [
                Field.id_field(),
                Field.name_field(unique=True),
                Field.description_field(),
                Field(name="hex_color", type="VARCHAR(6)", nullable=True)
            ]),

            self.task_assignment_table_name: Table.pivot(self.task_assignment_table_name, tables=[
                self.user_table_name,
                self.task_table_name
            ], other_fields=[
                Field.datetime_now("assigned_at"),
                Field.datetime_now("last_visit_at")
            ], with_triggers=Trigger(
                name=f"{self.task_table_name}_updater_trigger",
                on_action=f"Update On {self.task_assignment_table_name}",
                script=f"Update {self.task_table_name} Set {SqlUtils.UPDATER_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where id = new.task_id"
            )),

            self.todo_item_table_name: Table(self.todo_item_table_name, [
                Field.id_field(),
                Field.description_field(nullable=False),
                Field.nullable_datetime_with_now_check_field(name="deadline"),
                Field.created_at_field(),
                Field.updated_at_field(),
                Field(name="done", type="INTEGER", default="0"),
                Field.fk_field(name="author_id"),
                Field.fk_field(name="task_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="author_id", on_table=self.user_table_name),
                FKConstraint.on_id(fk_field="task_id", on_table=self.task_table_name),
            ], with_triggers=Trigger(
                name=f"{self.task_table_name}_updater_trigger",
                on_action=f"Update Of {self.todo_item_table_name} On {self.task_table_name}",
                script=f"Update {self.task_table_name} Set {SqlUtils.UPDATER_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where id = new.task_id"
            )),

            self.task_task_label_pivot_table_name: Table.pivot(self.task_task_label_pivot_table_name, [
                self.task_table_name,
                self.task_label_table_name
            ], with_triggers=Trigger(
                name=f"{self.task_table_name}_updater_trigger",
                on_action=f"Update On {self.task_task_label_pivot_table_name}",
                script=f"Update {self.task_table_name} Set {SqlUtils.UPDATER_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where id = new.task_id"
            ))

        }

    @property
    def seeders(self) -> Dict[str, Seeder]:
        """
        Return the dict of seeders

        :return: seeders
        :rtype dict:
        """

        return {
            self.task_label_table_name: Seeder(table=self.task_label_table_name,
                                               values=[
                                                   ("Front-end", "Front-end tasks", "32a852"),
                                                   ("Back-end", "Front-end tasks", "f56342"),
                                                   ("Documentation", "Documentation tasks", "f242f5")
                                               ], cols=("name", "description", "hex_color")),

            self.role_table_name: Seeder(table=self.role_table_name,
                                         values=[
                                           ("Project Manager",  1, 1, 1, 1,     1, 1, 1, 1,     1, 1),
                                           ("Supervisor",       1, 1, 1, 1,     1, 1, 0, 1,     1, 1),
                                           ("Teammate",         1, 0, 1, 1,     1, 0, 0, 0,     1, 0),
                                           ("Base",             1, 0, 0, 0,     1, 0, 0, 0,     1, 0),
                                           ("External",         0, 0, 0, 0,     0, 0, 0, 0,     0, 0)
                                         ], cols=("name",
                                                  "permission_create", "permission_read_all", "permission_move_backward", "permission_move_forward",
                                                  "permission_edit_own", "permission_edit_all", "permission_change_role", "permission_change_assignment",
                                                  "permission_delete_own", "permission_delete_all"
                                                  )
                                         )
        }

    def run_seeder(self, name) -> None:
        """
        Run seeder by name

        :param name:
        :return:
        """

        try:

            Logger.log_info(f"run seeder: {name}", is_verbose=self.verbose)

            self.cursor.execute(self.seeders[name].to_sql())

            Logger.log_info(f"inserted base data in {self.seeders[name].table}", is_verbose=self.verbose)

        except Exception as exception:

            Logger.log_error(msg=f"error occurs during run seeder: {name}", full=True,
                             is_verbose=self.verbose)

    @property
    def db_path(self):
        return self.__db_path

    @property
    def db_name(self) -> str:
        return self.__db_name

    @db_name.setter
    def db_name(self, name: str) -> None:
        self.__db_name = name

    @db_name.deleter
    def db_name(self):
        raise Exception("db_name cannot be deleted")

    @property
    def connection(self):
        return self.__db_connection

    @property
    def cursor(self):
        return self.__db_cursor

    def create_table(self, table_name: str, if_not_exists: bool = True) -> None:
        """
        Create table

        :param if_not_exists:
        :type if_not_exists: bool
        :type table_name: str
        :param table_name:
        :return:
        """

        query: str = self.tables[table_name].to_sql(if_not_exist=if_not_exists)

        self.cursor.executescript(query)

        Logger.log_info(f"created if not exists {table_name}", is_verbose=self.verbose)

        self.connection.commit()

    def __insert_base_task_status(self) -> None:
        """
        Insert into db base task status

        :return: None
        :rtype None:
        """

        try:

            Logger.log_info(f"start to fill {self.task_status_table_name}", is_verbose=self.verbose)

            # insert default task status
            query = f"""\
                        Insert Into {self.task_status_table_name} (id, name, description, default_next_task_status_id, default_prev_task_status_id, hex_color)
                        Values
                        ({self.release_task_status_id}, "Release", "Task successful tested and released", NULL, NULL, "3eed72"),
                        ({self.done_task_status_id}, "Done", "Task done", {self.release_task_status_id}, NULL, "b4e34f"),
                        ({self.bug_fixing_task_status_id}, "Bug Fixing", "Task with bug to resolve", {self.testing_task_status_id}, NULL, "e84157"),
                        ({self.testing_task_status_id}, "Testing", "Task done in testing", {self.done_task_status_id}, NULL, "facdf3"),
                        ({self.doing_task_status_id}, "Doing", "Task work in progress", {self.testing_task_status_id}, NULL, "ffbf7a"),
                        ({self.todo_task_status_id}, "To-Do", "Task that must be done", {self.doing_task_status_id}, NULL, "73f5fa"),
                        ({self.backlog_task_status_id}, "Backlog", "Tasks to be performed at the end of the most priority tasks", {self.todo_task_status_id}, NULL, "c9eeff"),
                        ({self.ideas_task_status_id}, "Ideas", "Tasks yet to be defined, simple ideas and hints for new features", {self.todo_task_status_id}, NULL, "f5d442");
                    """

            self.cursor.execute(query)

            query = f"""\
                    Update {self.task_status_table_name}
                    Set default_prev_task_status_id = {self.done_task_status_id}
                    Where id = {self.release_task_status_id}
                    """

            self.cursor.execute(query)

            query = f"""\
                    Update {self.task_status_table_name}
                    Set default_prev_task_status_id = {self.doing_task_status_id}
                    Where id in ({self.done_task_status_id}, {self.bug_fixing_task_status_id}, {self.testing_task_status_id})
                    """

            self.cursor.execute(query)

            query = f"""\
                    Update {self.task_status_table_name}
                    Set default_prev_task_status_id = {self.todo_task_status_id}
                    Where id = {self.doing_task_status_id}
                    """

            self.cursor.execute(query)

            query = f"""\
                    Update {self.task_status_table_name}
                    Set default_prev_task_status_id = {self.ideas_task_status_id}
                    Where id = {self.backlog_task_status_id}
                    """

            self.cursor.execute(query)

            query = f"""\
                    Update {self.task_status_table_name}
                    Set default_prev_task_status_id = {self.backlog_task_status_id}
                    Where id = {self.todo_task_status_id}
                    """

            self.cursor.execute(query)

            self.connection.commit()

            Logger.log_info(f"inserted base data in {self.task_status_table_name}", is_verbose=self.verbose)

        except Exception as exception:

            Logger.log_error(msg=f"error occurs during fill {self.task_status_table_name}", full=True,
                             is_verbose=self.verbose)

    @property
    def task_task_label_pivot_table_name(self) -> str:
        return "task_task_label_pivot"

    def generate_base_db_structure(self, strict: bool = False) -> None:
        """
        Generate the base db of app

        :param strict: flag to interrupt application if there is an exception
        :type strict: bool

        :return: None
        :rtype None:
        """

        try:

            Logger.log_info("start to generate base db", is_verbose=self.verbose)

            self.create_table(self.role_table_name)

            self.run_seeder(self.role_table_name)

            self.create_table(self.user_table_name)

            self.create_table(self.task_status_table_name)

            self.__insert_base_task_status()

            self.create_table(self.task_table_name)

            self.create_table(self.task_assignment_table_name)

            self.create_table(self.todo_item_table_name)

            self.create_table(self.task_label_table_name)

            self.run_seeder(self.task_label_table_name)

            self.create_table(self.task_task_label_pivot_table_name)

            self.connection.commit()

            Logger.log_success("base db structure generated", is_verbose=self.verbose)

        except Exception as exception:

            Logger.log_error(msg="error occurs during generate db", full=True, is_verbose=self.verbose)

            if strict:
                Utils.exit()

            raise exception

    def insert_from_tuple(self, table_name: str, values: Tuple | List[Tuple],
                          columns: List[str] | Tuple[str] | None = None) -> None:
        """
        Insert all tuple values passed in a table

        :param table_name:
        :type table_name: str
        :param values: values to insert
        :type values: Tuple | List[Tuple]
        :param columns: fields to use
        :type columns: List[str] | Tuple[str] | None
        """

        if type(values) is not tuple:  # convert single tuple in a list
            t = values.copy()
            values = list()
            values.append(t)

        query = QueryBuilder.from_table(table_name).enable_binding().insert_from_tuple(columns=columns, *values)

        self.cursor.execute(query.to_sql(), query.data_bound)

        self.connection.commit()

    def insert_from_dict(self, table_name: str, values: Dict | List[Dict],
                         columns: List[str] | Tuple[str] | None = None) -> None:
        """
        Insert all dict values passed in a table

        :param table_name:
        :type table_name: str
        :param values: values to insert
        :type values: Dict | List[Dict]
        :param columns: fields to use
        :type columns: List[str] | Tuple[str] | None
        """

        if type(values) is dict:  # convert single dict in a list
            d = values.copy()
            values = list()
            values.append(d)

        query = QueryBuilder.from_table(table_name).enable_binding().insert_from_dict(columns=columns, *values)

        self.cursor.execute(query.to_sql(), query.data_bound)

        self.connection.commit()

    def where(self, table_name: str, *conditions: WhereCondition, columns: List[str] | None = None) -> List[Dict]:
        """
        Filter entities based on conditions

        :param table_name:
        :type table_name: str
        :param columns: columns to get
        :type columns: List[str] | None
        :param conditions: list of conditions
        :type conditions: WhereCondition

        :return: list of records
        :rtype List[Dict]:
        """

        if isinstance(conditions, WhereCondition):
            conditions = [conditions]

        if columns is None:
            columns = []

        query_built = QueryBuilder.from_table(table_name).enable_binding().select(*columns)\
            .apply_conditions(*conditions)

        query: str = query_built.to_sql()
        data: list = query_built.data_bound

        res = self.cursor.execute(query, data)

        return res.fetchall()

    def delete(self, table_name: str, *conditions: WhereCondition):
        """
        Delete data from table

        :param table_name:
        :param conditions:
        :return:
        """

        if isinstance(conditions, WhereCondition):
            conditions = [conditions]

        query_built = QueryBuilder.from_table(table_name).enable_binding().delete().apply_conditions(*conditions)

        query: str = query_built.to_sql()
        data: List = query_built.data_bound

        res = self.cursor.execute(query, data)

        self.connection.commit()

        return res

    def update(self, table_name: str, *conditions: WhereCondition, **data):
        """
        Update row of table_name using data where conditions

        :param table_name:
        :param conditions:
        :param data:
        :return:
        """

        if isinstance(conditions, WhereCondition):
            conditions = [conditions]

        # append updated_at to data with "now" if not exist and if table name has updated_at
        # if "updated_at" in self.tables[table_name]:
        #     data = dict(updated_at=).update(data)

        query_built = QueryBuilder.from_table(table_name)\
                                  .enable_binding()\
                                  .update_from_dict(data)\
                                  .apply_conditions(*conditions)

        query: str = query_built.to_sql()
        data: List = query_built.data_bound

        res = self.cursor.execute(query, data)

        self.connection.commit()

        return res
