import sqlite3
from lib.db.query import QueryBuilder
from lib.utils.logger import Logger
from typing import List, Tuple, Dict, Optional, Any
from lib.db.component import Table, Field, FKConstraint, WhereCondition, Trigger
from lib.db.seeder import Seeder
from lib.utils.utils import Utils, SqlUtils
from lib.utils.collections import DictUtils


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


class BaseRoleIdMixin:
    @property
    def project_manager_role_id(self) -> int:
        return 1


class DBManager(TableNamesMixin, BaseTaskStatusIdMixin, BaseRoleIdMixin):

    def __init__(self, db_path: str, verbose: bool = False, use_localtime: bool = False):
        """
        Create a DBManager

        :param db_path: db path
        :param verbose: verbose
        :param use_localtime: if db must use local in date
        """
        super().__init__()

        # get and set locally variables
        self.verbose = verbose

        self.use_localtime = use_localtime
        self.__db_path = db_path

        # open a new connection
        self.__db_connection = None     # initialized in __init__ to use it in open_connection()
        self.__db_cursor = None         # initialized in __init__ to use it in open_connection()
        self.open_connection()

    def __del__(self):
        self.close_connection()

    def set_connection_params(self, db_path: Optional[str] = None, use_localtime: Optional[bool] = None):
        """
        Set params to open connections

        :param db_path:
        :param use_localtime:
        :return:
        """

        if use_localtime is not None:
            self.use_localtime = use_localtime

        if db_path is not None:
            self.__db_path = db_path

    def is_open(self) -> bool:
        """
        Return the state of connection

        :return:
        """

        return isinstance(self.__db_connection, sqlite3.Connection)

    @classmethod
    def creating_database(cls, db_path: str, verbose: bool = False, use_localtime: bool = True) -> Optional['DBManager']:
        """
        Create a new database in path

        :param use_localtime:
        :param verbose:
        :param db_path:
        :return:
        """

        try:

            with sqlite3.connect(db_path) as conn:       # with auto-close connection resource

                Logger.log_success(msg=f"database created in path: '{db_path}'", is_verbose=verbose)

            return cls(db_path=db_path, verbose=verbose, use_localtime=use_localtime)

        except Exception as e:
            Logger.log_warning(msg=f"error during database creation in path: '{db_path}'", is_verbose=verbose)

            return None

    def open_connection(self) -> None:
        """
        Open a new connection with DB

        :return:
        """

        self.__db_connection = None
        self.__db_cursor = None

        # open connection if and only if database already exists
        if Utils.exist(self.__db_path):
            Logger.log_info(msg=f"found database: '{self.__db_path}'", is_verbose=self.verbose)
        else:
            Logger.log_warning(msg=f"database '{self.__db_path}' not found", is_verbose=self.verbose)

            return None

        try:
            self.__db_connection = sqlite3.connect(self.__db_path)  # connect to db
            self.__db_connection.row_factory = dict_factory  # set row factory to get dict instead of tuple
            self.__db_cursor = self.__db_connection.cursor()  # set cursor as attr

            Logger.log_success(msg=f"Connection successful with db: '{self.__db_path}'", is_verbose=self.verbose)

            # add FK checks
            self.__db_connection.execute('PRAGMA foreign_keys = ON;')

        except Exception as exception:

            Logger.log_error(exception, is_verbose=self.verbose)

    def refresh_connection(self, **kwargs) -> None:
        """
        Refresh DB connection

        :return:
        """

        Logger.log_info(msg=f"database connection will be refreshing...", is_verbose=self.verbose)

        self.close_connection()

        self.set_connection_params(**kwargs)

        self.open_connection()

    def close_connection(self) -> None:
        """
        Close DB connection

        :return:
        """

        try:
            self.__db_connection.close()

            Logger.log_info(msg="database connection closed", is_verbose=self.verbose)

        except Exception as e:
            Logger.log_warning(msg="database connection can't be closed", is_verbose=self.verbose)

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
                Field.hex_color(name="avatar_hex_color", default="'#cfcfcf'", nullable=False),
                Field(name="phone", type="VARCHAR(30)", nullable=True),
                Field.nullable_datetime("last_visit_at", default=None),
                Field.fk_field(name="role_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="role_id", on_table=self.role_table_name, on_update="CASCADE", on_delete="RESTRICT")
            ]),

            self.role_table_name: Table(self.role_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field(name="permission_create", type="INTEGER", default='1'),
                Field(name="permission_read_all", type="INTEGER", default='0'),
                Field(name="permission_move_backward", type="INTEGER", default='1'),
                Field(name="permission_move_forward", type="INTEGER", default='1'),
                Field(name="permission_move", type="INTEGER", default='0'),
                Field(name="permission_edit_own", type="INTEGER", default='1'),
                Field(name="permission_edit_all", type="INTEGER", default='0'),
                Field(name="permission_change_role", type="INTEGER", default='0'),
                Field(name="permission_change_assignment", type="INTEGER", default='0'),
                Field(name="permission_delete_own", type="INTEGER", default='1'),
                Field(name="permission_delete_all", type="INTEGER", default='0'),
                Field(name="permission_manage_roles", type="INTEGER", default='0'),
                Field(name="permission_manage_task_status", type="INTEGER", default='0'),
                Field(name="permission_manage_task_labels", type="INTEGER", default='0'),
                Field(name="permission_manage_users", type="INTEGER", default='0'),
                Field(name="permission_edit_task_deadline", type="INTEGER", default='0'),
                Field(name="permission_remove_work", type="INTEGER", default='0'),
            ]),

            self.task_status_table_name: Table(self.task_status_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field.description_field(),
                Field.hex_color(name="hex_color", nullable=True),
                Field.fk_field(name="default_next_task_status_id", nullable=True),
                Field.fk_field(name="default_prev_task_status_id", nullable=True),
                Field(name="final", type="INTEGER", default='0'),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="default_next_task_status_id", on_table=self.task_status_table_name, on_update="CASCADE", on_delete="SET NULL"),
                FKConstraint.on_id(fk_field="default_prev_task_status_id", on_table=self.task_status_table_name, on_update="CASCADE", on_delete="SET NULL")
            ]),

            self.task_table_name: Table(self.task_table_name, [
                Field.id_field(),
                Field.name_field(unique=False),
                Field.description_field(),
                Field.nullable_datetime(name="deadline"),
                Field(name="priority", type="INTEGER", default="0"),
                Field.created_at_field(use_localtime=self.use_localtime),
                Field.updated_at_field(use_localtime=self.use_localtime),
                Field.fk_field(name="author_id", nullable=True),
                Field.fk_field(name="task_status_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="author_id", on_table=self.user_table_name, on_update="CASCADE", on_delete="SET NULL"),
                FKConstraint.on_id(fk_field="task_status_id", on_table=self.task_status_table_name, on_update="CASCADE", on_delete="RESTRICT"),
            ], with_triggers=Trigger(
                name=f"{self.task_table_name}_updater_trigger",
                on_action=f"Update On {self.task_table_name}",
                script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where id = new.id"
            )),

            self.task_label_table_name: Table(self.task_label_table_name, [
                Field.id_field(),
                Field.name_field(unique=True),
                Field.description_field(),
                Field.hex_color(name="hex_color", nullable=True)
            ]),

            self.task_assignment_table_name: Table.pivot(self.task_assignment_table_name, tables=[
                self.user_table_name,
                self.task_table_name
            ], other_fields=[
                Field.datetime_now("assigned_at", use_localtime=self.use_localtime),
                Field.nullable_datetime("last_watched_at", default=None),
            ], with_triggers=[
                Trigger(
                    name=f"{self.task_assignment_table_name}_on_insert_updater_trigger",
                    on_action=f"After Insert On {self.task_assignment_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = new.task_id"
                ),
                Trigger(
                    name=f"{self.task_assignment_table_name}_on_delete_updater_trigger",
                    on_action=f"After Delete On {self.task_assignment_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = old.task_id"
                ),
                Trigger(
                    name=f"{self.task_assignment_table_name}_on_delete_updater_trigger",
                    on_action=f"After Update On {self.task_assignment_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = new.task_id"
                ),
            ]),

            self.todo_item_table_name: Table(self.todo_item_table_name, [
                Field.id_field(),
                Field.description_field(nullable=False),
                Field.nullable_datetime(name="deadline"),
                Field.created_at_field(use_localtime=self.use_localtime),
                Field.updated_at_field(use_localtime=self.use_localtime),
                Field(name="done", type="INTEGER", default="0"),
                Field.fk_field(name="author_id", nullable=True),
                Field.fk_field(name="task_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="author_id", on_table=self.user_table_name, on_update="CASCADE", on_delete="SET NULL"),
                FKConstraint.on_id(fk_field="task_id", on_table=self.task_table_name, on_update="CASCADE", on_delete="CASCADE"),
            ], with_triggers=[
                Trigger(
                    name=f"{self.todo_item_table_name}_on_insert_updater_trigger",
                    on_action=f"After Insert On {self.todo_item_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = new.task_id"
                ),
                Trigger(
                    name=f"{self.todo_item_table_name}_on_delete_updater_trigger",
                    on_action=f"After Delete On {self.todo_item_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = old.task_id"
                ),
                Trigger(
                    name=f"{self.todo_item_table_name}_on_update_updater_trigger",
                    on_action=f"After Update On {self.todo_item_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = new.task_id"
                ),
            ]),

            self.task_task_label_pivot_table_name: Table.pivot(self.task_task_label_pivot_table_name, [
                self.task_table_name,
                self.task_label_table_name
            ], with_triggers=[
                Trigger(
                    name=f"{self.task_task_label_pivot_table_name}_on_insert_updater_trigger",
                    on_action=f"After Insert On {self.task_task_label_pivot_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = new.task_id"
                ),
                Trigger(
                    name=f"{self.task_task_label_pivot_table_name}_on_delete_updater_trigger",
                    on_action=f"After Delete On {self.task_task_label_pivot_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = old.task_id"
                ),
                Trigger(
                    name=f"{self.task_task_label_pivot_table_name}_on_update_updater_trigger",
                    on_action=f"After Update On {self.task_task_label_pivot_table_name}",
                    script=f"Update {self.task_table_name} Set {SqlUtils.UPDATED_AT_FIELD_NAME} = {SqlUtils.datetime_strf_now()} Where {self.task_table_name}.id = new.task_id"
                ),
            ])

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
                                                   ("Front-end", "Front-end tasks", "#32a852"),
                                                   ("Back-end", "Back-end tasks", "#f56342"),
                                                   ("Documentation", "Documentation tasks", "#f242f5")
                                               ], cols=("name", "description", "hex_color")),

            self.role_table_name: Seeder(table=self.role_table_name,
                                         values=[
                                           (self.project_manager_role_id, "Project Manager",  1, 1, 1, 1,     1, 1, 1, 1,     1, 1, 1, 1,     1, 1, 1, 1,   1),
                                           (2, "Supervisor",       1, 1, 1, 1,     1, 1, 0, 1,     1, 1, 1, 0,     1, 1, 0, 1,  0),
                                           (3, "Teammate",         1, 0, 1, 1,     1, 0, 0, 0,     1, 0, 1, 0,     0, 0, 0, 0,  0),
                                           (4, "Base",             1, 0, 0, 0,     1, 0, 0, 0,     1, 0, 0, 0,     0, 0, 0, 0,  0),
                                           (5, "External",         0, 0, 0, 0,     0, 0, 0, 0,     0, 0, 0, 0,     0, 0, 0, 0,  0),
                                         ], cols=("id", "name",
                                                  "permission_create", "permission_read_all", "permission_move_backward", "permission_move_forward",
                                                  "permission_edit_own", "permission_edit_all", "permission_change_role", "permission_change_assignment",
                                                  "permission_delete_own", "permission_delete_all", "permission_move", "permission_manage_roles",
                                                  "permission_manage_task_status", "permission_manage_task_labels", "permission_manage_users", "permission_edit_task_deadline",
                                                  "permission_remove_work"
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

            # Logger.log_info(f"inserted base data in {self.seeders[name].table}", is_verbose=self.verbose)         # too verbose

        except Exception as exception:

            Logger.log_error(msg=f"error occurs during run seeder: {name}", full=True, is_verbose=self.verbose)

    @property
    def db_path(self):
        return self.__db_path

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
                        Insert Into {self.task_status_table_name} (id, name, description, default_next_task_status_id, default_prev_task_status_id, hex_color, final)
                        Values
                        ({self.release_task_status_id}, "Release", "Task successful tested and released", NULL, NULL, "#3eed72", 1),
                        ({self.done_task_status_id}, "Done", "Task done", {self.release_task_status_id}, NULL, "#b4e34f", 1),
                        ({self.bug_fixing_task_status_id}, "Bug Fixing", "Task with bug to resolve", {self.testing_task_status_id}, NULL, "#e84157", 0),
                        ({self.testing_task_status_id}, "Testing", "Task done in testing", {self.done_task_status_id}, NULL, "#facdf3", 0),
                        ({self.doing_task_status_id}, "Doing", "Task work in progress", {self.testing_task_status_id}, NULL, "#ffbf7a", 0),
                        ({self.todo_task_status_id}, "To-Do", "Task that must be done", {self.doing_task_status_id}, NULL, "#73f5fa", 0),
                        ({self.backlog_task_status_id}, "Backlog", "Tasks to be performed at the end of the most priority tasks", {self.todo_task_status_id}, NULL, "#c9eeff", 0),
                        ({self.ideas_task_status_id}, "Ideas", "Tasks yet to be defined, simple ideas and hints for new features", {self.todo_task_status_id}, NULL, "#f5d442", 0);
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

            Logger.log_error(msg=f"error occurs during fill {self.task_status_table_name}", full=True, is_verbose=self.verbose)

    @property
    def task_task_label_pivot_table_name(self) -> str:
        return "task_task_label_pivot"

    def generate_base_db_structure(self, strict: bool = False) -> None:
        """
        Generate the base db of project

        :param strict: flag to interrupt application if there is an exception
        :type strict: bool

        :return: None
        :rtype None:
        """

        try:

            # drop all tables
            for table_name in self.tables.keys():
                self.drop_table(table_name)

            Logger.log_info("start to generate base database", is_verbose=self.verbose)

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

    def insert_from_dict(self, table_name: str, values: Dict | List[Dict], columns: List[str] | Tuple[str] | None = None) -> int:
        """
        Insert all dict values passed in a table

        :param table_name:
        :type table_name: str
        :param values: values to insert
        :type values: Dict | List[Dict]
        :param columns: fields to use
        :type columns: List[str] | Tuple[str] | None

        :return: id of inserted record
        :rtype int:
        """

        if type(values) is dict:  # convert single dict in a list
            d = values.copy()
            values = list()
            values.append(d)

        # remove items which doesn't have a key in used table header
        checked_values: List[Dict] = []
        for value in values:
            checked_values.append(DictUtils.filter_dict_by_key(dict(value), self.tables[table_name].header))

        values = checked_values

        # create query
        query = QueryBuilder.from_table(table_name).enable_binding().insert_from_dict(columns=columns, *values)

        self.cursor.execute(query.to_sql(), query.data_bound)   # execute insert query

        self.connection.commit()

        return self.cursor.lastrowid

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

        query_built = QueryBuilder.from_table(table_name).enable_binding().select(*columns).apply_conditions(*conditions)

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

        if isinstance(conditions, WhereCondition):      # cast to list to use it as iterable
            conditions = [conditions]

        # remove items which doesn't have a key in used table header
        data: Dict = DictUtils.filter_dict_by_key(dict(data), self.tables[table_name].header)

        query_built = QueryBuilder.from_table(table_name)\
                                  .enable_binding()\
                                  .update_from_dict(data)\
                                  .apply_conditions(*conditions)

        query: str = query_built.to_sql()
        data: List = query_built.data_bound

        res = self.cursor.execute(query, data)

        self.connection.commit()

        return res

    def execute(self, raw_query: str) -> Any:
        """
        Execute passed raw query

        :param raw_query: the raw query to execute
        :type raw_query: str
        :return: execution result
        """

        return self.cursor.executescript(raw_query)

    def drop_table(self, table_name: str) -> bool:
        """
        Drop table by name

        :param table_name:
        :return:
        """

        try:
            self.cursor.execute(f"Drop Table If Exists {table_name};")

            self.connection.commit()

            return True

        except Exception:
            return False
