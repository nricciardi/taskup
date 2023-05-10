import eel
from lib.utils.logger import Logger
from lib.app.project import ProjectManager
from lib.app.service.exposer import ExposerService
from lib.utils.demo import Demo
from lib.utils.utils import Utils
from lib.settings.settings import SettingsManager


class AppManager:

    VERSION: str = "1.0.0"
    SHUTDOWN_DELAY = 600

    def __init__(self):
        Logger.log_info(msg="App init...", is_verbose=True)

        # instance settings manager to take project configuration settings
        Logger.log_info(msg="Take settings...", is_verbose=True)
        self.__settings_manager = SettingsManager()     # only one SettingsManager for each App

        self.verbose = self.settings_manager.verbose

        # each AppManager has only one ProjectManager
        self.project_manager = ProjectManager(settings_manager=self.settings_manager)

        self.open_project(self.settings_manager.project_directory_path)

        # init Eel
        Logger.log_info(msg="Init frontend with Eel", is_verbose=self.verbose)
        eel.init(self.settings_manager.frontend_directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])  # init eel

        # expose methods
        exposer = ExposerService(self, verbose=self.verbose)
        exposer.expose_methods()

    @property
    def settings_manager(self) -> SettingsManager:
        return self.__settings_manager

    def start(self) -> None:

        Logger.log_info(msg="Start app...", is_verbose=True)

        frontend_start = self.settings_manager.frontend_start
        frontend_port = self.settings_manager.port

        eel.start(frontend_start, port=frontend_port, shutdown_delay=self.SHUTDOWN_DELAY)  # start eel: this generates a loop

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

        Utils.open_in_webbrowser(self.settings_manager.settings_path())

    def version(self) -> str:
        """
        Return version

        :return:
        """

        return self.VERSION

    def open_project(self, path: str) -> bool:
        """
        Open project by path. Set current project path based on path passed (and can refresh)

        :return:
        """

        try:

            if not self.project_manager.check_project_path(path=path, force_exit=False):
                Logger.log_error(msg=f"project '{path}' not initialized", is_verbose=self.verbose)
                return False

            res = self.settings_manager.set_project_path(path)      # set path of project which must be opened

            if res is False:
                return False

            self.project_manager.refresh()      # refresh project managed by ProjectManager instance

            Logger.log_info(msg=f"'{path}' project opened", is_verbose=self.verbose)
            return True

        except Exception as e:

            Logger.log_error(msg=f"{e}", full=True, is_verbose=self.verbose)

            return False
