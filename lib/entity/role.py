from lib.db.entity_manager import EntityManager
from dataclasses import dataclass
from lib.settings.settings_manager import SettingsManager
from lib.entity.bem import BaseEntityModel
from lib.utils.base import Base


@dataclass
class RoleModel(BaseEntityModel):
    id: int
    name: str
    permission_create: bool
    permission_read_all: bool
    permission_move_backward: bool
    permission_move_forward: bool
    permission_edit: bool
    

class RolesManager(EntityManager):
    __table_name = "role"
    __settings_manager = SettingsManager()

    def __init__(self):
        verbose = self.__settings_manager.get(self.__settings_manager.VERBOSE_KEY)
        db_name = self.__settings_manager.get(self.__settings_manager.DB_NAME_KEY)
        work_directory_path = self.__settings_manager.work_directory_path()

        super().__init__(db_name=db_name, table_name=self.__table_name, verbose=verbose,
                         work_directory_path=work_directory_path)

    def find(self, role_id: int) -> RoleModel:
        """
        Find the role with specified id

        :param role_id: role id
        :type role_id: int

        :return: RoleModel
        :rtype RoleModel:
        """

        data = super().find(role_id)

        return RoleModel.from_tuple(data)

    def create(self, data: dict) -> RoleModel:
        """
        Create the role from data

        :param data: role data
        :type data: dict

        :return: RoleModel
        :rtype RoleModel:
        """

        data = super().create(data)

        return RoleModel.from_tuple(data)
