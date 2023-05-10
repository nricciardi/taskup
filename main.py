from lib.app.app import AppManager
import sys
import colorama
from colorama import Fore, Back, Style

from lib.utils.demo import Demo

# Initialising Colorama (Important)
colorama.init(autoreset=True)


def print_help() -> None:
    """
    Print the help for user

    :return:
    """

    msg: str = """\
    - run, r or nothing: launch the application
    - demo, d: launch application with a demo database
      - -f: force erase if there is already a database
    - init, i: initialize this app in users projects
      - -f: force reinitialization
    - help, h: print help 
    - version, v: print version
    """

    print(msg)


def print_version() -> None:
    print(AppManager.VERSION)


def main(args: list) -> None:
    """
    Launch main to startup app

    :return:
    """

    if "help" in args or "h" in args:
        print_help()
        return

    if "version" in args or "v" in args:
        print_version()
        return

    if "demo" in args or "d" in args:
        forced = "-f" in args

        AppManager.demo(force_demo=forced)

        return

    app = AppManager()

    app.start()


if __name__ == '__main__':

    main(sys.argv)




