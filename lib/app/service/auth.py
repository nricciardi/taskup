from lib.db.entity.user import UserModel, UsersManager
from lib.db.component import WhereCondition
from lib.utils.collections import CollectionsUtils
from lib.utils.logger import Logger
from lib.file.file_manager import FileManger


class Auth:

    __users_manager: UsersManager

    def __init__(self, users_manager: UsersManager, vault_path: str,  verbose: bool = False):
        self.__users_manager = users_manager
        self.__vault_path = vault_path
        self.verbose = verbose


    @property
    def vault_path(self) -> str:
        return self.__vault_path

    def login(self, email: str, password: str) -> UserModel:
        """
        Login user by email and password

        :param email:
        :type email: str
        :param password:
        :type password: str
        :return: logged user
        :rtype: UserModel
        """

        users_matched = self.__users_manager.where_as_model(
            WhereCondition("email", "=", email),
            WhereCondition("password", "=", password),
        )

        user = CollectionsUtils.first(users_matched)

        if user is None:
            msg: str = f"no match with {email} + {password}"

            Logger.log_error(msg=msg, is_verbose=self.verbose)

            raise ValueError(msg)

        return user

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
            "email": email,
            "password": password
        })
