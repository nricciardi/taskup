import os
import datetime
from lib.app.service.project import ProjectManager
from lib.db.db import DBManager
from lib.utils.logger import Logger
from lib.utils.utils import Utils
from random import randint
from typing import Tuple
from lib.settings.settings import SettingsManager


class Demo:
    PM_EMAIL = "pm@email.com"
    PM_USERNAME = "project.manager"
    PM_PASSWORD = Utils.generate_psw()

    N_USERS = 10
    N_TASKS = 50

    NAMES: Tuple[str] = (
    "Nicola", "Alessio", "Luca", "Mario", "Giovanni", "Giuseppe", "Matteo", "Filippo", "Enrico", "Laura", "Maria",
    "Sara", "Sofia", "Alice", "Aurora", "Lorenzo")
    SURNAMES: Tuple[str] = (
    "Rossi", "Verdi", "Bianchi", "Ferrari", "Marini", "Rizzi", "Greco", "Neri", "Moretti", "Costa", "Gentile",
    "Pellegrini")

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

    def __init__(self, project_path: str, settings_manager: SettingsManager, verbose: bool = False):

        try:
            self.verbose = verbose

            Logger.log_info(msg="Demo init...", is_verbose=self.verbose)

            self.__pm = ProjectManager(settings_manager=settings_manager, verbose=self.verbose)  # load Project Manager

            self.verbose = self.verbose
            self.project_path = project_path

        except Exception as e:
            Logger.log_error(msg=f"error is occurred during the demo init", is_verbose=self.verbose)

    def launch(self, n_users: int = N_USERS, n_tasks: int = N_TASKS, force_demo: bool = False) -> None:
        try:
            Logger.log_info(msg="launch demo...", is_verbose=self.verbose)

            # prevent pre-existed db overwrite
            db_path = self.__pm.settings.assemble_db_path(project_path=self.project_path)
            if ProjectManager.already_initialized(self.project_path):

                if force_demo:
                    Logger.log_warning(msg=f"project already initialized in path '{self.project_path}', a new demo will be created...")

                else:
                    Logger.log_warning(
                        msg=f"project already initialized in path '{self.project_path}', to avoid damage the demo has been blocked!")

                    return None

            if not Utils.exist_dir(self.project_path) and not force_demo:
                Logger.log_error(msg=f"impossible initialize project because '{self.project_path}' directory not "
                                     f"found, try to force init", is_verbose=self.verbose)

                return None


            # init project
            self.__pm.init_new(self.project_path, future_pm_data={
                "email": Demo.PM_EMAIL,
                "username": Demo.PM_USERNAME,
                "password": Demo.PM_PASSWORD
            }, force_init=force_demo)

            use_localtime: bool = self.__pm.settings.get_setting_by_key(self.__pm.settings.KEY_DB_LOCALTIME)
            self.__pm.db_manager.refresh_connection(db_path=db_path, use_localtime=use_localtime)  # refresh connection

            # add data in DB
            Logger.log_info(msg=f"Add {n_users} users...", is_verbose=self.verbose)
            self.add_users(n_users)

            Logger.log_info(msg=f"Add {n_tasks} tasks...", is_verbose=self.verbose)
            self.add_tasks(n_tasks, n_users)

            # print credentials
            Logger.log_custom(msg=f"""Project manager credentials:\nemail: {Demo.PM_EMAIL}\nusername: {Demo.PM_USERNAME}\npassword: {Demo.PM_PASSWORD}""", is_verbose=self.verbose, capitalize=False)

        except Exception as e:
            Logger.log_error(msg=f"error is occurred during the demo launch", is_verbose=self.verbose, full=False)

    def add_users(self, n_users: int) -> None:

        for n in range(2, n_users + 1):     # +1 because range give [start, stop)
            name: str = self.NAMES[randint(0, len(self.NAMES) - 1)]
            surname: str = self.SURNAMES[randint(0, len(self.SURNAMES) - 1)]

            self.__pm.users_manager.create_from_dict({"username": f"{name}.{surname}{n}".lower(),
                                                      "email": f"{name}.{surname}{n}@email.com".lower(),
                                                      "name": name,
                                                      "surname": surname,
                                                      "password": "asd123",
                                                      "avatar_hex_color": Utils.random_hex_color(),
                                                      "role_id": randint(2, 4)})

    def add_tasks(self, n_tasks: int, n_users: int) -> None:

        today = datetime.date.today()

        for n in range(1, n_tasks):

            task = self.__pm.tasks_manager.create_from_dict({
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
                self.__pm.tasks_manager.add_assignment(task.id, randint(1, n_users))

            # add to-do items
            for i in range(randint(3, 15)):
                todo = self.__pm.todo_items_manager.create_from_dict({
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
                self.__pm.tasks_manager.add_label(task.id, i)
