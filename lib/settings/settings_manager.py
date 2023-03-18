from lib.utils.base import Base
import json


class SettingsManager(Base):
    def __int__(self):
        self.settings: dict = self.BASE_SETTINGS

        with open(self.SETTINGS_PATH) as file:
            self.settings.update(json.load(file))

    def set(self, key: str, value: str) -> None:
        """
        Modify settings

        :param key: settings' key
        :param value: key's value
        :rtype: None
        """
        self.settings[key] = value

    def get(self) -> dict:
        return self.settings


