import unittest
from lib.entity.user import UserManager


class UserModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # run once before all test cases
        cls.user_manager = UserManager()

    def all(self):
        print(self.user_manager.all())


if __name__ == '__main__':
    unittest.main()
