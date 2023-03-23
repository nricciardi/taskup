import unittest
from lib.entity.user import UserManager
import logging


class UserModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # run once before all test cases
        cls.user_manager = UserManager()

    def all(self):
        print(self.user_manager.all())

    def create(self):
        self.user_manager.create(name="nome")


if __name__ == '__main__':
    unittest.main()
