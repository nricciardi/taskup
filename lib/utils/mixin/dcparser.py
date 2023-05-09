from abc import ABC
from dataclasses import asdict, dataclass, astuple
from typing import Dict, Tuple, List, Any, Generic, TypeVar, Callable
from lib.utils.logger import Logger


def to_dict(method: Callable, verbose: bool = False):
    """
    Decorator to call 'to_dict' on EntityModel

    :param method: method which return an object with method "to_dict"
    :type method: Callable
    :param verbose: if verbose
    :type verbose: bool
    :return:
    """

    def wrapper(*args, **kwargs):
        res = method(*args, **kwargs)

        def apply(item) -> Dict:
            if hasattr(item, "to_dict"):
                return item.to_dict()

            return item

        if isinstance(res, list):
            data_to_dict = []
            for i in range(len(res)):
                data_to_dict.append(apply(res[i]))

        else:
            data_to_dict = apply(res)

        Logger.log(msg=f"convert data to_dict: {data_to_dict}", is_verbose=verbose, truncate=250)

        return data_to_dict

    return wrapper


@dataclass
class DCToDictMixin(ABC):

    def to_dict(self) -> Dict[str, Any]:
        entity_as_dict = asdict(self)

        return entity_as_dict


@dataclass
class DCToTupleMixin(ABC):

    def to_tuple(self) -> Tuple[Any]:
        entity_as_tuple = astuple(self)

        return entity_as_tuple


