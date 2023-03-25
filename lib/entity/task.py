from lib.db.entity_manager import EntityManager
from dataclasses import dataclass
from lib.entity.bem import BaseEntityModel
from lib.settings.settings_manager import SettingsManager


@dataclass
class TaskModel(BaseEntityModel):
    id: int
    name: str


class TasksManager(EntityManager):
    __table_name = "task"
    __settings_manager = SettingsManager()

    def __init__(self):
        verbose = self.__settings_manager.get(self.__settings_manager.VERBOSE_KEY)
        db_name = self.__settings_manager.get(self.__settings_manager.DB_NAME_KEY)
        work_directory_path = self.__settings_manager.work_directory_path()

        super().__init__(db_name=db_name, table_name=self.__table_name, verbose=verbose,
                         work_directory_path=work_directory_path)

    def find(self, user_id: int) -> TaskModel:
        """
        Find the user with specified id

        :param user_id: user id
        :type user_id: int

        :return: UserModel
        :rtype UserModel:
        """

        data = super().find(user_id)

        return TaskModel.from_tuple(data)

    def create(self, data: dict) -> TaskModel:
        """
        Create the user from data

        :param data: user data
        :type data: dict

        :return: UserModel
        :rtype UserModel:
        """

        data = super().create(data)

        return data