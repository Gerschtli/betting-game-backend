from unittest.mock import Mock, call

from app.modules import auth, register_blueprints, secret, users


def test_register_blueprint() -> None:
    app = Mock('flask.Flask', autospec=True)
    app.register_blueprint = Mock()

    register_blueprints(app)

    assert app.register_blueprint.call_args_list == [
        call(auth.module),
        call(secret.module),
        call(users.module),
    ]
