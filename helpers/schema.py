from datetime import date

from pydantic import BaseModel, Field, ValidationError


class TodoSchema(BaseModel):
    description: str
    due_date: date
    is_complete: bool


def validate_data(data):
    try:
        validated_data = TodoSchema.validate(data)
        return (True, validated_data)
    except ValidationError as e:
        return (False, e.errors())
