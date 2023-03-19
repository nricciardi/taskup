import unittest
from lib.utils.base import Base
from lib.settings.settings_manager import SettingsManager


class SettingsManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.settingsManager = SettingsManager()

    def test_get(self):
        self.settingsManager.get("db_name")


if __name__ == '__main__':

    unittest.main()
