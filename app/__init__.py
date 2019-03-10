from typing import Any, Dict

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import default as default_config
from .errors import register_error_handler

app = Flask(__name__)
app.config.from_object(default_config)  # type: ignore
app.config.from_envvar('APP_CONFIG_FILE')  # type: ignore

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


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


register_error_handler(app)
register_blueprints(app)
