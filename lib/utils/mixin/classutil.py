from abc import ABC
from typing import List, Tuple, Dict, Any
from lib.utils.pair import PairAttrValue


class ModifyMixin(ABC):

    def modify(self, new: dict) -> None:
        """
        Update fields from dict

        :param new: new data
        :type new: dict

        :return: None
        """

        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)


class AppendAttrMixin(ABC):

    def append_attr(self, attr: str, value: Any) -> None:
        setattr(self, attr, value)

    def append_attr_from_pair(self, pair: PairAttrValue) -> None:
        self.append_attr(attr=pair.attr, value=pair.value)

    def append_attr_from_tuple(self, pair: Tuple) -> None:
        self.append_attr(attr=pair[0], value=pair[0])

    def append_attr_from_list(self, data: List[Tuple | PairAttrValue] | Tuple[Tuple | PairAttrValue]) -> None:
        for d in data:
            if isinstance(d, Tuple):
                self.append_attr_from_tuple(d)

            if isinstance(d, PairAttrValue):
                self.append_attr_from_pair(d)

    def append_attr_from_list_of_tuple(self, data: List[Tuple[str, Any]] | Tuple[Tuple[str, Any]]) -> None:

        for pair in data:
            self.append_attr_from_tuple(pair)

    def append_attr_from_list_of_pair(self, data: List[PairAttrValue] | Tuple[PairAttrValue]) -> None:

        for pair in data:
            self.append_attr_from_pair(pair)
