from typing import Any, Dict, Tuple

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from .config import default as default_config
from .response import Response

app = Flask(__name__)
app.config.from_object(default_config)  # type: ignore
app.config.from_envvar('APP_CONFIG_FILE')  # type: ignore

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


@app.errorhandler(NotFound)
def not_found(error: NotFound) -> Tuple[Response, int]:
    return jsonify({'message': 'Not Found'}), 404


@app.errorhandler(SQLAlchemyError)
def database_error(error: SQLAlchemyError) -> Tuple[Response, int]:
    return jsonify({'message': 'Internal Server Error'}), 500


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token: Dict[str, Any]) -> bool:
    from .models import Token

    jti = decrypted_token['jti']
    return Token.is_jti_blacklisted(jti)


def register_blueprints(app: Flask) -> None:
    from .modules import auth, secret, users

    app.register_blueprint(auth.module)
    app.register_blueprint(secret.module)
    app.register_blueprint(users.module)


register_blueprints(app)
