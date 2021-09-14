from datetime import date


class Todo:
    def __init__(
        self, id: int, description: str, due_date: date, is_complete: bool = False
    ) -> None:
        self.id = id
        self.description = description
        self.due_date = due_date
        self._is_complete = is_complete

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Todo):
            return False
        return other.id == self.id

    def mark_complete(self):
        if not self._is_complete:
            self._is_complete = True

    def mark_incomplete(self):
        if self._is_complete:
            self._is_complete = False

    @property
    def status(self) -> bool:
        return self._is_complete

    @property
    def is_due(self) -> bool:
        return self.due_date > date.today()
