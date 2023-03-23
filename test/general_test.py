from lib.entity.user import UserManager, UserModel



if __name__ == '__main__':

    user_manager = UserManager()

    um = UserModel(1, "nicola")
    user_manager.create(UserModel(1, "asdf"))