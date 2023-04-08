from enum import Enum
from dataclasses import dataclass
from typing import Type
from lib.db.entity.bem import EntityModel


class RelationCardinality(Enum):
    MANY = "many"
    ONE = "one"


@dataclass
class Relation:
    """


    :ivar has: relation type
    :type has: RelationType
    
    :ivar fk_EM: fk dataclass
    :type fk_EM: str

    :ivar in_table: relation table
    :type in_table: str

    :ivar fk_field: fk field in entity
    :type fk_field: str

    :ivar to_attr: dataclass type
    :type to_attr: [EntityModel]
    """

    has: RelationCardinality
    fk_EM: Type[EntityModel]
    in_table: str
    fk_field: str
    to_attr: str

