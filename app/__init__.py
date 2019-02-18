from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import default as default_config

app = Flask(__name__)
app.config.from_object(default_config)
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not Found'}), 404


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    from app.mod_auth.models import Token

    jti = decrypted_token['jti']
    return Token.is_jti_blacklisted(jti)


def register_blueprints(app):
    from app.mod_auth.resources import mod_auth as auth_module

    app.register_blueprint(auth_module)


register_blueprints(app)
