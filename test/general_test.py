import os
from lib.db.query import SelectQueryBuilder
from lib.db.entity.user import UsersManager
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager
from lib.db.component import WhereCondition
from lib.app.service.auth import AuthService
from random import randint

if __name__ == '__main__':

    os.remove("/home/ncla/Desktop/project/project-pi/code/fakeproject/work/database.db")
    pm = ProjectManager()

    users_manager = UsersManager("database.db", "/home/ncla/Desktop/project/project-pi/code/fakeproject/work", verbose=True)
    tasks_manager = TasksManager("database.db", "/home/ncla/Desktop/project/project-pi/code/fakeproject/work", verbose=True)

    # auth = AuthService(users_manager, "/home/ncla/Desktop/project/project-pi/code/fakeproject/work/fakevault.json", True)
    # auth.login("n1@r.com", "asdf123", False)

    # query = SelectQueryBuilder.from_table("user").enable_binding().select().where("username", "=", "franco1")
    # print(query.to_sql())
    # print(query.data_bound)

    #
    # users = users_manager.all_as_dict(with_relations=True)
    # print(users)
    #
    # tasks = tasks_manager.find(1, with_relations=True, safe=False)
    # print(tasks.to_dict())

    # users_manager.where_as_model(WhereCondition("username", "=", "franco2"))

    offset = 1
    count = 1

    for n in range(count * offset, count * offset + count):
        user = users_manager.create_from_dict({"username": f"franco{n}",
                                    "email": f"n{n}@r.com",
                                    "password": "asdf123",
                                    "role_id": 1})

        print(user)

        task = tasks_manager.create_from_dict({
            "name": f"prova task{n}",
            "description": f"descrizione di prova{n}",
            "author_id": user.id,
            "task_status_id": randint(1, 8)
        })




