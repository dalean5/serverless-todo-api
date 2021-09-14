import json
from src.domain.model import Todo


class TodoSerializer(json.JSONEncoder):
    def default(self, o: Todo):
        try:
            to_serialize = {
                "id": str(o.id),
                "description": o.description,
                "due_date": o.due_date.isoformat(),
                "is_complete": o._is_complete,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)
