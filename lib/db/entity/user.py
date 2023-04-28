from lib.db.db import TableNamesMixin, DBManager
from lib.db.entity.entity import EntitiesManager
from dataclasses import dataclass, field
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
    permission_edit_own: bool
    permission_edit_all: bool
    permission_change_role: bool
    permission_change_assignment: bool
    permission_delete_own: bool
    permission_delete_all: bool

    # @property
    # def table_name(self) -> str:
    #     return "role"


@dataclass
class UserModel(BaseEntityModel):
    id: int
    username: str
    email: str
    password: str
    avatar_hex_color: str
    role_id: int
    role: Optional[RoleModel] = field(default=None)
    name: Optional[str] = field(default=None)
    surname: Optional[str] = field(default=None)

    # @property
    # def table_name(self) -> str:
    #     return "user"


class UsersManager(EntitiesManager, TableNamesMixin):

    def __init__(self, db_manager: DBManager, verbose: bool = False):
        self.verbose = verbose

        super().__init__(db_manager=db_manager, verbose=self.verbose)

    @property
    def EM(self) -> Type[UserModel]:
        return UserModel

    @property
    def table_name(self) -> str:
        return self.user_table_name

    @property
    def relations(self) -> list[Relation]:
        return [
            # role -< user
            OneRelation(fk_model=RoleModel, of_table=self.role_table_name, fk_field="role_id", to_attr="role")
        ]


class RolesManager(EntitiesManager, TableNamesMixin):

    def __init__(self, db_manager: DBManager, verbose: bool = False):
        self.verbose = verbose

        super().__init__(db_manager=db_manager, verbose=self.verbose)

    @property
    def EM(self) -> Type[RoleModel]:
        return RoleModel

    @property
    def table_name(self) -> str:
        return self.role_table_name

    def able_to(self, role_id: int, permission_name: str) -> bool:
        """
        Return True if users with role_id have permission specified

        :param role_id:
        :param permission_name:
        :return:
        """

        role: RoleModel = self.find(role_id)

        return bool(role.to_dict()[permission_name])
