import os
from lib.db.query import SelectQueryBuilder
from lib.db.entity.user import UsersManager
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager

if __name__ == '__main__':

    # os.remove("/home/ncla/Desktop/project/project-pi/code/fakeproject/work/database.db")
    pm = ProjectManager()

    users_manager = UsersManager("database.db", "/home/ncla/Desktop/project/project-pi/code/fakeproject/work", verbose=True)
    tasks_manager = TasksManager("database.db", "/home/ncla/Desktop/project/project-pi/code/fakeproject/work", verbose=True)

    # query = SelectQueryBuilder.from_table("user").select().where("username", "=", "franco1").to_sql()
    # # print(query)
    #
    users = users_manager.all_as_model(with_relations=True)
    print(users)
    #
    # tasks = tasks_manager.find(1, with_relations=True, safe=False)
    # print(tasks.to_dict())

    n = 3

    for n in range(10):
        user = users_manager.create_from_dict({"username": f"franco{n}",
                                    "email": f"n{n}@r.com",
                                    "password": "asdf123",
                                    "role_id": 1})

        print(user)

        task = tasks_manager.create_from_dict({
            "name": f"prova task{n}",
            "description": f"descrizione di prova{n}",
            "author_id": user.id,
            "task_status_id": 3
        })




