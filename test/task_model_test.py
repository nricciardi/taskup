import unittest
from lib.db.models import Task

class TaskModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # run once before all test cases
        cls.task = Task()

    def all(self):
        pass





if __name__ == '__main__':
    unittest.main()