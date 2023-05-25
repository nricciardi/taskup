from lib.db.db import TableNamesMixin, DBManager
from lib.db.entity.entity import EntitiesManager
from dataclasses import dataclass, field
from lib.db.entity.bem import BaseEntityModel
from typing import Type, Optional, Dict, TypedDict
from lib.db.entity.relation import Relation, OneRelation
from datetime import datetime
from lib.utils.utils import Utils, Logger
from lib.db.component import WhereCondition
from lib.utils.collections import ListUtils


class FuturePMData(TypedDict):
    username: str
    email: str
    password: str


@dataclass
class RoleModel(BaseEntityModel):
    id: int
    name: str
    permission_create: bool
    permission_read_all: bool
    permission_move_backward: bool
    permission_move_forward: bool
    permission_move: bool
    permission_edit_own: bool
    permission_edit_all: bool
    permission_edit_task_deadline: bool
    permission_change_role: bool
    permission_change_assignment: bool
    permission_delete_own: bool
    permission_delete_all: bool
    permission_manage_roles: bool
    permission_manage_task_status: bool
    permission_manage_task_labels: bool
    permission_manage_users: bool
    permission_remove_work: bool

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
    phone: Optional[str] = field(default=None)
    last_visit_at: Optional[datetime] = field(default=None)


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

    def create_from_dict(self, data: dict, safe: bool = True) -> UserModel | None:
        """
        Override to disguise password

        :param data:
        :param safe:
        :return:
        """

        Utils.disguise_value_of_dict(data, "password")

        return super().create_from_dict(data)

    def update_from_dict(self, entity_id: int, data: Dict, safe: bool = True, create_if_not_exists: bool = True) -> UserModel:
        """
        Override to disguise password

        :param create_if_not_exists:
        :param entity_id:
        :param data:
        :param safe:
        :return:
        """

        Utils.disguise_value_of_dict(data, "password")

        return super().update_from_dict(entity_id, data, safe, create_if_not_exists)

    def find_by_email(self, email: str) -> UserModel | None:
        """
        Find user by email

        :param email:
        :return:
        """

        try:
            user: Optional[UserModel] = ListUtils.first(self.where_as_model(WhereCondition("email", "=", email)))

            return user

        except Exception as e:
            Logger.log_error(msg=f"error during find by email using '{email}' as email", is_verbose=self.verbose)

            return None


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
