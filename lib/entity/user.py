from lib.db.entity_manager import EntityManager
from dataclasses import dataclass
from lib.settings.settings_manager import SettingsManager



@dataclass
class User:
    id: int
    username: str


class UserManager(EntityManager):

    def __init__(self):
        settings_manager = SettingsManager()

        self.table_name = "user"
        self.db_name = settings_manager.db_path()

        super().__init__(self.db_name, self.table_name)

