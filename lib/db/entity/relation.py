from dataclasses import dataclass, field
from typing import Type, TypeVar, Generic
from lib.db.entity.bem import EntityModel, BaseEntityModel
from abc import ABC

Pivot = TypeVar('Pivot', bound=BaseEntityModel)     # pivot

@dataclass
class Relation(ABC, Generic[EntityModel]):
    """

    :ivar has: relation type
    :type has: RelationType
    
    :ivar fk_model: fk dataclass
    :type fk_model: str

    :ivar of_table: relation table
    :type of_table: str



    :ivar to_attr: dataclass type
    :type to_attr: [EntityModel]
    """

    fk_model: Type[EntityModel]
    of_table: str
    to_attr: str


@dataclass
class OneRelation(Relation):
    """

    :ivar fk_field: fk field in entity
    :type fk_field: str

    """

    fk_field: str


@dataclass
class ManyRelation(Relation):
    """

    """

    pivot_table: str
    pivot_model: Type[Pivot]

    def __post_init__(self) -> None:
        if self.pivot_model == self.fk_model:
            raise ValueError("a and b must be different types")
