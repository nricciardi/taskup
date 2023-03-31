from lib.db.entity import EntityManager
from dataclasses import dataclass
from lib.settings.settings import SettingsManager
from lib.entity.bem import BaseEntityModel, BEM
from lib.utils.base import Base
from typing import List, Dict, Any


@dataclass
class UserModel(BaseEntityModel):
    id: int
    username: str
    email: str
    password: str
    role_id: int


class UsersManager(EntityManager):
    __table_name = "user"

    db_use_localtime = False

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, table_name=self.__table_name, verbose=self.verbose,
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

    def all_as_dict(self) -> List[Dict[str, Any]]:
        """
        Return all users as list of dict

        :return: all users as dict
        :rtype List[Dict[str, Any]]:
        """

        raise NotImplementedError

    def all_as_model(self) -> List[UserModel]:
        """
        Return all users as list of model

        :return: all roles
        :rtype List[UserModel]:
        """

        raise NotImplementedError


@dataclass
class RoleModel(BaseEntityModel):
    id: int
    name: str
    permission_create: bool
    permission_read_all: bool
    permission_move_backward: bool
    permission_move_forward: bool
    permission_edit: bool
    permission_change_role: bool
    permission_change_assignment: bool


class RolesManager(EntityManager):
    __table_name = "role"
    __settings_manager = SettingsManager()

    def __init__(self):
        self.verbose = self.__settings_manager.get(self.__settings_manager.KEY_VERBOSE)
        self.db_name = self.__settings_manager.get(self.__settings_manager.KEY_DB_NAME)
        work_directory_path = self.__settings_manager.work_directory_path()

        super().__init__(db_name=self.db_name, table_name=self.__table_name, verbose=self.verbose,
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
        Create a role from data

        :param data: role data
        :type data: dict

        :return: RoleModel
        :rtype RoleModel:
        """

        data = super().create(data)

        return RoleModel.from_tuple(data)

    def all_as_dict(self) -> List[Dict[str, Any]]:
        """
        Return all roles as list of dict

        :return: all users as dict
        :rtype List[Dict[str, Any]]:
        """

        raise NotImplementedError

    def all_as_model(self) -> List[RoleModel]:
        """
        Return all roles as list of model

        :return: all roles
        :rtype List[RoleModel]:
        """

        raise NotImplementedError
