import json
import logging

import azure.functions as func
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy import create_engine

from src import config
from src.adapters import orm, repository
from src.service_layer import services
from helpers import serializers

get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        orm.start_mappers()
        session = get_session()
        repo = repository.SqlAlchemyRepository(session)
        todos = services.list_todos(repo)
        return func.HttpResponse(
            body=json.dumps(todos, cls=serializers.TodoSerializer),
            status_code=200,
            mimetype="application/json",
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(status_code=500, mimetype="application/json")
    finally:
        clear_mappers()
