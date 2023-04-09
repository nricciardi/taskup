import unittest
from lib.db.entity.task import TasksManager


class TaskModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # run once before all test cases
        cls.task_manager = TasksManager()

    def all(self):
        pass


if __name__ == '__main__':
    unittest.main()
