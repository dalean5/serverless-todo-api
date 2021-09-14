import json
import logging

import azure.functions as func
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy import create_engine

from helpers import schema
from src import config
from src.domain import model
from src.adapters import orm, repository
from src.service_layer import services

get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    # check if payload was actually passed, raise 400 error if not
    try:
        data = req.get_json()
    except Exception as e:
        return func.HttpResponse(status_code=400, mimetype="application/json")

    # use our custom validator function to validate the payload,
    # return 400 if invalid
    is_valid, data = schema.validate_data(data)

    if not is_valid:
        return func.HttpResponse(
            body=json.dumps(data), status_code=400, mimetype="application/json"
        )

    try:
        orm.start_mappers()
        session = get_session()
        repo = repository.SqlAlchemyRepository(session)
        services.update_todo(
            data.description, data.due_date, data.is_complete, repo, session
        )
        return func.HttpResponse(status_code=201, mimetype="application/json")
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
