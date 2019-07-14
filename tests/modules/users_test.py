from http import HTTPStatus
from unittest.mock import Mock, patch

from flask import Blueprint, Flask

from app.modules import users
from app.resource import Resource
from app.validator import matcher, schemas

from .utils import get_validator_schema, validator_call_through


def test_module() -> None:
    assert isinstance(users.module, Blueprint)
    assert users.module.name == 'users'
    assert users.module.url_prefix == '/users'


class TestUsers(object):
    def test_subclass(self) -> None:
        assert issubclass(users.Users, Resource)

    @patch('app.models.User')
    @patch('app.validator._validate_input')
    @patch('app.validator._validate_schema')
    def test_post(self, mock_validate_schema: Mock, mock_validate_input: Mock, mock_user: Mock,
                  app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through
        mock_validate_input.side_effect = validator_call_through

        mock_user.generate_hash.return_value = 'hash'
        user_instance = mock_user.return_value

        app.register_blueprint(users.module)

        client = app.test_client()

        response = client.post(  # type: ignore
            '/users',
            json={
                'username': 'flask',
                'password': 'secret',
                'email': 'mail',
                'is_admin': True,
            },
        )

        assert get_validator_schema(mock_validate_schema) == schemas.USER
        schema = get_validator_schema(mock_validate_input)

        assert list(schema.keys()) == ['username', 'password', 'email']
        assert isinstance(schema['username'], matcher.And)
        assert len(schema['username'].matchers) == 2
        assert isinstance(schema['username'].matchers[0], matcher.Required)
        assert isinstance(schema['username'].matchers[1], matcher.UniqueUsername)
        assert isinstance(schema['password'], matcher.MinLength)
        assert schema['password'].min_length == 6
        assert isinstance(schema['email'], matcher.Required)

        mock_user.generate_hash.assert_called_once_with('secret')
        mock_user.assert_called_once_with(
            username='flask',
            password='hash',
            email='mail',
            is_admin=True,
        )
        user_instance.save.assert_called_once_with()

        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT
