from datetime import date, timedelta

from src.domain import model

yesterday = date.today() - timedelta(days=-1)
today = date.today()


def test_todo_due_date():
    todo = model.Todo(1, "A Todo", yesterday)

    assert todo.is_due


def test_todo_mark_complete():
    todo = model.Todo(1, "A Todo", today)

    assert todo.status is False
    todo.mark_complete()
    assert todo.status is True


def test_todo_mark_incomplete():
    todo = model.Todo(1, "A Todo", today)

    todo.mark_complete()
    assert todo.status is True
    todo.mark_incomplete()
    assert todo.status is False
