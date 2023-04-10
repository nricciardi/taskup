from lib.db.entity.user import UserModel


class Auth:

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

