from dataclasses import dataclass
from lib.utils.mixin.dcparser import DCToDictMixin


@dataclass
class Error(DCToDictMixin):
    code: str
    message: str


class Errors:
    LOGIN_REQUIRE = Error(
        code="A1",
        message="login require"
    )
