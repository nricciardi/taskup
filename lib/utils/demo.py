import os
import datetime
from lib.app.service.project import ProjectManager
from lib.db.entity.task import TasksManager, TaskAssignmentsManager, TaskLabelsManager, TaskTaskLabelPivotManager, TodoItemsManager
from lib.db.entity.user import UsersManager
from lib.utils.logger import Logger
from lib.utils.utils import Utils
from random import randint
from typing import Tuple
from lib.settings.settings import SettingsManager


class Demo:
    NAMES: Tuple[str] = ("Nicola", "Alessio", "Luca", "Mario", "Giovanni", "Giuseppe", "Matteo", "Filippo", "Enrico", "Laura", "Maria", "Sara", "Sofia", "Alice", "Aurora", "Lorenzo")
    SURNAMES: Tuple[str] = ("Rossi", "Verdi", "Bianchi", "Ferrari", "Marini", "Rizzi", "Greco", "Neri", "Moretti", "Costa", "Gentile", "Pellegrini")

    LOREM_IPSUM: str = """
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Maxime mollitia,
    molestiae quas vel sint commodi repudiandae consequuntur voluptatum laborum
    numquam blanditiis harum quisquam eius sed odit fugiat iusto fuga praesentium
    optio, eaque rerum! Provident similique accusantium nemo autem. Veritatis
    obcaecati tenetur iure eius earum ut molestias architecto voluptate aliquam
    nihil, eveniet aliquid culpa officia aut! Impedit sit sunt quaerat, odit,
    tenetur error, harum nesciunt ipsum debitis quas aliquid. Reprehenderit,
    quia. Quo neque error repudiandae fuga? Ipsa laudantium molestias eos 
    sapiente officiis modi at sunt excepturi expedita sint? Sed quibusdam
    recusandae alias error harum maxime adipisci amet laborum. Perspiciatis 
    minima nesciunt dolorem! Officiis iure rerum voluptates a cumque velit 
    quibusdam sed amet tempora. Sit laborum ab, eius fugit doloribus tenetur 
    fugiat, temporibus enim commodi iusto libero magni deleniti quod quam 
    consequuntur! Commodi minima excepturi repudiandae velit hic maxime
    doloremque. Quaerat provident commodi consectetur veniam similique ad 
    earum omnis ipsum saepe, voluptas, hic voluptates pariatur est explicabo 
    fugiat, dolorum eligendi quam cupiditate excepturi mollitia maiores labore 
    suscipit quas? Nulla, placeat. Voluptatem quaerat non architecto ab laudantium
    modi minima sunt esse temporibus sint culpa, recusandae aliquam numquam 
    totam ratione voluptas quod exercitationem fuga. Possimus quis earum veniam 
    quasi aliquam eligendi, placeat qui corporis!
    """

    def __init__(self, settings_manager: SettingsManager):

        try:
            Logger.log_info(msg="Demo init...", is_verbose=True)

            self.__pm = ProjectManager(settings_manager=settings_manager)  # load Project Manager

            self.verbose = self.__pm.verbose

            # load all managers
            self.__users_manager = UsersManager(self.__pm.db_manager, verbose=self.verbose)
            self.__task_assignment_manager = TaskAssignmentsManager(self.__pm.db_manager, verbose=self.verbose)
            self.__task_labels_manager = TaskLabelsManager(self.__pm.db_manager, verbose=self.verbose)
            self.__task_task_labels_manager = TaskTaskLabelPivotManager(self.__pm.db_manager, verbose=self.verbose)
            self.__todo_item_manager = TodoItemsManager(self.__pm.db_manager, verbose=self.verbose)
            self.__tasks_manager = TasksManager(self.__pm.db_manager, self.__task_assignment_manager,
                                                task_task_label_pivot_manager=self.__task_task_labels_manager,
                                                verbose=self.verbose)

        except Exception as e:
            Logger.log_error(msg=f"error is occurred during the demo init", is_verbose=self.verbose)

    def launch(self, n_users: int = 10, n_tasks: int = 50, force_demo: bool = False) -> None:
        try:
            Logger.log_info(msg="launch demo...", is_verbose=self.verbose)

            # prevent pre-existed db overwrite
            db_path = self.__pm.settings.db_path
            if os.path.isfile(db_path):

                if force_demo:
                    Logger.log_warning(msg=f"a database already exists in path '{db_path}', creating a new db...")

                    os.remove(db_path)      # remove oldest db

                    self.__pm.db_manager.refresh_connection()       # refresh connection because db file is changed

                else:
                    Logger.log_warning(msg=f"a database already exists in path '{db_path}', to avoid damage the demo has been blocked!")

                    return None

            Logger.log_info(msg=f"Add {n_users} users...", is_verbose=self.verbose)
            self.add_users(n_users)

            Logger.log_info(msg=f"Add {n_tasks} tasks...", is_verbose=self.verbose)
            self.add_tasks(n_tasks, n_users)

        except Exception as e:
            Logger.log_error(msg=f"error is occurred during the demo launch", is_verbose=self.verbose, full=True)

    def add_users(self, n_users: int) -> None:

        # create PM (user)
        self.__users_manager.create_from_dict({"username": f"project.manager",
                                               "email": f"pm@email.com",
                                               "name": self.NAMES[randint(0, len(self.NAMES) - 1)],
                                               "surname": self.SURNAMES[randint(0, len(self.SURNAMES) - 1)],
                                               "password": "asd123",
                                               "avatar_hex_color": Utils.random_hex_color(),
                                               "role_id": 1
                                               })

        for n in range(1, n_users):
            name: str = self.NAMES[randint(0, len(self.NAMES) - 1)]
            surname: str = self.SURNAMES[randint(0, len(self.SURNAMES) - 1)]

            self.__users_manager.create_from_dict({"username": f"{name}.{surname}{n}".lower(),
                                                   "email": f"{name}.{surname}{n}@email.com".lower(),
                                                   "name": name,
                                                   "surname": surname,
                                                   "password": "asd123",
                                                   "avatar_hex_color": Utils.random_hex_color(),
                                                   "role_id": randint(2, 4)})

    def add_tasks(self, n_tasks: int, n_users: int) -> None:

        today = datetime.date.today()

        for n in range(1, n_tasks):

            task = self.__tasks_manager.create_from_dict({
                "name": f"Name of task {n}",
                "description": self.LOREM_IPSUM,
                "author_id": randint(1, n_users),
                "task_status_id": randint(1, 8),
                "priority": randint(1, 20),
                "deadline": datetime.datetime(today.year,
                                              randint(today.month, (today.month + 2) % 12),
                                              randint(1, 30),
                                              randint(8, 19),
                                              randint(1, 59)
                                              ).strftime("%Y-%m-%d %H:%M:%S") if randint(1, 2) % 2 == 0 else None
            })

            for i in range(randint(1, 8)):
                self.__tasks_manager.add_assignment(task.id, randint(1, n_users))

            # add to-do items
            for i in range(randint(3, 15)):
                todo = self.__todo_item_manager.create_from_dict({
                    "description": f" {i + 1}° To-do of task",
                    "author_id": randint(1, n_users),
                    "task_id": task.id,
                    "deadline": datetime.datetime(today.year,
                                                  randint(today.month, (today.month + 2) % 12),
                                                  randint(1, 30),
                                                  randint(8, 19),
                                                  randint(1, 59)
                                                  ).strftime("%Y-%m-%d %H:%M:%S") if randint(1, 2) % 2 == 0 else None
                })

            for i in range(1, randint(1, 3)):
                self.__tasks_manager.add_label(task.id, i)


