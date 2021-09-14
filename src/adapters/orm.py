from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Boolean
from sqlalchemy.orm import registry

from src.domain import model

mapper_registry = registry()

metadata = MetaData()

todos = Table(
    "todos",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("description", String(100), nullable=False),
    Column("due_date", Date, nullable=False),
    Column("_is_complete", Boolean, nullable=False),
)


def start_mappers():
    mapper_registry.map_imperatively(model.Todo, todos)
