from datetime import date

from src.domain import model
from src.adapters import repository


def insert_todo(session):
    session.execute(
        "INSERT INTO todos (description, due_date, _is_complete)"
        ' VALUES ("A Todo", "2021-01-01", 0)'
    )

    [[todo_id]] = session.execute("SELECT id FROM todos WHERE id=:id", dict(id=1))
    return todo_id


def test_repository_can_save_a_todo(session):
    todo = model.Todo(None, "Write Azure Functions App", date(2021, 1, 1), False)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(todo)
    session.commit()

    rows = list(
        session.execute('SELECT id, description, due_date, _is_complete FROM "todos"')
    )
    assert rows == [(1, "Write Azure Functions App", "2021-01-01", 0)]


def test_repository_can_retrieve_a_todo_by_id(session):
    todo_id = insert_todo(session)

    repo = repository.SqlAlchemyRepository(session)
    retrieved_todo = repo.get(todo_id)

    expected = model.Todo(todo_id, "A Todo", date(2021, 1, 1), False)
    assert retrieved_todo == expected  # Todo.__eq__ compares only the id field
    assert retrieved_todo.description == expected.description
    assert retrieved_todo.due_date == expected.due_date
    assert retrieved_todo._is_complete == expected._is_complete
