from typing import List, Tuple, TypeVar, Generic, Any

T = TypeVar('T')


class CollectionsUtils:

    @staticmethod
    def first(collection: List | Tuple) -> Any | None:
        if not isinstance(collection, list) or not isinstance(collection, tuple):
            raise TypeError(f"{collection} must be a list or tuple")

        if len(collection) > 0:
            return collection[0]

        return None

    @staticmethod
    def first_or_fail(collection: List | Tuple) -> Any | None:
        if not isinstance(collection, list) or not isinstance(collection, tuple):
            raise TypeError(f"{collection} must be a list or tuple")

        if len(collection) > 0:
            return collection[0]

        raise ValueError(f"{collection} must have almost a value")
