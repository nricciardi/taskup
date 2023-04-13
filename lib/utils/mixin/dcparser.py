from abc import ABC
from dataclasses import asdict, dataclass, astuple
from typing import Dict, Tuple, List, Any, Generic, TypeVar, Callable


def to_dict(method: Callable):
    """
    Decorator to call 'to_dict' on EntityModel

    :param method:
    :return:
    """

    def wrapper(*args, **kwargs):
        res = method(*args, **kwargs)

        if hasattr(res, "to_dict"):
            return res.to_dict()

        return None

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


