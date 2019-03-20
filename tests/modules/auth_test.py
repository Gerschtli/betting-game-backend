import datetime
from http import HTTPStatus
from unittest.mock import Mock, patch

from flask import Blueprint, Flask

from app.modules import auth
from app.resource import AuthenticatedResource, Resource
from app.validator import schemas

from .utils import build_authorization_headers, get_validator_schema, validator_call_through


def test_module() -> None:
    assert isinstance(auth.module, Blueprint)
    assert auth.module.name == 'auth'
    assert auth.module.url_prefix == '/auth'


class TestLogin(object):
    def test_subclass(self) -> None:
        assert issubclass(auth.Login, Resource)

    @patch('flask_jwt_extended.decode_token')
    @patch('flask_jwt_extended.create_access_token')
    @patch('app.models.Token', autospec=True)
    @patch('app.models.User', autospec=True)
    @patch('app.validator._validate_schema')
    def test_post(self, mock_validate_schema: Mock, mock_user: Mock, mock_token: Mock,
                  mock_create_token: Mock, mock_decode_token: Mock, app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through

        current_user = Mock('app.models.User', autospec=True)
        current_user.id = 123
        current_user.password = 'hash'

        mock_user.find_by_username.return_value = current_user
        mock_user.verify_hash.return_value = True

        mock_create_token.return_value = 'access_token'
        mock_decode_token.return_value = {
            'jti': 'token_jti',
            'identity': 'token_identity',
            'exp': 1553117809,
        }

        token_instance = mock_token.return_value

        app.register_blueprint(auth.module)

        client = app.test_client()

        response = client.post('/auth/login', json={'username': 'flask', 'password': 'secret'})

        assert get_validator_schema(mock_validate_schema) == schemas.USER

        mock_user.find_by_username.assert_called_once_with('flask')
        mock_user.verify_hash.assert_called_once_with('secret', 'hash')

        mock_create_token.assert_called_once_with(identity=123)
        mock_decode_token.assert_called_once_with('access_token')

        mock_token.assert_called_once_with(
            jti='token_jti',
            user_id='token_identity',
            expires=datetime.datetime(2019, 3, 20, 22, 36, 49),
            revoked=False,
        )
        token_instance.save.assert_called_once_with()

        assert response.data == b'{"access_token": "access_token"}\n'
        assert response.status_code == HTTPStatus.OK

    @patch('app.models.User', autospec=True)
    @patch('app.validator._validate_schema')
    def test_post_with_wrong_password(self, mock_validate_schema: Mock, mock_user: Mock,
                                      app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through

        current_user = Mock('app.models.User', autospec=True)
        current_user.password = 'hash'

        mock_user.find_by_username.return_value = current_user
        mock_user.verify_hash.return_value = False

        app.register_blueprint(auth.module)

        client = app.test_client()

        response = client.post('/auth/login', json={'username': 'flask', 'password': 'secret'})

        assert get_validator_schema(mock_validate_schema) == schemas.USER

        mock_user.find_by_username.assert_called_once_with('flask')
        mock_user.verify_hash.assert_called_once_with('secret', 'hash')

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @patch('app.models.User', autospec=True)
    @patch('app.validator._validate_schema')
    def test_post_with_no_user(self, mock_validate_schema: Mock, mock_user: Mock,
                               app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through

        mock_user.find_by_username.return_value = None

        app.register_blueprint(auth.module)

        client = app.test_client()

        response = client.post('/auth/login', json={'username': 'flask', 'password': 'secret'})

        assert get_validator_schema(mock_validate_schema) == schemas.USER

        mock_user.find_by_username.assert_called_once_with('flask')

        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestLogout(object):
    def test_subclass(self) -> None:
        assert issubclass(auth.Logout, AuthenticatedResource)

    @patch('app.models.Token', autospec=True)
    @patch('flask_jwt_extended.get_raw_jwt')
    def test_post(self, mock_get_jwt: Mock, mock_token: Mock, app: Flask) -> None:
        mock_get_jwt.return_value = {'jti': 'token_jti'}

        token_instance = Mock('app.models.Token', autospec=True)
        token_instance.revoked = False
        token_instance.save = Mock()
        mock_token.find_by_jti.return_value = token_instance

        app.register_blueprint(auth.module)

        client = app.test_client()

        response = client.post('/auth/logout', headers=build_authorization_headers(app))

        mock_token.find_by_jti.assert_called_once_with('token_jti')
        token_instance.save.assert_called_once_with()
        assert token_instance.revoked

        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT
