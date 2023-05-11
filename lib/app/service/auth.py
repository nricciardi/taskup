from lib.db.entity.user import UserModel, UsersManager, RolesManager
from lib.db.component import WhereCondition
from lib.utils.collections import CollectionsUtils
from lib.utils.logger import Logger
from lib.file.file_manager import FileManger
from typing import List, Callable, Optional
from lib.utils.error import Errors
from dataclasses import dataclass
from lib.utils.utils import Utils
from lib.db.query import QueryBuilder


@dataclass
class VaultData:
    email: str
    password: str


class AuthService:
    REFRESH_INTERVAL: int = 1  # seconds
    __users_manager: UsersManager
    __me: UserModel | None = None
    __local_vault: Optional[VaultData] = None

    EMAIL = "email"
    PASSWORD = "password"

    def __init__(self, users_manager: UsersManager, vault_path: str, verbose: bool = False):
        self.__users_manager = users_manager
        self.__vault_path = vault_path
        self.verbose = verbose

        self.try_autologin()

    def __del__(self):
        self.__me = None

    @property
    def vault_path(self) -> str:
        return self.__vault_path

    def refresh_me(self) -> None:
        """
        Refresh logged user data using local vault data

        :return:
        """

        if self.__local_vault is not None:
            users_matched: List = self.__users_manager.where_as_model(
                WhereCondition("email", "=", self.__local_vault.email),
                WhereCondition("password", "=", self.__local_vault.password),
                with_relations=True
            )

            self.__me = CollectionsUtils.first(users_matched)

    def me(self) -> UserModel | None:

        return self.__me

    def try_autologin(self) -> None:
        """
        Try the autologin using vault data

        :return:
        """

        try:
            Logger.log_info(msg="try autologin...", is_verbose=self.verbose)

            vault_data = self.get_vault_data()

            if self.EMAIL in vault_data and self.PASSWORD in vault_data:

                email: str = vault_data.get(self.EMAIL)
                password: str = vault_data.get(self.PASSWORD)

                self.login(email=email, password=password, disguise_psw=False)      # disguise_psw=False because psw is already disguised if it is in vault
            else:
                raise AttributeError()

        except Exception:

            Logger.log_warning(msg="autologin failed", is_verbose=self.verbose)

            return None

    def is_logged(self) -> bool:
        return self.__me is not None

    def login(self, email: str, password: str, keep: bool = False, disguise_psw: bool = True) -> UserModel | None:
        """
        Login user by email and password

        :param disguise_psw: flag which indicates if password must be disguised
        :param keep: keep data on login
        :type keep: bool
        :param email:
        :type email: str
        :param password:
        :type password: str
        :return: logged user
        :rtype: UserModel
        """

        # disguise password if required
        if disguise_psw:
            password = Utils.disguise(password)

        self.__local_vault = VaultData(email=email, password=password)
        self.refresh_me()       # try to refresh me with local vault data

        if self.__me is None:   # if me is None => login error (nobody users is found with email + password)
            msg: str = f"no match with email ({email}) and password ({password})"

            Logger.log_error(msg=msg, is_verbose=self.verbose)

            return None

        Logger.log_success(msg="logged in correctly", is_verbose=self.verbose)

        if keep:
            self.store_in_vault(email, password)

        return self.__me

    def logout(self) -> bool:
        try:

            self.erase_vault_data()

            self.__me = None
            self.__local_vault = None

            Logger.log_success(msg="logout correctly", is_verbose=self.verbose)

            return True

        except Exception as e:

            Logger.log_error(msg=e, is_verbose=self.verbose)

            return False

    def store_in_vault(self, email: str, password: str) -> None:
        """
        Store in vault email and password

        :param email:
        :type email: str
        :param password:
        :type password: str

        :return:
        :rtype None:
        """

        FileManger.write_json(self.vault_path, {
            self.EMAIL: email,
            self.PASSWORD: password
        })

        Logger.log_success(msg=f"email ({email}) and password ({'*' * len(password)}) are stored successful in vault ('{self.vault_path}')",
                           is_verbose=self.verbose)

    def get_vault_data(self) -> dict | None:
        """
        Get data in vault

        :return: data
        :rtype dict:
        """

        return FileManger.read_json(self.vault_path)

    def erase_vault_data(self) -> bool:

        try:
            FileManger.write_json(self.vault_path, "")

            return True
        except Exception:
            Logger.log_warning(msg="vault erase error", is_verbose=self.verbose)

            return False

    def update_last_visit(self) -> None:
        """
        Update last visit of logged user

        :return:
        """

        logged_user = self.me()
        table_name: str = self.__users_manager.table_name

        update_last_visit_query: str = QueryBuilder.from_table(table_name).update_from_dict({
            "last_visit_at": "DATETIME('now')"
        }).apply_conditions(WhereCondition("id", "=", logged_user.id)).to_sql()

        self.__users_manager.db_manager.execute(update_last_visit_query)


def login_required(func: Callable, auth: AuthService, verbose: bool = False) -> Callable:
    """
    Prevent function's call if user is NOT logged in

    :param verbose:
    :param func:
    :type func: Callable
    :param auth:
    :type auth: AuthService

    :return:
    """

    def wrapper(*args, **kwargs):
        if not auth.is_logged():
            if verbose:
                Logger.log_error(msg=f"login is required to call {func}")

            return Errors.LOGIN_REQUIRE.to_dict()

        return func(*args, **kwargs)

    return wrapper


def permission_required(func: Callable, auth: AuthService, roles_manager: RolesManager, *permissions_names, verbose: bool = False) -> Callable:
    """
    Prevent function's call if user has NO permission(s)

    :param roles_manager:
    :param verbose:
    :param func:
    :type func: Callable
    :param auth:
    :type auth: AuthService

    :return:
    """

    def wrapper(*args, **kwargs):
        if not auth.is_logged():
            return login_required(func, auth, verbose)

        logged_user: UserModel = auth.me()

        for p_name in permissions_names:
            if roles_manager.able_to(logged_user.role_id, p_name):
                return Errors.PERMISSION_DENIED.to_dict()

        return func(*args, **kwargs)

    return wrapper
