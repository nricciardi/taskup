from typing import List, Tuple, TypeVar, Generic, Any, Dict

T = TypeVar('T')


class ListUtils:

    @staticmethod
    def first(collection: List | Tuple) -> Any | None:
        """
        Get first element of a list/tuple if it isn't empty, else None

        :param collection:
        :return:
        """

        if not isinstance(collection, list) and not isinstance(collection, tuple):
            msg = f"{collection} must be a list or tuple, but {type(collection)} given"
            raise TypeError(msg)

        if len(collection) > 0:
            return collection[0]

        return None

    @staticmethod
    def first_or_fail(collection: List | Tuple) -> Any | None:
        """
        Get first element of a list/tuple if it isn't empty, else throw an error

        :param collection:
        :return:
        """

        if not isinstance(collection, list) and not isinstance(collection, tuple):
            raise TypeError(f"{collection} must be a list or tuple")

        if len(collection) > 0:
            return collection[0]

        raise ValueError(f"{collection} must have almost a value")


class DictUtils:
    @staticmethod
    def filter_dict_by_key(d: Dict, keys: Tuple[str] | List[str]) -> Dict:
        """
        Return a new dictionary from passed dict with only the keys are indicated

        :param d:
        :param keys:
        :return:
        """

        return {key: value for key, value in d.items() if key in keys}
