import unittest
from lib.db.db import DBManager


class DBManagerTest(unittest.TestCase):
    db_manager = DBManager()

    @classmethod
    def setUpClass(cls):  # run once before all test cases
        pass

    @classmethod
    def tearDownClass(cls):  # run once after all test cases
        pass

    def setUp(self):  # run before each test case
        pass

    def tearDown(self):  # run after each test case
        pass


if __name__ == '__main__':
    unittest.main()
