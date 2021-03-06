from flask import Flask

from . import auth, invitations, secret, users


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(auth.module)
    app.register_blueprint(invitations.module)
    app.register_blueprint(secret.module)
    app.register_blueprint(users.module)
