from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Dict, Any, Type, TypeVar

BEM = TypeVar('BEM', bound='BaseEntityModel')

@dataclass
class BaseEntityModel(ABC):
    """
    Provide a base model method for entity dataclass
    """

    id: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def update(self, new: dict) -> None:
        """
        Update fields from dict

        :param new: new data
        :type new: dict

        :return: None
        """

        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def from_dict(cls, data: dict) -> BEM:
        """
        Factory of BEM from dict data

        :param data: dict data of entity
        :type data: dict

        :return: BEM class
        :rtype BEM:
        """

        return cls(**data)

    # @classmethod
    # def from_dict_safe(cls, data: Dict[str, Any]) -> BEM:
    #     obj = cls.__new__(cls)
    #     for name, field in cls.__dataclass_fields__.items():
    #         value = data.get(name)
    #         if value is not None:
    #             setattr(obj, name, value)
    #         elif not field.init:
    #             setattr(obj, name, field.default)
    #         else:
    #             raise ValueError(f"Missing value for required field {name}")
    #     return obj

    @classmethod
    def from_tuple(cls, data: tuple) -> BEM:
        """
        Factory of BEM from tuple data

        :param data: tuple data of entity
        :type data: tuple

        :return: BEM class
        :rtype BEM:
        """

        return cls(*data)



