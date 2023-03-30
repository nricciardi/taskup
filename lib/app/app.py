import eel
from lib.settings.settings import SettingsManager


class App:

    __settings_manager = SettingsManager()

    def __init__(self):

        frontend_directory = self.__settings_manager.frontend_directory()
        eel.init(frontend_directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])

    def start(self):

        start_file = self.__settings_manager.frontend_start()
        port = self.__settings_manager.port()

        eel.start(start_file, port=port)        # this generates a loop
