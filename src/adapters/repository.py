import abc
from typing import List

from src.domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, todo: model.Todo) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> model.Todo:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[model.Todo]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, todo: model.Todo) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, todo: model.Todo):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, todo: model.Todo) -> None:
        self.session.add(todo)

    def get(self, id: int) -> model.Todo:
        try:
            return self.session.query(model.Todo).filter_by(id=id).one()
        except Exception as e:
            return None

    def list(self) -> List[model.Todo]:
        return self.session.query(model.Todo).all()

    def delete(self, todo: model.Todo) -> None:
        self.session.delete(todo)

    def update(self, todo: model.Todo):
        self.session.update(todo)
