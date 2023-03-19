import unittest
from lib.entity.task import TaskManager


class TaskModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # run once before all test cases
        cls.task_manager = TaskManager()

    def all(self):
        pass


if __name__ == '__main__':
    unittest.main()
