from dataclasses import dataclass
from lib.db.query import QueryBuilder
from lib.utils.mixin.sql import ToSqlInterface
from typing import List, Tuple, Dict, Any, Optional, TypeVar


@dataclass
class Seeder(ToSqlInterface):
    table: str
    values: List[Tuple | List]
    cols: Optional[Tuple | List] = None

    def to_sql(self, verbose: bool = False) -> str:
        return QueryBuilder.from_table(self.table).insert_from_tuple(*self.values, columns=self.cols).to_sql(verbose)
