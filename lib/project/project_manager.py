import os
from lib.settings.settings import SettingsManager
from lib.db.db import DBManager


class ProjectManager:
    def __init__(self):
        self.__settings_manager: SettingsManager = SettingsManager()

        self.verbose = self.__settings_manager.get(self.__settings_manager.VERBOSE_KEY)
        db_name = self.__settings_manager.get(self.__settings_manager.DB_NAME_KEY)
        use_localtime = self.__settings_manager.get(self.__settings_manager.DB_LOCALTIME_KEY)
        work_directory_path = self.__settings_manager.work_directory_path()

        # create work directory inside project if it does NOT exist
        if not self.exist_work_directory():
            self.create_work_directory()

        # generate db base structure if db doesn't exist
        self.__db_manager = DBManager(db_name=db_name,
                                      work_directory_path=work_directory_path,
                                      verbose=self.verbose,
                                      use_localtime=use_localtime)

    def exist_work_directory(self) -> bool:
        """
        Check if work directory exist

        :rtype bool:
        """

        # check if exist
        return os.path.isdir(self.__settings_manager.work_directory_path())

    def create_work_directory(self) -> None:
        """
        Create work directory in the project

        :rtype None:
        """

        os.mkdir(self.__settings_manager.work_directory_path())

    @property
    def project_path(self):
        return self.__settings_manager.project_directory_path()
