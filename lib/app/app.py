import eel
from typing import List, Dict, Any
from lib.app.service.auth import AuthService
from lib.app.service.dashboard import DashboardService
from lib.db.entity.user import FuturePMData
from lib.utils.logger import Logger
from lib.app.service.project import ProjectManager
from lib.app.service.exposer import ExposerService
from lib.app.service.demo import Demo
from lib.utils.utils import Utils
from lib.settings.settings import SettingsManager
from lib.utils.constants import PM_EMAIL, PM_USERNAME


class AppManager:

    APP_NAME: str = "Taskup"
    VERSION: str = "1.2.1"
    SHUTDOWN_DELAY = 3                  # seconds
    SHUTDOWN_DELAY_IN_DEBUG_MODE = 600  # seconds

    def __init__(self):
        Logger.log_info(msg=f"{self.APP_NAME} init...", is_verbose=True)

        # instance settings manager to take project configuration settings
        Logger.log_info(msg="take settings...", is_verbose=True)
        self.__settings_manager = SettingsManager()     # only one SettingsManager for each App

        self.verbose = self.settings_manager.verbose

        # each AppManager has only one ProjectManager
        self.project_manager = ProjectManager(settings_manager=self.settings_manager)

        self.auth_service = AuthService(users_manager=self.project_manager.users_manager,
                                        vault_path=self.settings_manager.vault_path,
                                        verbose=self.verbose)

        self.dashboard_service = DashboardService(tasks_manager=self.project_manager.tasks_manager,
                                                  task_status_manager=self.project_manager.task_status_manager,
                                                  auth_service=self.auth_service,
                                                  roles_manager=self.project_manager.roles_manager,
                                                  verbose=self.verbose)

        # open project if already initialized
        if ProjectManager.already_initialized(self.settings_manager.project_directory_path):
            self.open_project(self.settings_manager.project_directory_path)

        self.__expose()     # expose py methods

        # init Eel
        frontend_dir = self.settings_manager.frontend_directory

        Logger.log_info(msg=f"init frontend '{frontend_dir}'@{self.settings_manager.frontend_start}", is_verbose=self.verbose)
        eel.init(frontend_dir, allowed_extensions=['.html'])  # init eel

    @classmethod
    def starter(cls) -> 'AppManager':
        """
        Start application using default parameters

        :return: application instance
        :rtype AppManager:
        """

        app = cls()
        app.start()

        return app

    def start(self) -> None:
        """
        Start GUI using eel.start()

        :return:
        :rtype None:
        """

        # pick frontend entry and port from settings
        frontend_start = self.settings_manager.frontend_start
        port = self.settings_manager.port

        # set shutdown delay based on debug mode
        shutdown_delay = self.SHUTDOWN_DELAY

        if self.settings_manager.debug_mode:
            Logger.log_warning(msg="app will be launched in debug-mode", is_verbose=self.verbose)
            shutdown_delay = self.SHUTDOWN_DELAY_IN_DEBUG_MODE

        mode = self.settings_manager.get_setting_by_key(self.settings_manager.KEY_APP_MODE)     # pick mode from settings

        try:
            Logger.log_info(msg=f"start app... (mode: {mode})", is_verbose=self.verbose)

            eel.start(frontend_start, port=port, shutdown_delay=shutdown_delay, mode=mode,
                      cmdline_args=["--disable-translate"])  # start eel: this generates a loop

        except KeyboardInterrupt:
            Logger.log_custom(msg="KeyboardInterrupt is handled", is_verbose=self.verbose)

        # insert here all instructions to run before end
        finally:
            self.close()        # close app manually

    @classmethod
    def demo(cls, project_path: str, force_demo: bool = False, open_app_at_end: bool = True, verbose: bool = False) -> None:
        """
        Launch demo of app

        :param open_app_at_end:
        :param project_path:
        :param force_demo:
        :param verbose:
        :return:
        """

        demo = Demo(project_path=project_path, settings_manager=SettingsManager(), verbose=verbose)

        demo.launch(force_demo=force_demo)

        if open_app_at_end:
            AppManager.starter()    # launch app

    @property
    def settings_manager(self) -> SettingsManager:
        return self.__settings_manager

    def __ng_serve(self) -> None:
        """
        Run ng serve in frontend

        :return:
        """

        try:
            import subprocess

            command = "ng serve"

            subprocess.Popen(command, shell=True, cwd=self.settings_manager.frontend_directory)

        except Exception as e:
            pass

    def __expose(self) -> None:
        """
        Expose methods using Eel

        :return:
        """

        try:
            # expose all app's methods with "app_" prefix
            ExposerService.expose_all_from_list(to_expose=[
                self.open_settings,
                self.version,
                self.open_project,
                self.close,
                self.init_project,
                self.get_projects_paths_stored,
                self.remove_work_dir,
                self.settings_manager.get_settings,
                self.settings_manager.update_settings
            ], prefix="app_")

        except Exception as excepetion:
            Logger.log_error(msg="app exposure error", is_verbose=self.verbose, full=True)

        # expose methods
        exposer = ExposerService(self.project_manager, auth_service=self.auth_service, dashboard_service=self.dashboard_service,
                                 verbose=self.verbose, debug_mode=self.settings_manager.debug_mode)
        exposer.expose_methods()

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

        return self.project_manager.open(path)

    @classmethod
    def initializer(cls, project_path: str, open_on_init: bool = False, force_init: bool = False) -> 'AppManager':
        """
        Initializer method

        :param project_path:
        :param open_on_init:
        :param force_init:
        :return: instance of app
        :rtype AppManager:
        """

        pm_data = FuturePMData(username=PM_USERNAME, email=PM_EMAIL, password=Utils.generate_psw())

        app = cls()
        app.init_project(path=project_path, future_pm_data=pm_data, open_on_init=open_on_init, force_init=force_init)

        Logger.log_custom(msg=f"Project manager credentials:\nemail: {Demo.pm_email}\npassword: {Demo.pm_password}",
                          is_verbose=True, capitalize=False)

        return app

    def init_project(self, path: str, future_pm_data: FuturePMData, open_on_init: bool = False, force_init: bool = False) -> bool:
        """
        Initialized a new project in path with pm as project manager

        :param open_on_init:
        :param force_init: flag which indicates if overwrite previously init
        :param path:
        :param future_pm_data:
        :return:
        """

        # verify if there are all required values
        required_values = ["email", "username", "password"]
        for required in required_values:
            if required not in future_pm_data.keys():
                Logger.log_error(msg=f"invalid pm data ({future_pm_data}): {required} is required", is_verbose=self.verbose)

                return False

        res: bool = self.project_manager.init_new(path, future_pm_data, force_init=force_init)

        if open_on_init:
            self.open_project(path)

        return res

    def close(self) -> None:
        """
        Close app

        :return:
        """

        try:
            Logger.log_info(msg="request to close app...", is_verbose=self.verbose)

            self.project_manager.backup_work_dir()

        except Exception:
            pass

    def get_projects_paths_stored(self) -> List[str]:
        """
        Get all projects paths stored

        :return: projects paths
        """

        paths_stored: List[str] = self.__settings_manager.projects_paths_stored

        return paths_stored

    def remove_work_dir(self) -> bool:
        """
        Remove work directory from current project opened

        :return:
        """

        res = self.project_manager.remove(self.settings_manager.project_directory_path)

        self.auth_service.logout()

        return res
