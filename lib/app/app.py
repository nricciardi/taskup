import eel
from lib.settings.settings import SettingsManager
from abc import ABC
from lib.utils.base import Base
from lib.app.project import ProjectManager


class Exposer(ABC):
    """
    Class to expose py method to js

    """

    def __init__(self, verbose: bool = False):
        self.__verbose = verbose

    def test(self, *args, **kwargs):
        """
        Method to test connection with frontend

        :param p:
        :return:
        """

        Base.log_eel(msg="Called by JS", is_verbose=self.__verbose)

        return args, kwargs

    def expose(self) -> None:
        """
        Expose py method.
        Modify it to expose new methods

        :rtype None:
        """

        Base.log_info(msg="Expose py methods...", is_verbose=self.__verbose, end=" ")

        eel.expose(self.test)

        Base.log_success(msg="OK", is_verbose=self.__verbose, prefix=False)


class App(Exposer):

    __settings_manager = SettingsManager()

    def __init__(self):
        self.__verbose = self.__settings_manager.verbose()

        Base.log_info(msg="App init...", is_verbose=self.__verbose)

        frontend_directory = self.__settings_manager.frontend_directory()
        eel.init(frontend_directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])

        super().__init__(self.__verbose)

        self.expose()

        self.__project_manager = ProjectManager()

    def start(self):

        start_file = self.__settings_manager.frontend_start()
        port = self.__settings_manager.port()

        eel.start(start_file, port=port)        # this generates a loop
