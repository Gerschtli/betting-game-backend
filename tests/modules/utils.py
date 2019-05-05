from typing import Any, Callable, Dict, List, TypeVar
from unittest.mock import Mock

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

RT = TypeVar('RT')


def build_authorization_headers(app: Flask, is_admin: bool = False) -> Dict[str, str]:
    app.config['JWT_SECRET_KEY'] = 'abcxyz'
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_access_token(data: str) -> Dict[str, bool]:
        nonlocal is_admin
        return {'is_admin': is_admin}

    with app.test_request_context():
        access_token = create_access_token('testuser')

    return {'Authorization': 'Bearer {}'.format(access_token)}


def get_validator_schema(mock: Mock) -> Dict[str, Any]:
    mock.assert_called_once()
    args, kwargs = mock.call_args_list[0]

    assert len(args) == 4
    assert kwargs == {}

    return args[0]


def validator_call_through(schema: Dict[str, Any], wrapped: Callable[..., RT], args: List[Any],
                           kwargs: Dict[str, Any]) -> RT:
    return wrapped(*args, **kwargs)
