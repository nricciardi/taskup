import sys
import os


class Utils:

    @staticmethod
    def exit():
        print("Forced Exit...")
        sys.exit()

    @staticmethod
    def exist_dir(dir_path: str) -> bool:
        """
        Check if dir passed exists or not

        :param dir_path: dir's path
        :type dir_path: str
        :return:
        :rtype: bool
        """

        # check if exist
        return os.path.isdir(dir_path)
