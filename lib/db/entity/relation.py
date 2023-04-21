from dataclasses import dataclass, field
from typing import Type, TypeVar, Generic, List, Optional
from lib.db.entity.bem import EntityModel, BaseEntityModel
from abc import ABC

Pivot = TypeVar('Pivot', bound=BaseEntityModel)     # pivot

@dataclass
class Relation(ABC, Generic[EntityModel]):
    """
    
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

    :ivar pivot_table: the pivot table
    :ivar pivot_model: model which represents pivot records

    """

    pivot_table: str
    pivot_model: Type[Pivot]

    def __post_init__(self) -> None:
        if self.pivot_model == self.fk_model:
            raise ValueError("a and b must be different types")


@dataclass
class ExtendedManyRelation(ManyRelation):
    """
    :ivar other_cols: other columns to add
    :ivar fk_col: column's name of fk
    :ivar wrap_fk_model: model which wraps relations
    """

    other_cols: List[str]
    fk_col: str
    wrap_fk_model: Type[dataclass]
