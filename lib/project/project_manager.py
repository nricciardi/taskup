import os
from lib.settings.settings_manager import SettingsManager


class ProjectManager:
    def __init__(self):
        self.__settings_manager: SettingsManager = SettingsManager()

        # create work directory inside project if it does NOT exist
        if not self.exist_work_directory():
            self.create_work_directory()

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
