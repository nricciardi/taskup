from lib.app.app import App
import sys
import colorama
from colorama import Fore, Back, Style


# Initialising Colorama (Important)
colorama.init(autoreset=True)


def help():
    """
    Print the help for user

    :return:
    """



def main(*args):
    """
    Launch main to startup app

    :return:
    """

    app = App()

    app.start()


if __name__ == '__main__':

    main(*sys.argv)


