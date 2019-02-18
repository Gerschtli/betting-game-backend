from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import default as default_config

app = Flask(__name__)
app.config.from_object(default_config)
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    return jsonify({'message': 'index'})
