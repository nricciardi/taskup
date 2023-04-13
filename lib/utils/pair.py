from dataclasses import dataclass
from lib.utils.mixin.dcparser import DCToDictMixin, DCToTupleMixin
from typing import Any


@dataclass
class PairAttrValue(DCToDictMixin, DCToTupleMixin):
    attr: str
    value: Any
