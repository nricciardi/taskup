from lib.app.app import AppManager
import sys
import colorama
from colorama import Fore
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

    app_name = f"""\n{Fore.BLUE}
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
{Fore.RESET}"""

    print(app_name)

    msg: str = f"""\
{Fore.LIGHTGREEN_EX}run{Fore.RESET}, {Fore.LIGHTGREEN_EX}r{Fore.RESET}: launch the application
{Fore.LIGHTGREEN_EX}demo{Fore.RESET}, {Fore.LIGHTGREEN_EX}d{Fore.RESET} {Fore.GREEN}[-flag1 -flag2 ...] <path>{Fore.RESET}: launch application with a demo database in path specified, path has to the last parameter
  {Fore.MAGENTA}-f{Fore.RESET}: force erase if there is already a database
  {Fore.MAGENTA}-o{Fore.RESET}: open app at end
  {Fore.MAGENTA}-v{Fore.RESET}: verbose
{Fore.LIGHTGREEN_EX}init{Fore.RESET}, {Fore.LIGHTGREEN_EX}i{Fore.RESET} {Fore.GREEN}[-flag1 -flag2 ...] <path>{Fore.RESET}: initialize this app in users projects
  {Fore.MAGENTA}-f{Fore.RESET}: force reinitialization
  {Fore.MAGENTA}-o{Fore.RESET}: open app at end
{Fore.LIGHTGREEN_EX}help{Fore.RESET}, {Fore.LIGHTGREEN_EX}h{Fore.RESET}: print help 
{Fore.LIGHTGREEN_EX}version{Fore.RESET}, {Fore.LIGHTGREEN_EX}v{Fore.RESET}: print version
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

    elif "version" in args or "v" in args:
        print_version()

        Utils.exit(verbose=False)

    elif "demo" in args or "d" in args:
        flags: Dict = {
                "forced": "-f" in args,
                "open_app_at_end": "-o" in args,
                "verbose": "-v" in args,
            }

        flags_management(min_params=3, flags=flags, args=args)

        project_path: str = args[-1]

        AppManager.demo(project_path=project_path, force_demo=flags["forced"], open_app_at_end=flags["open_app_at_end"],
                        verbose=flags["verbose"])

        Utils.exit(verbose=False)

    elif "run" in args or "r" in args:

        AppManager.starter()

    elif "init" in args or "i" in args:
        flags: Dict = {
            "forced": "-f" in args,
            "open_app_at_end": "-o" in args,
        }

        flags_management(min_params=2, flags=flags, args=args)

        project_path: str = args[-1]

        AppManager.initializer(project_path=project_path, open_on_init=flags["open_app_at_end"], force_init=flags["forced"])

    else:
        Logger.log_warning(msg="command not found, use 'help' to see the commands list", is_verbose=True)


if __name__ == '__main__':

    main(sys.argv)




