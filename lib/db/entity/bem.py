from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Dict, Any, Type, TypeVar
from lib.mixin.dcparser import DCToDictMixin, DCModifyMixin


EntityModel = TypeVar('EntityModel', bound='BaseEntityModel')  # Entity Model


@dataclass
class BaseEntityModel(DCToDictMixin, DCModifyMixin, ABC):
    """
    Provide a base model for entity dataclass
    """

    id: int

    @classmethod
    def from_dict(cls, data: dict) -> EntityModel:
        """
        Factory of BEM from dict data

        :param data: dict data of entity
        :type data: dict

        :return: BEM class
        :rtype BEM:
        """

        return cls(**data)

    # Uncomment this method to have a from_dict method with field check
    #
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
    def from_tuple(cls, data: tuple) -> EntityModel:
        """
        Factory of BEM from tuple data

        :param data: tuple data of entity
        :type data: tuple

        :return: BEM class
        :rtype BEM:
        """

        return cls(*data)
