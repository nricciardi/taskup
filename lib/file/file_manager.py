import json
from typing import Any


class FileManger:

    @staticmethod
    def read_json(path: str) -> Any:
        """
        Return the content of a JSON file

        :param path: file path
        :type path: str
        :return: file content
        :rtype: Any
        """
        with open(path, "r") as file:
            return json.load(file)

    @staticmethod
    def write_json(path: str, data: Any) -> None:
        """
        Write body in the JSON file

        :param path: file path
        :param data: data to write
        """
        with open(path, "w") as file:
            file.write(json.dumps(data))
