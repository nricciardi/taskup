from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any
from lib.mixin.sql import ToSqlInterface
from lib.mixin.dcparser import DCToDictMixin, DCToTupleMixin


@dataclass
class WhereCondition(DCToDictMixin, DCToTupleMixin):
    col: str
    operator: str
    value: str
    of_table: str | None = field(default=None)


@dataclass
class Field(ToSqlInterface):
    name: str
    type: str
    default: str | None = field(default=None)
    pk: bool = field(default=False)
    autoincrement: bool = field(default=False)
    unique: bool = field(default=False)
    nullable: bool = field(default=False)
    check: str | None = field(default=None)

    @classmethod
    def id_field(cls) -> 'Field':
        return cls(name="id", type="INTEGER", pk=True, autoincrement=True)

    @classmethod
    def fk_field(cls, name: str, nullable: bool = False, unique: bool = False) -> 'Field':
        return cls(name=name, type="INTEGER", nullable=nullable, unique=unique)

    @classmethod
    def name_field(cls, unique: bool = True) -> 'Field':
        return cls(name="name", type="VARCHAR(150)", nullable=False, unique=unique)

    @classmethod
    def description_field(cls, nullable: bool = False) -> 'Field':
        return cls(name="description", type="VARCHAR(1000)", nullable=nullable, unique=False)

    @classmethod
    def created_at_field(cls) -> 'Field':
        return cls(name="created_at", type="DATETIME", default="strftime('%Y-%m-%d %H:%M:%S', 'now')")

    @classmethod
    def updated_at_field(cls) -> 'Field':
        return cls(name="updated_at", type="DATETIME", default="strftime('%Y-%m-%d %H:%M:%S', 'now')")

    @classmethod
    def nullable_date_with_now_check_field(cls, name: str, default: str | None = 'NULL') -> 'Field':
        return cls(name=name, type="DATE", default=default, nullable=True,
                   check=f"{name} IS NULL OR {Field.get_date_sql(name)} > {Field.get_date_sql('now', strict_string=True)}")

    @staticmethod
    def get_datetime_sql(datetime: str, strict_string: bool = False, use_localtime: bool = False) -> str:
        return f"""strftime('%Y-%m-%d %H:%M:%S', {"'" if strict_string else ""}{datetime}{", 'localtime'" if use_localtime else ""}{"'" if strict_string else ""})"""

    @staticmethod
    def get_date_sql(date: str, strict_string: bool = False, use_localtime: bool = False) -> str:
        return f"""strftime('%Y-%m-%d', {"'" if strict_string else ""}{date}{", 'localtime'" if use_localtime else ""}{"'" if strict_string else ""})"""

    def to_sql(self) -> str:
        """
        Get sql string for table

        :return: SQL
        :rtype str:
        """

        return f"{self.name} {self.type} {'DEFAULT (' + self.default + ')' if self.default is not None else ''} " + \
            f"{'UNIQUE' if self.unique else ''} {'PRIMARY KEY' if self.pk else ''} {'AUTOINCREMENT' if self.autoincrement else ''} " + \
            f"{'NULL' if self.nullable and not self.pk else 'NOT NULL'}"


@dataclass
class FKConstraint(ToSqlInterface):
    fk_field: str
    on_table: str
    reference_field: str

    @classmethod
    def on_id(cls, fk_field: str, on_table: str) -> 'FKConstraint':
        return cls(fk_field=fk_field, on_table=on_table, reference_field='id')

    def to_sql(self) -> str:
        """
        Get sql strin for FK constraint

        :return: SQL
        :rtype str:
        """

        return f"Foreign Key ({self.fk_field}) References {self.on_table}({self.reference_field})"


@dataclass
class Table(ToSqlInterface):
    name: str
    fields: List[Field]
    fk_constraints: List[FKConstraint] = field(default=None)

    def has_fk_constraint(self) -> bool:
        return self.fk_constraints is not None and len(self.fk_constraints) > 0

    @classmethod
    def pivot(cls, table_name: str, tables: List[str]) -> 'Table':
        fields = [
            Field.id_field()
        ]

        fk_constraints = []

        for t in tables:
            name = f"{t}_id"

            fields.append(Field.fk_field(name=name))
            fk_constraints.append(FKConstraint.on_id(name, t))

        return cls(table_name, fields, fk_constraints)

    def to_sql(self, if_not_exist: bool = True) -> str:
        """
        Get sql string to create table

        :return: SQL
        :rtype str:
        """

        fields = ',\n'.join(f.to_sql() for f in self.fields)

        return f"""Create Table {'If Not Exists' if if_not_exist else ''} {self.name} (
            {fields}

            {"," + ','.join(fk.to_sql() for fk in self.fk_constraints) if self.has_fk_constraint() else "" if self.has_fk_constraint() else ""}
        );
        """


@dataclass
class Seeder:
    table: str
    values: List[Tuple | Dict]
    fields: List | None = None


@dataclass
class DBStructure:
    name: str
    tables: List[Table]
    use_localtime: bool = False
