from lib.db.db import TableNamesMixin
from lib.db.entity.entity import EntitiesManager
from dataclasses import dataclass
from lib.db.entity.bem import BaseEntityModel
from typing import Type, Optional
from lib.db.entity.relation import Relation, OneRelation


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

    # @property
    # def table_name(self) -> str:
    #     return "role"


@dataclass
class UserModel(BaseEntityModel):
    id: int
    username: str
    email: str
    password: str
    role_id: int
    role: Optional[RoleModel] = None

    # @property
    # def table_name(self) -> str:
    #     return "user"


class UsersManager(EntitiesManager, TableNamesMixin):

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):
        self.verbose = verbose
        self.db_name = db_name
        work_directory_path = work_directory_path

        super().__init__(db_name=self.db_name, verbose=self.verbose, work_directory_path=work_directory_path)

    @property
    def EM(self) -> Type[UserModel]:
        return UserModel

    @property
    def table_name(self) -> str:
        return self.user_table_name

    @property
    def relations(self) -> list[Relation]:
        return [
            OneRelation(fk_model=RoleModel, of_table=self.role_table_name, fk_field="role_id", to_attr="role")
        ]


class RolesManager(EntitiesManager, TableNamesMixin):

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
        return self.role_table_name
