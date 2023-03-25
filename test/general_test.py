from lib.entity.user import UsersManager, UserModel
from lib.project.project_manager import ProjectManager


if __name__ == '__main__':

    pm = ProjectManager()

    user_manager = UsersManager()

    # um = UserModel(1, "nicola")
    # um2 = UserModel(1, "asdf")
    # um3 = UserModel.from_dict()
    #
    # user_manager.create({"id": 1, "username": "franco"})
