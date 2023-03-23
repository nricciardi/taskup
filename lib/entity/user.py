from lib.db.entity_manager import EntityManager
from dataclasses import dataclass
from lib.settings.settings_manager import SettingsManager



@dataclass
class UserModel:
    id: int
    username: str


class UserManager(EntityManager):

    __table_name = "user"
    __settings_manager = SettingsManager()

    def __init__(self):

        verbose = self.__settings_manager.get(self.__settings_manager.VERBOSE_KEY)
        db_name = self.__settings_manager.get(self.__settings_manager.DB_NAME_KEY)
        work_directory_path = self.__settings_manager.work_directory_path()

        super().__init__(db_name=db_name, table_name=self.__table_name, verbose=verbose, work_directory_path=work_directory_path)

    @property
    def _type(self):

        return UserModel

