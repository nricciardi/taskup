from lib.utils.base import Base
import json


class SettingsManager(Base):
    def __init__(self):
        super().__init__()

        self.settings: dict = self.base_settings

        with open(self.settings_path) as file:
            self.settings.update(json.load(file))

    def set(self, key: str, value: str) -> None:
        """
        Modify settings

        :param key: settings' key
        :param value: key's value

        :rtype: None
        """
        self.settings[key] = value

    def get(self, key: str) -> str:
        """
        Return the value of key passed

        :param key: A key of settings
        :type key: str

        :rtype: str
        """

        return self.settings[key]


