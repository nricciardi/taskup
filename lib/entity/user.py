from lib.db.entity_manager import EntityManager
from dataclasses import dataclass
from lib.settings.settings_manager import SettingsManager
from lib.entity.bem import BaseEntityModel
from lib.utils.base import Base


@dataclass
class UserModel(BaseEntityModel):
    id: int
    username: str
    email: str
    password: str
    role_id: int


class UsersManager(EntityManager):
    __table_name = "user"
    __settings_manager = SettingsManager()

    db_use_localtime = False

    def __init__(self):
        verbose = self.__settings_manager.get(self.__settings_manager.VERBOSE_KEY)
        db_name = self.__settings_manager.get(self.__settings_manager.DB_NAME_KEY)
        work_directory_path = self.__settings_manager.work_directory_path()

        super().__init__(db_name=db_name, table_name=self.__table_name, verbose=verbose,
                         work_directory_path=work_directory_path)

    def find(self, user_id: int) -> UserModel:
        """
        Find the user with specified id

        :param user_id: user id
        :type user_id: int

        :return: UserModel
        :rtype UserModel:
        """

        data = super().find(user_id)

        return UserModel.from_tuple(data)

    def create(self, data: dict) -> UserModel:
        """
        Create a user from data

        :param data: user data
        :type data: dict

        :return: UserModel
        :rtype UserModel:
        """

        data = super().create(data)

        return UserModel.from_tuple(data)
