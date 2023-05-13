from lib.app.app import AppManager
import sys
import colorama
from lib.utils.logger import Logger
from lib.utils.utils import Utils

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

        Utils.exit(verbose=False)

    if "version" in args or "v" in args:
        print_version()

        Utils.exit(verbose=False)

    if "demo" in args or "d" in args:
        forced: bool = "-f" in args

        if (forced and len(args) < 4) or (not forced and len(args) < 3):
            Logger.log_error(msg="too few arguments", is_verbose=True)
            Utils.exit(verbose=False)

        project_path: str = args[-1]

        AppManager.demo(project_path=project_path, force_demo=forced)

        Utils.exit(verbose=False)

    app = AppManager()

    app.start()


if __name__ == '__main__':

    main(sys.argv)




