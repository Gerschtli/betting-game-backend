import logging
import os
import sys
import time

from flask import Flask
from flask_migrate import Migrate

from .config import default as default_config
from .errors import register_error_handler
from .jwt import jwt
from .models import db
from .modules import register_blueprints


def create_app() -> Flask:
    os.environ['TZ'] = 'Europe/Berlin'
    time.tzset()

    app = Flask(__name__)
    app.config.from_object(default_config)  # type: ignore
    app.config.from_envvar('APP_CONFIG_FILE')  # type: ignore

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    logging.basicConfig(
        level=logging.DEBUG,
        stream=sys.stdout,
    )

    register_error_handler(app)
    register_blueprints(app)

    return app
