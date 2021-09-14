from datetime import date
from typing import List

import pytest

from src.domain import model
from src.service_layer import services
from src.adapters import repository


class FakeRepository(repository.AbstractRepository):
    def __init__(self, todos):
        self._todos = set(todos)

    def add(self, todo: model.Todo) -> None:
        self._todos.add(todo)

    def get(self, id: int) -> model.Todo:
        try:
            return next(t for t in self._todos if t.id == id)
        except StopIteration:
            return None

    def list(self) -> List[model.Todo]:
        return list(self._todos)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_add_todo():
    repo, session = FakeRepository([]), FakeSession()
    services.add_todo("A Todo", date(2021, 1, 1), False, repo, session)
    assert len(repo.list()) == 1
    assert session.committed


def test_get_todo_error_if_todo_not_found():
    repo = FakeRepository([])

    with pytest.raises(services.TodoNotFound, match="Todo with id 1 not found"):
        services.get_todo(1, repo)
