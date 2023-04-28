import eel
from lib.settings.settings import SettingsManager
from lib.utils.logger import Logger
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager
from lib.db.entity.user import UsersManager
from lib.app.service.exposer import ExposerService


class App:

    def __init__(self):
        Logger.log_info(msg="App init...", is_verbose=True)

        # run project manager
        self.project_manager = ProjectManager()

        self.verbose = self.project_manager.settings.verbose
        self.frontend_start = self.project_manager.settings.frontend_start
        self.frontend_port = self.project_manager.settings.port

        # init Eel
        Logger.log_info(msg="Init frontend with Eel", is_verbose=self.verbose)
        eel.init(self.project_manager.settings.frontend_directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])  # init eel

        # expose methods
        exposer = ExposerService(self.project_manager.db_manager, self.project_manager.settings.vault_path, verbose=self.verbose)
        exposer.expose_methods()

    def start(self):

        eel.start(self.frontend_start, port=self.frontend_port, shutdown_delay=600)  # start eel: this generates a loop

        Logger.log_info(msg="Close app...", is_verbose=True)
