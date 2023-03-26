import sqlite3
from lib.utils.base import Base
import os


class DBManager:
    def __init__(self, db_name: str, work_directory_path: str = ".", verbose: bool = False,
                 use_localtime: bool = False):

        self.verbose = verbose
        self.use_localtime = use_localtime

        self.__db_name: str = db_name
        self.__work_directory_path: str = work_directory_path
        self.__db_path = os.path.join(self.__work_directory_path, self.__db_name)

        db_exists = os.path.exists(self.__db_path)  # if False => database structure must be created

        Base.log_info(message=f"database {self.db_path} found", is_verbose=self.verbose)

        try:
            self.__db_connection = sqlite3.connect(self.__db_path)
            self.__db_cursor = self.__db_connection.cursor()

        except Exception as exception:
            print("Connection with database failed...")

            Base.log_error(exception, is_verbose=self.verbose)

            Base.exit()

        # generate db
        if not db_exists:
            self.generate_base_db_structure(strict=True)

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
                permission_edit INTEGER NOT NULL
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
                         permission_move_backward, permission_move_forward, permission_edit)
                        Values
                        ("Project Manager", 1, 1, 1, 1, 1),
                        ("Development", 1, 0, 1, 1, 0),
                        ("Base", 0, 0, 0, 0, 0);
                    """

            self.cursor.execute(query)

            Base.log_info(f"inserted base data in {self.role_table_name}", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(message=f"error occurs during fill {self.role_table_name}", full=True,
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

            Base.log_error(message=f"error occurs during fill {self.task_status_table_name}", full=True,
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
                 deadline DATE NULL CHECK (deadline IS NULL OR {self.__date('deadline')} > {self.__date('now',
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
                 deadline DATE NULL CHECK (deadline IS NULL OR {self.__date('deadline')} > {self.__date('now',
                                                                                                        strict_string=True)}),
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

    def generate_base_db_structure(self, strict: bool = False) -> None:
        """
        Generate the base db of project

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

            self.__create_todo_item_table()

            self.__create_task_label_table()

            self.connection.commit()

            Base.log_success("base db generated", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(message="error occurs during generate db", full=True, is_verbose=self.verbose)

            if strict:
                Base.exit()

            raise exception
