from lib.db.db_manager import DBManager
from lib.settings.settings_manager import SettingsManager


class EntityManager(DBManager):
    __table_name: str = None
    __db_name: str = None

    def __init__(self):

        self.__settings_manager = SettingsManager()
        self.__db_name = self.__settings_manager.get(self.__settings_manager.DB_NAME_KEY)

        super().__init__(db_name=self.__db_name, work_directory=self.__settings_manager.work_directory_path(),
                         verbose=self.__settings_manager.get(self.__settings_manager.VERBOSE_KEY))

    @classmethod
    def using(cls, table_name: str, db_name: str) -> object:
        """
        Factory of EntityManger using passed table name and db name

        :param table_name:
        :type table_name: str
        :param db_name:
        :type db_name: str
        :return: EntityManger
        :rtype EntityManger:
        """

        cls.__table_name = table_name

        cls.__db_name = db_name

        return EntityManager()

    @property
    def table_name(self) -> str:
        """
        Return table name

        :rtype: str
        """

        return self.__table_name

    @table_name.setter
    def table_name(self, value) -> None:
        """
        Change entity

        :param value: table name of entity
        """

        self.__table_name = value

    def all(self) -> list:
        """
        Return all records from db table

        :return: All records from db table
        :rtype: list
        """

        res = self.__db_cursor.execute(f"Select * From {self.table_name}")

        return res.fetchall()

    def find(self, entity_id: int) -> dict:
        """
        Return the record requested

        :param entity_id: the record's id
        :type entity_id: int
        :return:
        """

        res = self.__db_cursor.execute(f"Select * From {self.table_name} Where {self.table_name}.id = {entity_id}")

        return res.fetchone()
