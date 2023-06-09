from lib.db.db import DBManager
from abc import ABC, abstractmethod
from lib.db.entity.relation import Relation, OneRelation, ManyRelation, ExtendedManyRelation
from lib.utils.logger import Logger
from lib.db.entity.bem import BaseEntityModel, EntityModel
from typing import Any, List, Dict, Type, Generic
from lib.db.query import QueryBuilder
from lib.db.component import WhereCondition
from lib.utils.pair import PairAttrValue


class EntitiesManager(ABC, Generic[EntityModel]):
    """
    Abstract class to manage DB's entities
    """

    db_use_localtime: bool = True

    def __init__(self, db_manager: DBManager, verbose: bool = False):
        self.__verbose = verbose

        self.__db_manager = db_manager

    @property
    def db_manager(self) -> DBManager:
        return self.__db_manager

    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self.__verbose = value

    @property
    def relations(self) -> list[Relation]:
        """
        Provide a list with all relations of entity

        :return: list of relations
        :rtype list:
        """

        return []

    @property
    @abstractmethod
    def table_name(self) -> str:
        """
        Return table name

        :rtype: str
        """

        raise NotImplementedError

    @property
    @abstractmethod
    def EM(self) -> Type[EntityModel]:
        """
        Generic reference of an EntityModel

        :return:
        """

        raise NotImplementedError

    def __is_valid_model_data_type(self, data: Any) -> bool:
        """
        Return True if data is a subclass of BaseEntityModel, otherwise False

        :param data: data to check
        :type data: Any

        :return: result of check
        :rtype bool:
        """

        return issubclass(data.__class__, BaseEntityModel)

    def __validate_model_data_type(self, data: Any):
        """
        Raise exception if param data is not a subclass of BaseEntityModel

        :param data: data to check
        :type data: Any

        :return:
        """

        if not self.__is_valid_model_data_type(data):
            msg = f"{data} must be an implementation of BaseEntityModel"

            Logger.log_error(msg=msg, is_verbose=self.__verbose)

            raise TypeError(msg)

    def all_as_dict(self, with_relations: bool = True) -> List[Dict[str, Any]]:
        """
        Return all entities as dict.

        :param with_relations: add entity data of relations
        :type with_relations: bool

        :return: all entities as dict
        :rtype List[Dict[str, Any]]:
        """

        dicts: List = self.__all_as_dict(self.table_name)

        if with_relations:
            for i in range(len(dicts)):
                em: EntityModel = self.EM.from_dict(dicts[i])
                self.append_relations_data_on(em, True)
                dicts[i] = em.to_dict()

        return dicts

    def __all_as_dict(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Actual method to get all entities data from database using a table name as list of dict

        :param table_name:
        :type table_name: str

        :return: all entities as dict
        :rtype List[Dict[str, Any]]:
        """

        query = QueryBuilder.from_table(table_name).select().to_sql()

        records = self.db_manager.cursor.execute(query).fetchall()

        return records

    def all_as_model(self, with_relations: bool = True, safe: bool = True) -> List[EntityModel]:
        """
        Return all entities as EntityModel.

        :param safe: safe execute flag
        :type safe: bool
        :param with_relations: add entity data of relations
        :type with_relations: bool

        :return: all entities as EntityModel
        :rtype List[EntityModel]:
        """

        models = self.__all_as_model(table_name=self.table_name, with_relations=with_relations, model=self.EM,
                                     safe=safe)

        Logger.log_info(msg=f"get {len(models)} entities from database")

        return models

    def __all_as_model(self, table_name: str, with_relations: bool, model: EntityModel, safe: bool) -> List[EntityModel]:

        tuples = self.__all_as_dict(table_name)

        models = model.all_from_dicts(tuples)

        if with_relations:
            for em in models:
                self.append_relations_data_on(em, safe)

        return models

    def find(self, entity_id: int, with_relations: bool = True, safe: bool = True) -> EntityModel | None:
        """
        Return the record requested

        :param safe: safe execution flag
        :type safe: bool
        :param with_relations: add entity data of relations
        :type with_relations: bool
        :param entity_id: the record's id
        :type entity_id: int

        :return: entity record
        :rtype EntityModel:
        """

        data: Dict = self.__find(entity_id, self.table_name)

        if data is None:
            return None

        em = self.EM.from_dict(data)    # create a new EntityModel from found data (dict)

        if with_relations:
            self.append_relations_data_on(em, safe=safe)

        return em

    def __find(self, entity_id: int, table_name: str) -> Dict | None:
        """
        Actual find method implementation.
        This method return a tuple because it can be used with different table, therefore it doesn't know any
        entity model.

        :param table_name:
        :type table_name: str

        :param entity_id: the record's id
        :type entity_id: int

        :return:
        :rtype Dict:
        """

        query = self.__get_find_query(entity_id, table_name)

        res = self.db_manager.cursor.execute(query)

        if res is None:
            return None

        data = res.fetchone()

        if data is None:
            return None

        return dict(data)

    def __get_find_query(self, entity_id: int, table_name: str) -> str:
        """
        Return the query for find an entity

        :param entity_id:
        :type entity_id: int

        :param table_name:
        :type table_name: str

        :return: the query
        :rtype: str
        """

        return QueryBuilder.from_table(table_name).select().where("id", "=", entity_id).to_sql()

    def create_from_dict(self, data: dict, safe: bool = True) -> EntityModel | None:
        """
        Create a new record

        :param data: dict represent entity data
        :type data: Entity dataclass

        :param safe: if True prevent fault
        :type safe: bool

        :return: entity created
        :rtype EntityModel:
        """

        try:

            self.db_manager.insert_from_dict(self.table_name, data)

            # find entity created to return its
            entity = self.find(self.db_manager.cursor.lastrowid)

            Logger.log_success(msg=f"created a new resource in {self.table_name} with data: {data}\nresult: {entity}", is_verbose=self.verbose)

            return entity

        except Exception as exception:

            Logger.log_error(msg=f"{exception} during inserting with data: {data}", is_verbose=self.__verbose)

            if not safe:
                raise exception

            return None

    def where_as_model(self, *conditions: WhereCondition, columns: List[str] | None = None, with_relations: bool = True, safe: bool = True) -> List[EntityModel]:
        """
        Filter entities based on conditions

        :param safe: flag for safe operation
        :type safe: bool
        :param with_relations:
        :type with_relations: bool
        :param columns: columns to get
        :type columns: List[str] | None
        :param conditions: list of conditions
        :type conditions: WhereCondition

        :return: list of entities
        :rtype List[EntityModel]:
        """

        try:
            result: List[Dict] = self.db_manager.where(self.table_name, *conditions, columns=columns)

            models = self.EM.all_from_dicts(result)

            if with_relations:
                for em in models:
                    self.append_relations_data_on(em, safe)

            return models

        except Exception as e:
            Logger.log_error(msg=f"error during 'where_as_model' using {conditions}", is_verbose=self.verbose)

            if not safe:
                raise e

    def filter(self, filters: Dict[str, str], operator: str = "=", with_relations: bool = True, safe: bool = True) -> List[EntityModel]:
        """
        Return entities filter by key-value

        :param operator:
        :param filters:
        :param with_relations:
        :param safe:
        :return:
        """

        operator = operator.lower()

        conditions: List[WhereCondition] = []

        for k, v in filters.items():
            if operator == "like":
                v = f"%{v}%"

            conditions.append(WhereCondition(k, operator, v))

        return self.where_as_model(*conditions, with_relations=with_relations, safe=safe)

    def check_already_used(self, field_name: str, value: Any) -> bool:
        """
        Check if the value passed is already used (where alias)

        :param field_name:
        :param value:
        :return:
        """

        return len(self.where_as_model(WhereCondition(col=field_name, operator="=", value=value),
                                       with_relations=False, safe=True)) > 0

    def append_relations_data_on(self, em: EntityModel, safe: bool) -> None:
        """
        Append relations data on entity passed

        :param em:
        :type em: EntityModel

        :param safe: flag to prevent crash if a relation is wrong
        :type safe: bool

        :return: None
        :rtype None:
        """

        em.append_attr_from_list_of_pair(self.get_all_relations_data_of(em, safe))

    def get_all_relations_data_of(self, em: EntityModel, safe: bool) -> List[PairAttrValue]:
        """
        Get all relations data of entity passed

        :param em:
        :type em: EntityModel

        :param safe: flag to prevent crash if a relation is wrong
        :type safe: bool

        :return: None
        :rtype None:
        """

        all_relations = []
        for relation in self.relations:
            data = self.get_relation_data_of(em, relation, safe)
            all_relations.append(PairAttrValue(attr=relation.to_attr, value=data))

        return all_relations

    def get_relation_data_of(self, em: EntityModel, relation: Relation, safe: bool) -> EntityModel | List[EntityModel] | None:
        """
        Return the entities in relation(s) with an entity

        :param safe: flag to prevent crash if a relation is wrong
        :type safe: bool

        :param relation:
        :type relation: Relation

        :param em: entity from get data
        :type em: EntityModel

        :return:
        :rtype EntityModel | list[EntityModel]:
        """

        try:

            # ==== OneRelation ====
            if isinstance(relation, OneRelation):
                return self.get_one_relation_data_of(em, relation)

            # ==== ExtendedManyRelation ====
            # ExtendedManyRelation is subclass of ManyRelation, the check have to be above
            elif isinstance(relation, ExtendedManyRelation):
                return self.get_extended_many_relation_data_based_on(em, relation)

            # ==== ManyRelation ====
            elif isinstance(relation, ManyRelation):
                return self.get_many_relation_data_based_on(em, relation)

            else:
                Logger.log_warning(msg=f"{relation} does not exist as relationship type", is_verbose=self.verbose)

        except Exception as exception:

            Logger.log_warning(msg=f"{relation} is wrong!\nUsing {em}\nBecause: {exception}")

            if not safe:
                raise exception

    def get_one_relation_data_of(self, em: EntityModel, relation: OneRelation) -> EntityModel | None:
        """
        Return data for a one relation

        :param relation:
        :type relation: Relation

        :param em: entity from get data
        :type em: EntityModel

        :return: entity
        :rtype EntityModel | None:
        """

        fk_id: int | None = getattr(em, relation.fk_field)  # get fk_id from em based on fk_field of relation

        if fk_id is None:
            return None

        data: Dict = self.__find(fk_id, relation.of_table)  # find fk entity

        return relation.fk_model.from_dict(data)  # return a fk EM from tuple resulted

    def get_many_relation_data_based_on(self, em: EntityModel, relation: ManyRelation) -> List[EntityModel] | None:
        """
        Return data for a many relation

        :param em: entity from get data
        :type em: EntityModel
        :param relation:
        :type relation: Relation

        :return: entities
        :rtype List[EntityModel] | None:
        """

        fk_pivot_col = relation.of_table + "_id"  # pivot col convention: <fk_table>_id
        entity_pivot_col = self.table_name + "_id"

        pivot_data: List[Dict] = self.db_manager.where(relation.pivot_table,
                                                       WhereCondition(
                                                             col=entity_pivot_col,
                                                             operator="=",
                                                             value=em.id
                                                         ))

        data: List[relation.fk_model] = []
        for pivot_record in pivot_data:     # for each pivot record append data to fk_record

            fk_record: Dict = self.__find(pivot_record[fk_pivot_col], relation.of_table)

            data.append(relation.fk_model.from_dict(fk_record))

        return data

    def get_extended_many_relation_data_based_on(self, em: EntityModel, relation: ExtendedManyRelation) -> List[EntityModel] | None:
        """
        Return data for an extended many relation

        :param em: entity from get data
        :type em: EntityModel
        :param relation:
        :type relation: Relation

        :return: entities
        :rtype List[EntityModel] | None:
        """

        fk_pivot_col = relation.of_table + "_id"  # pivot col convention: <fk_table>_id
        entity_pivot_col = self.table_name + "_id"

        pivot_data: List[Dict] = self.db_manager.where(relation.pivot_table,
                                                       WhereCondition(
                                                             col=entity_pivot_col,
                                                             operator="=",
                                                             value=em.id
                                                         ))

        data: List[relation.wrap_fk_model] = []
        for pivot_record in pivot_data:

            fk_record: Dict = self.__find(pivot_record[fk_pivot_col], relation.of_table)

            # generate values to initialize wrap model
            values = {
                relation.fk_col: relation.fk_model.from_dict(fk_record)
            }

            for oc in relation.other_cols:      # for each other cols update values with the pivot value
                values.update({
                    oc: pivot_record[oc]
                })

            # create wrap model
            wrap_model = relation.wrap_fk_model(**values)

            data.append(wrap_model)

        return data

    def delete(self, *conditions: WhereCondition, safe: bool = True) -> bool:
        """
        Delete entities data

        :param conditions:
        :param safe:
        :return:
        """

        try:
            Logger.log_info(msg=f"delete from {self.table_name} where {conditions}", is_verbose=self.verbose)

            self.__delete(self.table_name, *conditions)

            return True

        except Exception as exception:

            Logger.log_error(msg=exception, full=True, is_verbose=self.verbose)

            if not safe:
                raise exception

            return False

    def __delete(self, table_name: str, *conditions: WhereCondition):
        """
        Delete entities data based on specific table

        :param table_name:
        :param conditions:
        :return:
        """

        return self.db_manager.delete(table_name, *conditions)

    def delete_by_id(self, entity_id: int) -> bool:
        """
        Delete entity data by its id

        :param entity_id:
        :return:
        """

        try:
            # Logger.log_info(msg=f"delete from {self.table_name} where id={entity_id}", is_verbose=self.verbose)

            return self.delete(
                WhereCondition("id", "=", entity_id)
            )

        except Exception as e:
            Logger.log_error(msg=f"error occurs during deleting...")

            return False

    def update_from_dict(self, entity_id: int, data: Dict, safe: bool = True, create_if_not_exists: bool = True) -> EntityModel:
        """
        Update entity by id with key-value data and return updated entity as model

        :param create_if_not_exists: if entity_id is None, this method try to call create
        :param safe: call this method safely
        :param entity_id:
        :param data:
        :return:
        """

        try:

            Logger.log_info(msg=f"updating {self.table_name} with data: {data}", is_verbose=self.verbose)

            if entity_id is None and create_if_not_exists:
                Logger.log_warning(msg=f"it doesn't exist, so it will be created")

                entity_id = self.db_manager.insert_from_dict(self.table_name, data)

            else:

                self.db_manager.update(self.table_name, WhereCondition("id", "=", entity_id), **data)

                Logger.log_success(msg=f"Updated {self.table_name} where id = {entity_id}")

            return self.find(entity_id)         # return entity

        except Exception as e:

            Logger.log_error(msg=f"{e} during updating", is_verbose=self.verbose)

            if not safe:
                raise e
