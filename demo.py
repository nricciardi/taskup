import os
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager, TaskAssignmentsManager, TaskLabelsManager, TaskTaskLabelPivotManager, \
    TodoItemsManager
from lib.db.entity.user import UsersManager
from lib.utils.logger import Logger
from lib.utils.utils import Utils


class Demo:

    def __init__(self, verbose: bool = True):
        self.__pm = ProjectManager()

        self.__users_manager = UsersManager(self.__pm.db_manager, verbose=verbose)
        self.__task_assignment_manager = TaskAssignmentsManager(self.__pm.db_manager, verbose=verbose)
        self.__task_labels_manager = TaskLabelsManager(self.__pm.db_manager, verbose=verbose)
        self.__task_task_labels_manager = TaskTaskLabelPivotManager(self.__pm.db_manager, verbose=verbose)
        self.__todo_item_manager = TodoItemsManager(self.__pm.db_manager, verbose=verbose)
        self.__tasks_manager = TasksManager(self.__pm.db_manager, self.__task_assignment_manager,
                                            task_task_label_pivot_manager=self.__task_task_labels_manager,
                                            verbose=verbose)

    def launch(self) -> None:
        # prevent pre-existed db overwrite
        if os.path.isfile(self.__pm.settings.db_path):
            return None

        # create PM
        self.__users_manager.create_from_dict({"username": f"pm",
                                               "email": f"pm@pm.com",
                                               "password": "asdf123",
                                               "avatar_hex_color": Utils.random_hex(),
                                               "role_id": 1
                                               })


if __name__ == '__main__':
    demo = Demo()

    demo.launch()
