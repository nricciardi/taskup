from lib.db.entity_manager import EntityManager
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    name: str


class TasksManager(EntityManager):
    table_name: str = "task"

    def __init__(self):
        super().__init__()
