import eel
from lib.settings.settings import SettingsManager
from lib.utils.logger import Logger
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager
from lib.db.entity.user import UsersManager
from lib.app.service.exposer import ExposerService


class App:
    __settings_manager = SettingsManager()

    def __init__(self):
        self.__verbose = self.__settings_manager.verbose()  # get verbose

        Logger.log_info(msg="App init...", is_verbose=self.__verbose)

        frontend_directory = self.__settings_manager.frontend_directory()
        eel.init(frontend_directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])  # init eel

        self.__project_manager = ProjectManager()

        db_name = self.__settings_manager.db_name()
        work_directory_path = self.__settings_manager.work_directory_path()
        vault_path = self.__settings_manager.vault_path()

        # expose methods
        exposer = ExposerService(db_name, work_directory_path, vault_path, verbose=self.__verbose)
        exposer.expose_methods()

    def start(self):
        start_file = self.__settings_manager.frontend_start()
        port = self.__settings_manager.port()

        eel.start(start_file, port=port,
                  #close_callback=lambda: Logger.log_info(msg="Close app...", is_verbose=True),
                  shutdown_delay=20)  # start eel: this generates a loop
