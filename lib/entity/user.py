from lib.db.entity_manager import EntityManager
from dataclasses import dataclass



@dataclass
class UserModel:
    id: int
    username: str


class UserManager(EntityManager):

    __table_name = "user"

    def __init__(self):
        super().__init__()



