from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import app

# TODO: test everything else in app/__init__.py


def test_init() -> None:
    assert isinstance(app.app, Flask)
    assert isinstance(app.db, SQLAlchemy)
    assert isinstance(app.jwt, JWTManager)
    assert isinstance(app.migrate, Migrate)
