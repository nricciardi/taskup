import unittest
from lib.db.entity.user import UsersManager


class UserModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # run once before all test cases
        cls.user_manager = UsersManager()

    def all(self):
        print(self.user_manager.all_as_dict())

    def create(self):
        self.user_manager.create_from_dict(name="nome")


if __name__ == '__main__':
    unittest.main()
