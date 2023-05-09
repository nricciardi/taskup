import eel
from lib.settings.settings import SettingsManager
from lib.utils.logger import Logger
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager
from lib.db.entity.user import UsersManager
from lib.app.service.exposer import ExposerService
from lib.utils.demo import Demo
from lib.utils.utils import Utils


class AppManager:

    VERSION: str = "1.0.0"

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
        exposer = ExposerService(self, verbose=self.verbose)
        exposer.expose_methods()

    def start(self) -> None:

        Logger.log_info(msg="Start app...", is_verbose=True)

        eel.start(self.frontend_start, port=self.frontend_port, shutdown_delay=600)  # start eel: this generates a loop

        Logger.log_info(msg="Close app...", is_verbose=True)

    @classmethod
    def demo(cls, force_demo: bool = False, verbose: bool = False) -> None:
        """
        Launch demo of app

        :param force_demo:
        :param verbose:
        :return:
        """

        demo = Demo()

        demo.launch(force_demo=force_demo)

        cls().start()   # launch app

    def open_settings(self) -> None:
        """
        Open settings file

        :return:
        """

        Utils.open_in_webbrowser(self.project_manager.settings.settings_path())

    def version(self) -> str:
        """
        Return version

        :return:
        """

        return self.VERSION

    def open_project(self, path: str, refresh_current: bool = True) -> bool:
        """
        Set current project path based on path passed (and can refresh)

        :return:
        """

        try:
            res = self.project_manager.settings.set_project_path(path)

            if res is False:
                return False

            if refresh_current:
                self.project_manager.refresh()

            return True

        except Exception as e:

            Logger.log_error(msg=f"{e}", full=True, is_verbose=self.verbose)

            return False
