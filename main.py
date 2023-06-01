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

    app_name = f"""{Fore.BLUE}\
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
{Fore.GREEN}run{Fore.RESET}, {Fore.GREEN}r{Fore.RESET} or {Fore.CYAN}nothing{Fore.RESET}: launch the application
{Fore.GREEN}demo{Fore.RESET}, {Fore.GREEN}d{Fore.RESET} [FLAGs] <path>: launch application with a demo database in path specified, path has to the last parameter
  {Fore.MAGENTA}-f{Fore.RESET}: force erase if there is already a database
  {Fore.MAGENTA}-o{Fore.RESET}: open app at end
  {Fore.MAGENTA}-o{Fore.RESET}: verbose
{Fore.GREEN}init, {Fore.GREEN}i{Fore.RESET}: initialize this app in users projects
  {Fore.MAGENTA}-f{Fore.RESET}: force reinitialization
{Fore.GREEN}help{Fore.RESET}, {Fore.GREEN}h{Fore.RESET}: print help 
{Fore.GREEN}version{Fore.RESET}, {Fore.GREEN}v{Fore.RESET}: print version
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

    else:
        Logger.log_warning(msg="command not found, use 'help' to see the commands list", is_verbose=True)


if __name__ == '__main__':

    main(sys.argv)




