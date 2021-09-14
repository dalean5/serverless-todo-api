from datetime import date
from typing import List

from src.domain import model
from src.adapters import repository
from helpers import schema


class TodoNotFound(Exception):
    pass


def add_todo(
    description: str,
    due_date: date,
    is_complete: bool,
    repo: repository.AbstractRepository,
    session,
) -> None:
    repo.add(model.Todo(None, description, due_date, is_complete))
    session.commit()


def get_todo(id: int, repo: repository.AbstractRepository) -> model.Todo:
    todo = repo.get(id)
    if todo is None:
        raise TodoNotFound(f"Todo with id {id} not found")
    return todo


def list_todos(repo: repository.AbstractRepository) -> List[model.Todo]:
    todos = repo.list()
    return todos


def delete_todo(id: int, repo: repository.AbstractRepository) -> None:
    todo = get_todo(id, repo)
    repo.delete(todo)


def update_todo(
    id: int,
    description: str,
    due_date: date,
    is_complete: bool,
    repo: repository.AbstractRepository,
    session,
) -> None:
    found_todo = get_todo(id, repo)
    if is_complete:
        found_todo.mark_complete()
    else:
        found_todo.mark_incomplete()

    found_todo.description = description
    found_todo.due_date = due_date
    session.commit()
