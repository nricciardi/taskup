from lib.db.entity.user import UsersManager
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager

if __name__ == '__main__':
    pass
    pm = ProjectManager()

    users_manager = UsersManager("database.db", "/home/ncla/Desktop/project/project-pi/code/fakeproject/work")
    tasks_manager = TasksManager("database.db", "/home/ncla/Desktop/project/project-pi/code/fakeproject/work")

    # users = users_manager.all_as_model(with_relations=True)
    # print(users)

    tasks = tasks_manager.find(1, with_relations=True)
    print(tasks)

    # n = 62
    # user = user_manager.create({"username": f"franco{n}",
    #                             "email": f"n{n}@r.com",
    #                             "password": "asdf",
    #                             "role_id": 1})
    # print(user)
    #
    # task = task_manager.create({
    #     "name": f"prova task{n}",
    #     "description": f"descrizione di prova{n}",
    #     "author_id": user.id,
    #     "task_status_id": 3
    # })
    #
    # print(task_manager.all_as_model())
