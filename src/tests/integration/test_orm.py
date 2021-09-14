from datetime import date

from src.domain import model


def test_todos_mappers_can_load_todos(session):
    """Test if the todos mapper can read values from the
    database as Python objects (in this case, model.Todo)
    """
    session.execute(
        "INSERT INTO todos (description, due_date, _is_complete)"
        ' VALUES ("Buy groceries", "2021-01-01", 1)'
    )

    expected = [model.Todo(1, "Buy Groceries", date(2021, 1, 1))]
    assert session.query(model.Todo).all() == expected


def test_todos_mapper_can_save_todos(session):
    todo = model.Todo(None, "A Todo", due_date=date(2021, 1, 1))
    session.add(todo)
    session.commit()

    rows = list(
        session.execute('SELECT id, description, due_date, _is_complete FROM "todos"')
    )
    assert rows == [(1, "A Todo", "2021-01-01", 0)]
