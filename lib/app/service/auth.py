from lib.db.entity.user import UserModel, UsersManager
from lib.db.component import WhereCondition


class Auth:

    __users_manager: UsersManager

    def __init__(self, users_manager: UsersManager):
        self.__users_manager = users_manager

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

        self.__users_manager.where(
            WhereCondition("email", "=", email),
            WhereCondition("password", "=", password),
        )


