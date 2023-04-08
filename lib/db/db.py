import sqlite3
from lib.utils.base import Base
import os
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Field:
    name: str
    type: str
    default: str | None = field(default=None)
    pk: bool = field(default=False)
    autoincrement: bool = field(default=False)
    unique: bool = field(default=False)
    nullable: bool = field(default=False)
    check: str | None = field(default=None)

    @classmethod
    def id_field(cls) -> 'Field':
        return cls(name="id", type="INTEGER", pk=True, autoincrement=True)

    @classmethod
    def fk_field(cls, name: str, nullable: bool = False, unique: bool = False) -> 'Field':
        return cls(name=name, type="INTEGER", nullable=nullable, unique=unique)

    @classmethod
    def name_field(cls, unique: bool = True) -> 'Field':
        return cls(name="name", type="VARCHAR(150)", nullable=False, unique=unique)

    @classmethod
    def description_field(cls, nullable: bool = False) -> 'Field':
        return cls(name="description", type="VARCHAR(1000)", nullable=nullable, unique=False)

    @classmethod
    def created_at_field(cls) -> 'Field':
        return cls(name="created_at", type="DATETIME", default="strftime('%Y-%m-%d %H:%M:%S', 'now')")

    @classmethod
    def updated_at_field(cls) -> 'Field':
        return cls(name="updated_at", type="DATETIME", default="strftime('%Y-%m-%d %H:%M:%S', 'now')")

    @classmethod
    def nullable_date_with_now_check_field(cls, name: str, default: str | None = 'NULL') -> 'Field':
        return cls(name=name, type="DATE", default=default, check=f"{name} IS NULL OR {Field.get_date_sql(name)} > {Field.get_date_sql('now', strict_string=True)}")

    @staticmethod
    def get_datetime_sql(datetime: str, strict_string: bool = False, use_localtime: bool = False) -> str:
        return f"""strftime('%Y-%m-%d %H:%M:%S', {"'" if strict_string else ""}{datetime}{", 'localtime'" if use_localtime else ""}{"'" if strict_string else ""})"""

    @staticmethod
    def get_date_sql(date: str, strict_string: bool = False, use_localtime: bool = False) -> str:
        return f"""strftime('%Y-%m-%d', {"'" if strict_string else ""}{date}{", 'localtime'" if use_localtime else ""}{"'" if strict_string else ""})"""

    def to_sql(self) -> str:
        """
        Get sql string for table

        :return: SQL
        :rtype str:
        """

        return f"{self.name} {self.type} {'DEFAULT (' + self.default + ')' if self.default is not None else ''} " + \
            f"{'UNIQUE' if self.unique else ''} {'PRIMARY KEY' if self.pk else ''} {'AUTOINCREMENT' if self.autoincrement else ''} " + \
            f"{'NULL' if self.nullable and not self.pk else 'NOT NULL'}"


@dataclass
class FKConstraint:
    fk_field: str
    on_table: str
    reference_field: str

    @classmethod
    def on_id(cls, fk_field: str, on_table: str) -> 'FKConstraint':
        return cls(fk_field=fk_field, on_table=on_table, reference_field='id')

    def to_sql(self) -> str:
        """
        Get sql strin for FK constraint

        :return: SQL
        :rtype str:
        """

        return f"Foreign Key ({self.fk_field}) References {self.on_table}({self.reference_field})"

@dataclass
class Table:
    name: str
    fields: List[Field]
    fk_constraints: List[FKConstraint] = field(default=None)

    def has_fk_constraint(self) -> bool:

        return self.fk_constraints is not None and len(self.fk_constraints) > 0

    @classmethod
    def pivot(cls, name: str, tables: List[str]) -> 'Table':

        fields = [
            Field.id_field()
        ]

        fk_constraints = []

        for t in tables:
            name = f"{t}_id"

            fields.append(Field.fk_field(name=name))
            fk_constraints.append(FKConstraint.on_id(name, t))

        return cls(name, fields, fk_constraints)

    def to_sql(self, if_not_exist: bool = True) -> str:
        """
        Get sql string to create table

        :return: SQL
        :rtype str:
        """

        fields = ',\n'.join(f.to_sql() for f in self.fields)

        return f"""Create Table {'If Not Exists' if if_not_exist else ''} {self.name} (
            {fields}
            
            {"," + ','.join(fk.to_sql() for fk in self.fk_constraints) if self.has_fk_constraint() else "" if self.has_fk_constraint() else ""}
        );
        """

