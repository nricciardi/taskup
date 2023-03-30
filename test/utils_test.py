import unittest
from lib.utils.base import Base


class UtilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = Base()

    def test_base_directory(self):
        self.assertEqual("/home/ncla/Desktop/app/app-pi/code/pi-app", self.base.base_directory)


if __name__ == '__main__':

    unittest.main()
