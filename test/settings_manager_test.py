import unittest
from lib.utils.logger import Logger
from lib.settings.settings import SettingsManager


class SettingsManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.settingsManager = SettingsManager()

    def test_get(self):
        print(self.settingsManager.get_setting_by_key("db_name"))


if __name__ == '__main__':

    unittest.main()
