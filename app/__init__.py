import logging
import sys

import flask
import flask_cors
import flask_migrate

from . import errors, jwt, models, modules
from .config import default as default_config


def create_app() -> flask.Flask:
    app = flask.Flask(__name__)
    app.config.from_object(default_config)  # type: ignore
    app.config.from_envvar('APP_CONFIG_FILE')  # type: ignore

    models.db.init_app(app)
    jwt.jwt.init_app(app)
    flask_cors.CORS(app)
    flask_migrate.Migrate(app, models.db)

    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
    )

    errors.register_error_handler(app)
    modules.register_blueprints(app)

    return app
