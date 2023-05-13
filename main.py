from lib.app.app import AppManager
import sys
import colorama
from lib.utils.logger import Logger
from lib.utils.utils import Utils
from typing import Dict, List

# Initialising Colorama (Important)
colorama.init(autoreset=True)


def flags_management(min_params: int, flags: Dict, args: List):
    """
    Manage flags

    :param args:
    :param min_params:
    :param flags:
    :return:
    """

    for key in flags.keys():
        if flags.get(key, False):
            min_params += 1

    if len(args) < min_params:
        Logger.log_error(msg="too few arguments", is_verbose=True)
        Utils.exit(verbose=False)


def print_help() -> None:
    """
    Print the help for user

    :return:
    """

    app_name = """\
 ███████████                   █████                          
░█░░░███░░░█                  ░░███                           
░   ░███  ░   ██████    █████  ░███ █████ █████ ████ ████████ 
    ░███     ░░░░░███  ███░░   ░███░░███ ░░███ ░███ ░░███░░███
    ░███      ███████ ░░█████  ░██████░   ░███ ░███  ░███ ░███
    ░███     ███░░███  ░░░░███ ░███░░███  ░███ ░███  ░███ ░███
    █████   ░░████████ ██████  ████ █████ ░░████████ ░███████ 
   ░░░░░     ░░░░░░░░ ░░░░░░  ░░░░ ░░░░░   ░░░░░░░░  ░███░░░  
                                                     ░███     
                                                     █████    
                                                    ░░░░░      
"""

    print(app_name)

    msg: str = """
run, r or nothing: launch the application
demo, d: launch application with a demo database in path specified, path has to the last parameter
  -f: force erase if there is already a database
  -o: open app at end
init, i: initialize this app in users projects
  -f: force reinitialization
help, h: print help 
version, v: print version
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
        flags: Dict = {
                "forced": "-f" in args,
                "open_app_at_end": "-o" in args,
            }

        flags_management(min_params=3, flags=flags, args=args)

        project_path: str = args[-1]

        AppManager.demo(project_path=project_path, force_demo=flags["forced"], open_app_at_end=flags["open_app_at_end"])

        Utils.exit(verbose=False)

    AppManager.starter()


if __name__ == '__main__':

    main(sys.argv)




