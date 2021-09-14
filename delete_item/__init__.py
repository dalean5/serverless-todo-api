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
        id = req.route_params.get("id")
        id = int(id)
    except ValueError as e:
        logging.exception(e)
        return func.HttpResponse(
            body=json.dumps({"msg": f"Invalid route parameter - {id}"}),
            status_code=400,
            mimetype="application/json",
        )

    try:
        orm.start_mappers()
        session = get_session()
        repo = repository.SqlAlchemyRepository(session)
        services.delete_todo(id, repo)
        session.commit()
        return func.HttpResponse(
            status_code=204,
            mimetype="application/json",
        )
    except services.TodoNotFound as e:
        return func.HttpResponse(
            body=json.dumps(e, default=str),
            status_code=404,
            mimetype="application/json",
        )
    except Exception as e:
        logging.exception(e)
        return func.HttpResponse(status_code=500, mimetype="application/json")
    finally:
        clear_mappers()