@dataclass
class Seeder:
    table: str
    values: List[Tuple | Dict]
    fields: List | None = None

@dataclass
class DBStructure:
    name: str
    tables: List[Table]
    use_localtime: bool = False


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
                Field(name="email", type="VARCHAR(256)", unique=True),
                Field(name="password", type="VARCHAR(256)", unique=True),
                Field.fk_field(name="role_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="role_id", on_table=self.role_table_name)
            ]),

            self.role_table_name: Table(self.role_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field(name="permission_create", type="INTEGER"),
                Field(name="permission_read_all", type="INTEGER"),
                Field(name="permission_move_backward", type="INTEGER"),
                Field(name="permission_move_forward", type="INTEGER"),
                Field(name="permission_edit", type="INTEGER"),
                Field(name="permission_change_role", type="INTEGER"),
                Field(name="permission_change_assignment", type="INTEGER"),
            ]),

            self.task_status_table_name: Table(self.task_status_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field.description_field(),
                Field.fk_field(name="default_next_task_status_id", nullable=True)
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="default_next_task_status_id", on_table=self.task_status_table_name)
            ]),

            self.task_table_name: Table(self.task_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field.description_field(),
                Field.nullable_date_with_now_check_field(name="deadline"),
                Field(name="priority", type="INTEGER", default="0"),
                Field.created_at_field(),
                Field.updated_at_field(),
                Field.fk_field(name="author_id"),
                Field.fk_field(name="task_status_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="author_id", on_table=self.user_table_name),
                FKConstraint.on_id(fk_field="task_status_id", on_table=self.task_status_table_name),
            ]),

            self.task_label_table_name: Table(self.task_label_table_name, [
                Field.id_field(),
                Field.name_field(),
                Field.description_field(),
                Field(name="rgb_color", type="TEXT(6)")
            ]),

            self.task_assignment_table_name: Table.pivot(self.task_assignment_table_name, tables=[
                self.user_table_name,
                self.task_table_name
            ]),

            self.todo_item_table_name: Table(self.todo_item_table_name, [
                Field.id_field(),
                Field.description_field(nullable=False),
                Field.nullable_date_with_now_check_field(name="deadline"),
                Field.created_at_field(),
                Field.updated_at_field(),
                Field(name="done", type="INTEGER", default="0"),
                Field.fk_field(name="author_id"),
                Field.fk_field(name="task_id"),
            ], fk_constraints=[
                FKConstraint.on_id(fk_field="author_id", on_table=self.user_table_name),
                FKConstraint.on_id(fk_field="task_id", on_table=self.task_table_name),
            ]),

            self.task_task_label_pivot_table_name: Table.pivot(self.task_task_label_pivot_table_name, [
                self.task_table_name,
                self.task_label_table_name
            ])


        }

    @property
    def seeders(self) -> Dict[str, Seeder]:
        """
        Return the dict of seeders

        :return: seeders
        :rtype dict:
        """

        return {}

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

    def create_table(self, table_name: str, if_not_exists: bool = True) -> None:
        """
        Create table

        :param if_not_exists:
        :type if_not_exists: bool
        :type table_name: str
        :param table_name:
        :return:
        """

        query: str = self.tables[table_name].to_sql()

        self.cursor.execute(query)

        Base.log_info(f"created if not exists {table_name}", is_verbose=self.verbose)

        self.connection.commit()


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

    @property
    def task_status_table_name(self) -> str:
        return "task_status"

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


    @property
    def task_assignment_table_name(self) -> str:
        return "task_assignment"

    @property
    def todo_item_table_name(self) -> str:
        return "todo_item"


    @property
    def task_label_table_name(self) -> str:
        return "task_label"

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

            self.create_table(self.role_table_name)

            self.__insert_base_roles()

            self.create_table(self.user_table_name)

            self.create_table(self.task_status_table_name)

            self.__insert_base_task_status()

            self.create_table(self.task_status_table_name)

            self.create_table(self.task_assignment_table_name)

            self.create_table(self.todo_item_table_name)

            self.create_table(self.task_label_table_name)

            self.__insert_base_task_labels()

            self.create_table(self.task_task_label_pivot_table_name)

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
