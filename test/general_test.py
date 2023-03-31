from lib.entity.user import UsersManager, UserModel
from lib.app.project import ProjectManager
from lib.entity.task import TaskTaskLabelPivotModel, TasksManager

if __name__ == '__main__':
    pm = ProjectManager()

    user_manager = UsersManager()
    task_manager = TasksManager()

    # n = 3
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

    print(task_manager.all_as_dict())
