from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Dict, Any, TypeVar, Tuple, List
from lib.mixin.dcparser import DCToDictMixin
from lib.mixin.classutil import ModifyMixin, AppendAttrMixin
from lib.utils.pair import PairAttrValue


EntityModel = TypeVar('EntityModel', bound='BaseEntityModel')  # Entity Model


@dataclass
class BaseEntityModel(DCToDictMixin, ModifyMixin, AppendAttrMixin, ABC):
    """
    Provide a base model for entity dataclass
    """

    id: int

    @classmethod
    def from_dict(cls, data: Dict, *append: PairAttrValue | Tuple) -> EntityModel:
        """
        Factory of BEM from dict data

        :param data: dict data of entity
        :type data: Dict

        :param append: data to append on entity
        :type append: PairAttrValue | Tuple

        :return: BEM class
        :rtype BEM:
        """

        entity = cls(**data)

        if len(append) > 0:
            entity.append_attr_from_list(append)

        return entity

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
    def from_tuple(cls, data: Tuple, *append: PairAttrValue | Tuple) -> EntityModel:
        """
        Factory of BEM from tuple data

        :param data: tuple data of entity
        :type data: Tuple

        :param append: data to append on entity
        :type append: PairAttrValue | Tuple

        :return: BEM class
        :rtype BEM:
        """

        entity = cls(*data)

        if len(append) > 0:
            entity.append_attr_from_list(append)

        return entity

    @classmethod
    def all_from_tuples(cls, data: List[Tuple]) -> List[EntityModel]:
        models = []

        for element in data:
            models.append(cls.from_tuple(element))

        return models

    @classmethod
    def all_from_dicts(cls, data: List[Dict]) -> List[EntityModel]:
        models = []

        for element in data:
            models.append(cls.from_dict(element))

        return models
