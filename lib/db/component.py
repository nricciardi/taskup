from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any, Optional, TypeVar
from lib.utils.mixin.dcparser import DCToDictMixin, DCToTupleMixin
from lib.utils.mixin.sql import ToSqlInterface
from lib.utils.utils import SqlUtils


@dataclass
class WhereCondition(DCToDictMixin, DCToTupleMixin):
    col: str
    operator: str
    value: Any
    of_table: str | None = field(default=None)


@dataclass
class Trigger(ToSqlInterface):

    name: str
    on_action: str
    script: str
    temporary: bool = field(default=False)
    if_not_exists: bool = field(default=True)

    def to_sql(self) -> str:

        query = f"""
        Create Trigger{'Temporary ' if self.temporary else ' '}{'If Not Exists ' if self.if_not_exists else ' '}{self.name}
        {self.on_action}
        Begin
            {self.script};
        End;
        """

        return query


@dataclass
class Field(ToSqlInterface):
    name: str
    type: str
    default: Optional[str] = field(default=None)
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
    def description_field(cls, nullable: bool = True) -> 'Field':
        return cls(name="description", type="VARCHAR(1000)", nullable=nullable, unique=False)

    @classmethod
    def created_at_field(cls) -> 'Field':
        return Field.datetime_now("created_at")

    @classmethod
    def updated_at_field(cls) -> 'Field':
        return Field.datetime_now("updated_at")

    @classmethod
    def datetime_now(cls, name: str, use_localtime: bool = False) -> 'Field':
        return cls(name=name, type="DATETIME", default=SqlUtils.datetime_strf_now(use_localtime))

    @classmethod
    def nullable_date_with_now_check_field(cls, name: str, default: str | None = 'NULL', use_localtime: bool = False) -> 'Field':
        return cls(name=name, type="DATE", default=default, nullable=True,
                   check=f"{name} IS NULL OR {SqlUtils.date_str_format(name, use_localtime=use_localtime)} > {SqlUtils.date_strf_now(use_localtime=use_localtime)}")

    @classmethod
    def nullable_datetime_with_now_check_field(cls, name: str, default: str | None = 'NULL', use_localtime: bool = False) -> 'Field':
        return cls(name=name, type="DATETIME", default=default, nullable=True,
                   check=f"{name} IS NULL OR {SqlUtils.datetime_str_format(name, use_localtime=use_localtime)} > {SqlUtils.datetime_strf_now(use_localtime=use_localtime)}")

    @classmethod
    def hex_color(cls, name: str = "hex_color", nullable: bool = False, default: Optional[str] = None):
        return cls(name=name, type="VARCHAR(7)", nullable=nullable, default=default)     # 7 because it includes '#' of html typical hex color

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
class RawSql(ToSqlInterface):

    sql: str

    def to_sql(self) -> str:
        return self.sql


@dataclass
class FKConstraint(ToSqlInterface):
    fk_field: str
    on_table: str
    reference_field: str
    on_update: Optional[str] = field(default=None)
    on_delete: Optional[str] = field(default=None)

    @classmethod
    def on_id(cls, fk_field: str, on_table: str, on_update: Optional[str] = None, on_delete: Optional[str] = None) -> 'FKConstraint':
        return cls(fk_field=fk_field, on_table=on_table, reference_field='id', on_update=on_update, on_delete=on_delete)

    def to_sql(self) -> str:
        """
        Get sql string for FK constraint

        :return: SQL
        :rtype str:
        """

        query = f"Foreign Key ({self.fk_field}) References {self.on_table}({self.reference_field})"

        if self.on_update is not None:
            query += f" On Update {self.on_update}"

        if self.on_delete is not None:
            query += f" On Update {self.on_delete}"

        return query


@dataclass
class UniqueConstraint(ToSqlInterface):
    cols: List[str]

    def to_sql(self) -> str:
        """
        Get sql string for UNIQUE constraint

        :return: SQL
        :rtype str:
        """

        return f"UNIQUE({', '.join(self.cols)})"


Constraint = TypeVar('Constraint', FKConstraint, UniqueConstraint)


@dataclass
class Table(ToSqlInterface):
    name: str
    fields: List[Field]
    fk_constraints: Optional[List[FKConstraint]] = field(default=None)
    other_constraints: Optional[List[Constraint]] = field(default=None)
    with_triggers: Optional[List[Trigger] | Trigger] = field(default=None)

    def has_fk_constraints(self) -> bool:
        return self.fk_constraints is not None and len(self.fk_constraints) > 0

    def has_other_constraints(self) -> bool:
        return self.other_constraints is not None and len(self.other_constraints) > 0

    @classmethod
    def pivot(cls, table_name: str, tables: List[str], other_fields: List[Field] | None = None,
              other_constraints: List[Constraint] | None = None, unique_record: bool = False, with_triggers: List[Trigger] | Trigger | None = None) -> 'Table':

        fields = [Field.id_field()]

        if other_fields is not None:
            fields.extend(other_fields)

        fk_constraints = []

        names = []
        for t in tables:
            name = f"{t}_id"
            names.append(name)

            fields.append(Field.fk_field(name=name))
            fk_constraints.append(FKConstraint.on_id(name, t))

        if unique_record:

            if other_constraints is None:
                other_constraints = []

            other_constraints.append(UniqueConstraint(names))

        return cls(table_name, fields, fk_constraints, other_constraints=other_constraints, with_triggers=with_triggers)

    def to_sql(self, if_not_exist: bool = True) -> str:
        """
        Get sql string to create table

        :return: SQL
        :rtype str:
        """

        fields = ',\n'.join(f.to_sql() for f in self.fields)

        table = f"""Create Table {'If Not Exists' if if_not_exist else ''} {self.name} (
            {fields}

            {"," + ','.join(fk.to_sql() for fk in self.fk_constraints) if self.has_fk_constraints() else ""}
            {"," + ','.join(constraint.to_sql() for constraint in self.other_constraints) if self.has_other_constraints() else ""}
        );
        """

        if self.with_triggers is not None:
            # append triggers

            if isinstance(self.with_triggers, Trigger):
                self.with_triggers = [self.with_triggers]       # cast to list

            table += "\n".join(trigger.to_sql() for trigger in self.with_triggers)

        return table

    @property
    def fields_name(self) -> Tuple:
        """
        Return the tuple of fields names

        :return: fields name
        :rtype tuple:
        """

        return tuple(f.name for f in self.fields)


@dataclass
class DBStructure:
    name: str
    tables: List[Table]
    use_localtime: bool = False

