from abc import ABC
from dataclasses import asdict, dataclass, astuple
from typing import Dict, Tuple, List, Any, Generic, TypeVar


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


