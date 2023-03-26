import sqlite3
from lib.utils.base import Base
import os


class DBManager:
    def __init__(self, db_name: str, work_directory_path: str = ".", verbose: bool = False, use_localtime: bool = False):

        self.verbose = verbose
        self.use_localtime = use_localtime

        self.__db_name: str = db_name
        self.__work_directory_path: str = work_directory_path
        self.__db_path = os.path.join(self.__work_directory_path, self.__db_name)

        db_exists = os.path.exists(self.__db_path)      # if False => database structure must be created

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
            try:

                self.generate_base_db_structure()

            except Exception as exception:
                Base.log_error(message=exception, is_verbose=self.verbose)

                Base.exit()

    def __del__(self):
        self.__db_connection.close()

    def __append_localtime(self) -> str:
        append_localtime = ""
        if self.use_localtime:
            append_localtime = ", 'localtime'"

        return append_localtime

    def __datetime(self, datetime: str) -> str:
        return f"(strftime('%Y-%m-%d %H:%M:%S', {datetime}{self.__append_localtime()}))"

    def __date(self, date: str) -> str:
        return f"(strftime('%Y-%m-%d', {date}{self.__append_localtime()}))"

    def __timestamp(self) -> str:
        return f"""
        created_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', {self.__datetime('now')})),
        updated_at DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%S', {self.__datetime('now')})),
        """

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

        self.cursor.execute(f"""
            Create Table if not exists {self.role_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                permission_create INTEGER NOT NULL,
                permission_read_all INTEGER NOT NULL,
                permission_move_backward INTEGER NOT NULL,
                permission_move_forward INTEGER NOT NULL,
                permission_edit INTEGER NOT NULL
            );
        """)

    def __insert_base_roles(self) -> None:
        """
        Insert into db base roles

        :return: None
        :rtype None:
        """

        try:

            Base.log_info(f"start to fill {self.role_table_name}", is_verbose=self.verbose)

            self.cursor.execute(f"""
                        Insert Into {self.role_table_name} (name, permission_create, permission_read_all,
                         permission_move_backward, permission_move_forward, permission_edit)
                        Values
                        ("Project Manager", 1, 1, 1, 1, 1),
                        ("Development", 1, 0, 1, 1, 0),
                        ("Base", 0, 0, 0, 0, 0);
                    """)

            Base.log_info(message=f"{self.role_table_name} filled", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(message=f"error occurs during fill {self.role_table_name}", full=True,
                           is_verbose=self.verbose)

    def __create_user_table(self) -> None:
        """
        Create user table if not exists

        :return: None
        :rtype None:
        """

        self.cursor.execute(f"""
            Create Table if not exists {self.user_table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(100) NOT NULL UNIQUE,
                email VARCHAR(256) NOT NULL UNIQUE,
                password VARCHAR(256),
                
                role_id INTEGER NOT NULL,
                
                Foreign Key (role_id) References {self.role_table_name}(id)
            );
        """)

    @property
    def task_status_table_name(self) -> str:
        return "task_status"

    def __create_task_status_table(self) -> None:
        """
        Create task table if not exists

        :return: None
        :rtype None:
        """

        self.cursor.execute(f"""
             Create Table if not exists {self.task_status_table_name} (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name VARCHAR(150) NOT NULL UNIQUE,
                 description VARCHAR(1000) NULL,
                 
                 default_next_task_status_id INTEGER NULL,
                 
                 Foreign Key (default_next_task_status_id) References {self.task_status_table_name}(id)
             );
         """)

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
            self.cursor.execute(f"""
                        Insert Into {self.task_status_table_name} (id, name, description, default_next_task_status_id)
                        Values
                        ({self.release_task_status_id}, "Release", "Task successful tested and released", NULL),
                        ({self.bug_fixing_task_status_id}, "Bug Fixing", "Task with bug to resolve", {self.testing_task_status_id}),
                        ({self.testing_task_status_id}, "Testing", "Task done in testing", {self.release_task_status_id}),
                        ({self.doing_task_status_id}, "Doing", "Task work in progress", {self.testing_task_status_id}),
                        ({self.todo_task_status_id}, "To-Do", "Task that must be done", {self.doing_task_status_id}),
                        ({self.backlog_task_status_id}, "Backlog", "Tasks to be performed at the end of the most priority tasks", {self.todo_task_status_id}),
                        ({self.ideas_task_status_id}, "Ideas", "Tasks yet to be defined, simple ideas and hints for new features", {self.todo_task_status_id});
                    """)

            Base.log_info(message=f"{self.task_status_table_name} filled", is_verbose=self.verbose)

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


        self.cursor.execute(f"""
             Create Table if not exists {self.task_table_name} (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name VARCHAR(150) NOT NULL,
                 description VARCHAR(1000) NOT NULL,
                 deadline DATE NULL CHECK (deadline IS NULL OR date(deadline) > date('now'{self.__append_localtime()})),
                 priority INTEGER NOT NULL DEFAULT 0,
                 {self.__timestamp()}

                 author_id INTEGER NOT NULL,
                 task_status_id INTEGER NOT NULL DEFAULT {self.todo_task_status_id},

                 Foreign Key(author_id) References {self.user_table_name}(id),
                 Foreign Key(task_status_id) References {self.task_status_table_name}(id)
             );
         """)

    def generate_base_db_structure(self) -> None:
        """
        Generate the base db of project

        :return: None
        :rtype None:
        """

        try:

            Base.log_info("start to generate base db", is_verbose=self.verbose)

            self.__create_role_table()
            Base.log_info(f"created if not exists {self.role_table_name}", is_verbose=self.verbose)

            self.__insert_base_roles()
            Base.log_info(f"inserted base data in {self.role_table_name}", is_verbose=self.verbose)

            self.__create_user_table()
            Base.log_info(f"created if not exists {self.user_table_name}", is_verbose=self.verbose)

            self.__create_task_status_table()
            Base.log_info(f"created if not exists {self.task_status_table_name}", is_verbose=self.verbose)

            self.__insert_base_task_status()
            Base.log_info(f"inserted base data in {self.task_status_table_name}", is_verbose=self.verbose)

            # self.__create_task_table()
            Base.log_info(f"created if not exists {self.task_table_name}", is_verbose=self.verbose)

            self.connection.commit()

            Base.log_success("base db generated", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(message="error occurs during generate db", full=True, is_verbose=self.verbose)

            raise exception
