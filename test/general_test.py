import os
from lib.db.query import QueryBuilder
from lib.db.entity.user import UsersManager
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager, TaskAssignmentsManager, TaskLabelsManager, TaskTaskLabelPivotManager, TodoItemsManager
from lib.db.component import WhereCondition
from lib.app.service.auth import AuthService
from random import randint
import sqlite3
import datetime


db_path = "/home/ncla/Desktop/project/project-pi/code/fakeproject/work/database.db"

if os.path.isfile(db_path):
    os.remove(db_path)
pm = ProjectManager()

users_manager = UsersManager(pm.db_manager, verbose=True)
task_assignment_manager = TaskAssignmentsManager(pm.db_manager, verbose=True)
task_labels_manager = TaskLabelsManager(pm.db_manager, verbose=True)
task_task_labels_manager = TaskTaskLabelPivotManager(pm.db_manager, verbose=True)
todo_item_manager = TodoItemsManager(pm.db_manager, verbose=True)
tasks_manager = TasksManager(pm.db_manager, task_assignment_manager,
                             task_task_label_pivot_manager=task_task_labels_manager, verbose=True)


def create_demo_db():
    def random_hex() -> str:
        random_number = randint(0, 16777215)
        hex_number = str(hex(random_number))
        hex_number = f"{hex_number[2:]}"

        return hex_number

    users_manager.create_from_dict({"username": f"pm",
                                    "email": f"pm@pm.com",
                                    "password": "asdf123",
                                    "avatar_hex_color": random_hex(),
                                    "role_id": 1})

    # task = tasks_manager.create_from_dict({
    #     "name": f"prova task single" * randint(1, 4),
    #     "description": f"descrizione di prova single" * randint(10, 60),
    #     "author_id": 1,  # user.id,
    #     "task_status_id": 4,
    #     "priority": randint(1, 20),
    #     "deadline": datetime.datetime(2023,
    #                                   4,
    #                                   17,
    #                                   9,
    #                                   4
    #                                   ).strftime("%Y-%m-%d %H:%M:%S")
    # })

    u = 8
    for n in range(1, u):
        users_manager.create_from_dict({"username": f"franco{n}",
                                        "email": f"n{n}@r.com",
                                        "password": "asdf123",
                                        "avatar_hex_color": random_hex(),
                                        "role_id": randint(2, 4)})

    offset = 0
    count = 300

    for n in range(count * offset, count * offset + count):
        # user = users_manager.create_from_dict({"username": f"franco{n}",
        #                             "email": f"n{n}@r.com",
        #                             "password": "asdf123",
        #                             "role_id": 1})
        #
        # print(user)

        task = tasks_manager.create_from_dict({
            "name": f"prova task{n}" * randint(1, 4),
            "description": f"descrizione di prova{n}" * randint(10, 60),
            "author_id": randint(1, u),
            "task_status_id": randint(1, 8),
            "priority": randint(1, 20),
            "deadline": datetime.datetime(2023,
                                          randint(4, 7),
                                          randint(1, 30),
                                          randint(8, 19),
                                          randint(1, 59)
                                          ).strftime("%Y-%m-%d %H:%M:%S") if randint(1, 2) % 2 == 0 else None
        })

        for i in range(randint(1, 8)):
            tasks_manager.add_assignment(task.id, randint(1, u))

        for i in range(randint(3, 15)):
            todo = todo_item_manager.create_from_dict({
                "description": f"sono un todo del task {n}" * randint(1, 3),
                "author_id": randint(1, u),
                "task_id": task.id,
                "deadline": datetime.datetime(2023,
                                              randint(4, 7),
                                              randint(1, 30),
                                              randint(8, 19),
                                              randint(1, 59)
                                              ).strftime("%Y-%m-%d %H:%M:%S") if randint(1, 2) % 2 == 0 else None
            })

        for i in range(1, randint(1, 3)):
            tasks_manager.add_label(task.id, i)


if __name__ == '__main__':
    print("start main...")


    # auth = AuthService(users_manager, "/home/ncla/Desktop/project/project-pi/code/fakeproject/work/fakevault.json", True)
    # auth.login("n1@r.com", "asdf123", False)

    # query = SelectQueryBuilder.from_table("user").enable_binding().select().where("username", "=", "franco1")
    # print(query.to_sql())
    # print(query.data_bound)

    #
    # users = users_manager.all_as_dict(with_relations=True)
    # print(users)

    # users = users_manager.all_as_model(with_relations=True)
    # print(users)

    #
    # tasks = tasks_manager.find(36, with_relations=True, safe=False)
    # print(tasks.assigned_users)

    # users_manager.where_as_model(WhereCondition("username", "=", "franco2"))

    create_demo_db()



    # def dict_factory(cursor, row):
    #
    #     print(type(row))
    #
    #     fields = [column[0] for column in cursor.description]
    #     return {key: value for key, value in zip(fields, row)}
    #
    # con = sqlite3.connect(db_path)
    # con.row_factory = dict_factory
    # cur = con.cursor()
    #
    # res = cur.execute("Select * From user where id = 1")
    #
    # res = res.fetchall()
    #
    #
    # print(res)




