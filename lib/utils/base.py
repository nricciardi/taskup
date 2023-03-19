import os


class Base:

    def __init__(self):
        pass

    @property
    def settings_file_name(self) -> str:
        """
        Return the settings file name

        :rtype: str
        """

        return "settings.json"

    @property
    def base_directory(self) -> str:
        """
        Return the base directory path

        :rtype: str
        """

        return os.path.abspath(os.path.join("..", ".."))

    @property
    def settings_path(self) -> str:
        """
        Return the settings path of the project

        :rtype: str
        """

        return os.path.join(self.base_directory, self.settings_file_name)

    @property
    def base_settings(self) -> dict:
        """
        Return base settings

        :rtype: dict
        """

        return {

        }