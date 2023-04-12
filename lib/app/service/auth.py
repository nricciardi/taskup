from lib.db.entity.user import UserModel, UsersManager
from lib.db.component import WhereCondition
from lib.utils.collections import CollectionsUtils
from lib.utils.logger import Logger
from lib.file.file_manager import FileManger
from typing import List


class AuthService:
    __users_manager: UsersManager
    __me: UserModel | None = None

    EMAIL = "email"
    PASSWORD = "password"

    def __init__(self, users_manager: UsersManager, vault_path: str, verbose: bool = False):
        self.__users_manager = users_manager
        self.__vault_path = vault_path
        self.verbose = verbose

        self.try_autologin()

    def __del__(self):
        self.__me = None

    @property
    def vault_path(self) -> str:
        return self.__vault_path

    def me(self) -> UserModel | None:
        return self.__me

    def try_autologin(self) -> None:
        """
        Try the autologin using vault data

        :return:
        """

        try:
            Logger.log_info(msg="try autologin...", is_verbose=self.verbose)

            vault_data = self.get_vault_data()

            if self.EMAIL in vault_data and self.PASSWORD in vault_data:
                self.login(vault_data.get(self.EMAIL), vault_data.get(self.PASSWORD))
            else:
                raise AttributeError()

        except Exception:

            Logger.log_warning(msg="autologin failed", is_verbose=self.verbose)

            return None

    def is_logged(self) -> bool:
        return self.__me is not None

    def login(self, email: str, password: str, keep: bool = False) -> UserModel:
        """
        Login user by email and password

        :param keep: keep data on login
        :type keep: bool
        :param email:
        :type email: str
        :param password:
        :type password: str
        :return: logged user
        :rtype: UserModel
        """

        users_matched: List = self.__users_manager.where_as_model(
            WhereCondition("email", "=", email),
            WhereCondition("password", "=", password),
            with_relations=True
        )

        self.__me = CollectionsUtils.first(users_matched)

        if self.__me is None:
            msg: str = f"no match with {email} + {password}"

            Logger.log_error(msg=msg, is_verbose=self.verbose)

            raise ValueError(msg)

        Logger.log_success(msg="logged in correctly", is_verbose=self.verbose)

        if keep:
            self.store_in_vault(email, password)

        return self.__me

    def logout(self) -> bool:
        try:

            self.erase_vault_data()

            self.__me = None

            Logger.log_success(msg="logout correctly", is_verbose=self.verbose)

            return True

        except Exception as e:

            Logger.log_error(msg=e, is_verbose=self.verbose)

            return False

    def store_in_vault(self, email: str, password: str) -> None:
        """
        Store in vault email and password

        :param email:
        :type email: str
        :param password:
        :type password: str

        :return:
        :rtype None:
        """

        FileManger.write_json(self.vault_path, {
            self.EMAIL: email,
            self.PASSWORD: password
        })

        Logger.log_success(msg=f"email: ({email}) and password ({'*' * len(password)}) are stored successful in vault",
                           is_verbose=self.verbose)

    def get_vault_data(self) -> dict | None:
        """
        Get data in vault

        :return: data
        :rtype dict:
        """

        return FileManger.read_json(self.vault_path)

    def erase_vault_data(self) -> bool:

        try:
            FileManger.write_json(self.vault_path, "")

            return True
        except Exception:
            Logger.log_warning(msg="vault erase error", is_verbose=self.verbose)

            return False
