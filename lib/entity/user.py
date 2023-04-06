from lib.db.entity import EntityManager
from dataclasses import dataclass
from lib.entity.bem import BaseEntityModel
from typing import List, Dict, Any, Type


@dataclass
class UserModel(BaseEntityModel):
    id: int
    username: str
    email: str
    password: str
    role_id: int


class UsersManager(EntityManager):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose,
                         work_directory_path=work_directory_path)

    @property
    def table_name(self) -> str:
        return "user"

    @property
    def EM(self) -> Type[UserModel]:
        return UserModel


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

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose,
                         work_directory_path=work_directory_path)

    @property
    def EM(self) -> Type[RoleModel]:
        return RoleModel

    @property
    def table_name(self) -> str:
        return "role"
