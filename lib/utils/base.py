import os


class Base:

    SETTINGS_FILE_NAME = "settings"

    @property
    def BASE_DIRECTORY(self) -> str:
        """
        Return the base directory path

        :rtype: str
        """

        return os.path.abspath(os.path.join(".."))

    @property
    def SETTINGS_PATH(self) -> str:
        """
        Return the settings path of the project

        :rtype: str
        """

        return os.path.join(self.BASE_DIRECTORY, Base.SETTINGS_FILE_NAME)

    @property
    def BASE_SETTINGS(self) -> dict:
        """
        Return base settings

        :rtype: dict
        """

        return {

        }