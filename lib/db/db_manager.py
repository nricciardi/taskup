import sqlite3
from lib.utils.base import Base
import os


class DBManager:
    def __init__(self, db_name: str, work_directory_path: str = ".", verbose: bool = False):

        self.verbose = verbose
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
    def user_table_name(self):
        return "user"

    @property
    def role_table_name(self):
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

        self.cursor.execute(f"""
            Insert Into {self.role_table_name} (name, permission_create, permission_read_all,
             permission_move_backward, permission_move_forward, permission_edit)
            Values
            ("Project Manager", 1, 1, 1, 1, 1),
            ("Development", 1, 0, 1, 1, 0),
            ("Base", 0, 0, 0, 0, 0);
        """)

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
                
                Foreign Key (role_id) References role(id)
            );
        """)

    def fill_db(self) -> None:
        """
        Fill db with default values

        :return: None
        :rtype None:
        """

        self.__insert_base_roles()

    def generate_base_db_structure(self) -> None:
        """
        Generate the base db of project

        :return: None
        :rtype None:
        """

        try:

            if self.verbose:
                Base.log_info("start to generate base db")

            self.__create_role_table()
            self.__create_user_table()

            if self.verbose:
                Base.log_success("base db generated")

        except Exception as exception:

            Base.log_error(message="error occurs during generate db", full=True, is_verbose=self.verbose)

            raise exception

        # fill db
        try:

            if self.verbose:
                Base.log_info("start to fill db")

            self.fill_db()

            Base.log_success(message="base db filled", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_error(message="error occurs during fill db", full=True, is_verbose=self.verbose)

        self.connection.commit()
