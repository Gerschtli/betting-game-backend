from flask import Flask

import app

# TODO: test everything else in app/__init__.py


def test_create_app() -> None:
    assert isinstance(app.create_app(), Flask)
