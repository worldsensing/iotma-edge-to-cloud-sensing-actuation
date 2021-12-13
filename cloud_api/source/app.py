import logging

from flask import Flask
from flask_restful import Api

from resources.resources_loader import Resources
from utils import db_uri

logger = logging.getLogger(__name__)

SQLALCHEMY_SETTINGS = {
    "SQLALCHEMY_DATABASE_URI": db_uri,
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}


def create_app(settings=SQLALCHEMY_SETTINGS):
    app = Flask(__name__)
    api = Api(app)

    logger.info("Enabling CORS and setting wildcards")
    Resources.init_cors(app)

    logger.info("Connecting to the DB")
    app.config["SQLALCHEMY_DATABASE_URI"] = settings["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings["SQLALCHEMY_TRACK_MODIFICATIONS"]

    with app.app_context():
        import database
        database.init_db()
        # TODO Future improvement
        # yield app

    Resources.load_resources(api)

    return app, database
