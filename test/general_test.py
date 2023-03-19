from lib.settings.settings_manager import SettingsManager
from lib.utils.base import Base


class Punto:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 1


if __name__ == '__main__':

    p = Punto()

    print(p.z)
