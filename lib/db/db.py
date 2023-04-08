import sqlite3
from lib.utils.base import Base
import os
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class Field:
    name: str
    type: str
    default: Any | None = None
    pk: bool = False
    autoincrement: bool = False
    unique: bool = False
    nullable: bool = False

    def to_sql(self) -> str:
        """
        Get sql string for table

        :return: SQL
        :rtype str:
        """

        return f"{self.name} {self.type} {'DEFAULT (' + self.default + ')' if self.default is not None else ''}" + \
            f"{'UNIQUE' if self.unique else ''} {'PRIMARY KEY' if self.pk else ''} {'AUTOINCREMENT' if self.autoincrement else ''}" + \
            f"{'NULL' if self.nullable else 'NOT NULL'}"


@dataclass
class Table:
    name: str
    fields: List[Field]

    def to_sql(self, if_not_exist: bool = True) -> str:
        """
        Get sql string to create table

        :return: SQL
        :rtype str:
        """

        return f"""Create Table {'If Not Exists' if if_not_exist else ''} {self.name} (
            {','.join(field.to_sql() for field in self.fields)}
        );
        """


class DBManager:
    def __init__(self, db_name: str, work_directory_path: str = ".", verbose: bool = False,
                 use_localtime: bool = False):
        """
        Create a DBManager

        :param db_name: db name
        :param work_directory_path: work directory path
        :param verbose: verbose
        :param use_localtime: if db must use local in date
        """

        self.verbose = verbose
        self.use_localtime = use_localtime

        self.__db_name: str = db_name
        self.__work_directory_path: str = work_directory_path
        self.__db_path = os.path.join(self.__work_directory_path, self.__db_name)

        db_exists = os.path.exists(self.__db_path)  # if False => database structure must be created

        if db_exists:
            Base.log_info(msg=f"database {self.__db_path} found", is_verbose=self.verbose)
        else:
            Base.log_warning(msg=f"database {self.__db_path} not found, will be generate...", is_verbose=verbose)

        try:
            self.__db_connection = sqlite3.connect(self.__db_path)
            self.__db_cursor = self.__db_connection.cursor()

            Base.log_success(msg=f"Connection successful with db: {self.__db_path}", is_verbose=verbose)

            if not db_exists:
                self.generate_base_db_structure(strict=True)

        except Exception as exception:
            print("Connection with database failed...")

            Base.log_error(exception, is_verbose=self.verbose)

            Base.exit()

    def __del__(self):
        self.__db_connection.close()

    def __append_localtime(self) -> str:
        append_localtime = ""
        if self.use_localtime:
            append_localtime = ", 'localtime'"

        return append_localtime

    def __datetime(self, datetime: str, strict_string: bool = False) -> str:
        return f"""strftime('%Y-%m-%d %H:%M:%S', {"'" if strict_string else ""}{datetime}{self.__append_localtime()}{"'" if strict_string else ""})"""

    def __date(self, date: str, strict_string: bool = False) -> str:
        return f"""strftime('%Y-%m-%d', {"'" if strict_string else ""}{date}{self.__append_localtime()}{"'" if strict_string else ""})"""

    def __timestamp(self) -> str:
        return f"""created_at DATETIME DEFAULT ({self.__datetime('now', strict_string=True)}),
                   updated_at DATETIME DEFAULT ({self.__datetime('now', strict_string=True)}),"""

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

    @property
    def user_table_name(self) -> str:
        return "user"

    @property
    def role_table_name(self) -> str:
        return "role"

    def __create_role_table(self) -> None:
        """
        Create role table if not exists

        :return: None
        :rtype None:
        """

        query = f"""
            Create Table if not exists {self.role_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                permission_create INTEGER NOT NULL,
                permission_read_all INTEGER NOT NULL,
                permission_move_backward INTEGER NOT NULL,
                permission_move_forward INTEGER NOT NULL,
                permission_edit INTEGER NOT NULL,
                permission_change_role INTEGER NOT NULL,
                permission_change_assignment INTEGER NOT NULL
            );
        """

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {self.role_table_name}", is_verbose=self.verbose)

    def __insert_base_roles(self) -> None:
        """
        Insert into db base roles

        :return: None
        :rtype None:
        """

        try:

            Base.log_info(f"start to fill {self.role_table_name}", is_verbose=self.verbose)

            query = f"""
                        Insert Into {self.role_table_name} (name, permission_create, permission_read_all,
                         permission_move_backward, permission_move_forward, permission_edit, permission_change_role,
                         permission_change_assignment)
                        Values
                        ("Project Manager", 1, 1, 1, 1, 1, 1, 1),
                        ("Supervisor", 1, 1, 1, 1, 1, 0, 1),
                        ("Teammate", 1, 0, 1, 1, 0, 0, 0),
                        ("Base", 0, 0, 0, 0, 0, 0, 0);
                    """

            self.cursor.execute(query)

            Base.log_info(f"inserted base data in {self.role_table_name}", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(msg=f"error occurs during fill {self.role_table_name}", full=True,
                           is_verbose=self.verbose)

    def __create_user_table(self) -> None:
        """
        Create user table if not exists

        :return: None
        :rtype None:
        """

        query = f"""
            Create Table if not exists {self.user_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(256) NOT NULL UNIQUE,
                password VARCHAR(256),
                
                role_id INTEGER NOT NULL,
                
                Foreign Key (role_id) References {self.role_table_name}(id)
            );
        """

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {self.user_table_name}", is_verbose=self.verbose)

    @property
    def task_status_table_name(self) -> str:
        return "task_status"

    def __create_task_status_table(self) -> None:
        """
        Create task table if not exists

        :return: None
        :rtype None:
        """

        query = f"""
             Create Table if not exists {self.task_status_table_name} (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name VARCHAR(150) NOT NULL UNIQUE,
                 description VARCHAR(1000) NULL,
                 
                 default_next_task_status_id INTEGER NULL,
                 
                 Foreign Key (default_next_task_status_id) References {self.task_status_table_name}(id)
             );
         """

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {self.task_status_table_name}", is_verbose=self.verbose)

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

    def __insert_base_task_status(self) -> None:
        """
        Insert into db base task status

        :return: None
        :rtype None:
        """

        try:

            Base.log_info(f"start to fill {self.task_status_table_name}", is_verbose=self.verbose)

            # insert default task status
            query = f"""
                        Insert Into {self.task_status_table_name} (id, name, description, default_next_task_status_id)
                        Values
                        ({self.release_task_status_id}, "Release", "Task successful tested and released", NULL),
                        ({self.bug_fixing_task_status_id}, "Bug Fixing", "Task with bug to resolve", {self.testing_task_status_id}),
                        ({self.testing_task_status_id}, "Testing", "Task done in testing", {self.release_task_status_id}),
                        ({self.doing_task_status_id}, "Doing", "Task work in progress", {self.testing_task_status_id}),
                        ({self.todo_task_status_id}, "To-Do", "Task that must be done", {self.doing_task_status_id}),
                        ({self.backlog_task_status_id}, "Backlog", "Tasks to be performed at the end of the most priority tasks", {self.todo_task_status_id}),
                        ({self.ideas_task_status_id}, "Ideas", "Tasks yet to be defined, simple ideas and hints for new features", {self.todo_task_status_id});
                    """

            self.cursor.execute(query)

            Base.log_info(f"inserted base data in {self.task_status_table_name}", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(msg=f"error occurs during fill {self.task_status_table_name}", full=True,
                           is_verbose=self.verbose)

    @property
    def task_table_name(self) -> str:
        return "task"

    def __create_task_table(self) -> None:
        """
        Create task table if not exists

        :return: None
        :rtype None:
        """

        query = f"""
             Create Table if not exists {self.task_table_name} (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name VARCHAR(150) NOT NULL,
                 description VARCHAR(1000) NOT NULL,
                 deadline DATE NULL DEFAULT NULL CHECK (deadline IS NULL OR {self.__date('deadline')} > {self.__date('now',
                                                                                                                     strict_string=True)}),
                 priority INTEGER NOT NULL DEFAULT 0,
                 {self.__timestamp()}

                 author_id INTEGER NOT NULL,
                 task_status_id INTEGER NOT NULL,

                 Foreign Key(author_id) References {self.user_table_name}(id),
                 Foreign Key(task_status_id) References {self.task_status_table_name}(id)
             );
         """

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {self.task_table_name}", is_verbose=self.verbose)

    @property
    def task_assignment_table_name(self) -> str:
        return "task_assignment"

    def __create_task_assignment_table(self) -> None:
        """
        Create task assignment table if not exists

        :return: None
        :rtype None:
        """

        query = f"""
                 Create Table if not exists {self.task_assignment_table_name} (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER NOT NULL,
                     task_id INTEGER NOT NULL,

                     Foreign Key(user_id) References {self.user_table_name}(id)
                     Foreign Key(task_id) References {self.task_table_name}(id)
                 );
             """

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {self.task_assignment_table_name}", is_verbose=self.verbose)

    @property
    def todo_item_table_name(self) -> str:
        return "todo_item"

    def __create_todo_item_table(self) -> None:
        """
        Create todoitem table if not exists

        :return: None
        :rtype None:
        """

        query = f"""
             Create Table if not exists {self.todo_item_table_name} (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 description VARCHAR(1000) NOT NULL,
                 deadline DATE NULL DEFAULT NULL CHECK (deadline IS NULL OR {self.__date('deadline')} > {self.__date('now', strict_string=True)}),
                 priority INTEGER NOT NULL DEFAULT 0,
                 {self.__timestamp()}
                 done INTEGER NOT NULL DEFAULT 0,

                 author_id INTEGER NOT NULL,
                 task_id INTEGER NOT NULL,

                 Foreign Key(author_id) References {self.user_table_name}(id),
                 Foreign Key(task_id) References {self.task_table_name}(id)
             );
         """

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {self.todo_item_table_name}", is_verbose=self.verbose)

    @property
    def task_label_table_name(self) -> str:
        return "task_label"

    def __create_task_label_table(self) -> None:
        """
        Create task label table if not exists

        :return: None
        :rtype None:
        """

        query = f"""
             Create Table if not exists {self.task_label_table_name} (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name VARCHAR(500) NOT NULL,
                 description VARCHAR(1000) NULL,
                 rgb_color TEXT(6) NOT NULL
             );
         """

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {self.task_label_table_name}", is_verbose=self.verbose)

    def __insert_base_task_labels(self) -> None:
        """
        Insert base task labels in DB

        :return:
        :rtype None:
        """

        try:

            Base.log_info(f"start to fill {self.task_label_table_name}", is_verbose=self.verbose)

            # insert default task status
            query = f"""
                        Insert Into {self.task_label_table_name} (name, description, rgb_color)
                        Values
                        ("Front-end", "Front-end tasks", "b6f542"),
                        ("Back-end", "Front-end tasks", "f56342"),
                        ("Documentation", "Documentation tasks", "f242f5");
                    """

            self.cursor.execute(query)

            Base.log_info(f"inserted base data in {self.task_status_table_name}", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(msg=f"error occurs during fill {self.task_status_table_name}", full=True,
                           is_verbose=self.verbose)

    @property
    def task_task_label_pivot_table_name(self) -> str:
        return "task_task_label_pivot"

    def __create_task_task_label_pivot_table(self) -> None:
        """
        Create task_task_label pivot table if not exists

        :return: None
        :rtype None:
        """

        query = f"""
                 Create Table if not exists {self.task_task_label_pivot_table_name} (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     task_id INTEGER NOT NULL,
                     task_label_id INTEGER NOT NULL,
                     
                     Foreign Key(task_id) References {self.task_table_name}(id)
                     Foreign Key(task_label_id) References {self.task_label_table_name}(id)
                 );
             """

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {self.task_task_label_pivot_table_name}", is_verbose=self.verbose)

    def generate_base_db_structure(self, strict: bool = False) -> None:
        """
        Generate the base db of app

        :param strict: flag to interrupt application if there is an exception
        :type strict: bool

        :return: None
        :rtype None:
        """

        try:

            Base.log_info("start to generate base db", is_verbose=self.verbose)

            self.__create_role_table()

            self.__insert_base_roles()

            self.__create_user_table()

            self.__create_task_status_table()

            self.__insert_base_task_status()

            self.__create_task_table()

            self.__create_task_assignment_table()

            self.__create_todo_item_table()

            self.__create_task_label_table()

            self.__insert_base_task_labels()

            self.__create_task_task_label_pivot_table()

            self.connection.commit()

            Base.log_success("base db structure generated", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(msg="error occurs during generate db", full=True, is_verbose=self.verbose)

            if strict:
                Base.exit()

            raise exception

    def insert_from_tuple(self, table_name: str, values: Tuple | List[Tuple], fields: List[str] | Tuple[str] | None = None) -> int:
        """
        Insert all tuple values passed in a table

        :param table_name:
        :type table_name: str
        :param values: values to insert
        :type values: Tuple | List[Tuple]
        :param fields: fields to use
        :type fields: List[str] | Tuple[str] | None

        :return: row inserted
        :rtype int:
        """

        if type(values) is not tuple:  # convert single tuple in a list
            t = values.copy()
            values = list()
            values.append(t)

        fields: str = "" if fields is None else "(" + ", ".join(fields) + ")"  # => "" or  "(field1, field2, ...)"
        placeholders: str = ','.join(['?'] * len(values))

        query: str = f"""Insert into {table_name}{fields}
                    Values ({placeholders})"""

        self.cursor.executemany(query, values)

        self.connection.commit()

        return self.cursor.rowcount

    def insert_from_dict(self, table_name: str, values: Dict | List[Dict], fields: List[str] | Tuple[str] | None = None) -> int:
        """
        Insert all dict values passed in a table

        :param table_name:
        :type table_name: str
        :param values: values to insert
        :type values: Dict | List[Dict]
        :param fields: fields to use
        :type fields: List[str] | Tuple[str] | None

        :return: row inserted
        :rtype int:
        """

        if not type(values) is dict:  # convert single dict in a list
            d = values.copy()
            values = list()
            values.append(d)

        row_count: int = 0
        for value in values:
            if fields is not None:  # get set of fields intersection between fields params and fields in dict
                fields_set: set = set(fields).intersection(set(value.keys()))
                fields_list = list(fields_set)

            else:
                fields_list = list(value.keys())

            fields: str = ", ".join(fields_list)

            placeholders: str = ','.join(['?'] * len(value.values()))

            query = f"""Insert into {table_name}{fields}
                        Values ({placeholders})"""

            actual_values: list = []

            for field in fields_list:
                actual_values.append(value[field])

            self.cursor.execute(query, tuple(actual_values))

            self.connection.commit()

            row_count += self.cursor.rowcount

        return row_count

    def create_table(self, if_not_exist: bool = True):
        raise NotImplementedError