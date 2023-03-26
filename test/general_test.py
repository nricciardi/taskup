from lib.entity.user import UsersManager, UserModel
from lib.project.project_manager import ProjectManager
from lib.entity.task import TaskTaskLabelPivotModel

if __name__ == '__main__':
    pm = ProjectManager()

    user_manager = UsersManager()

    # um = UserModel(1, "nicola")
    # um2 = UserModel(1, "asdf")
    # um3 = UserModel.from_dict()
    #

    # print(user_manager.find(1))

    n = 26
    print(user_manager.create({"username": f"franco{n}",
                               "email": f"n{n}@r.com",
                               "password": "asdf",
                               "role_id": 1}))
