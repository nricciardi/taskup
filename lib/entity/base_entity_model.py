from abc import ABC
from dataclasses import asdict, dataclass
from typing import Dict, Any, Type, TypeVar

T = TypeVar('T', bound='BaseEntityModel')

@dataclass
class BaseEntityModel(ABC):
    """
    Provide a base model method for entity dataclass

    """

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
