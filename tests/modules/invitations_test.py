from http import HTTPStatus
from unittest.mock import Mock, patch

from flask import Blueprint, Flask

from app.models import Invitation
from app.modules import invitations
from app.resource import AdminResource
from app.validator import matcher, schemas

from .utils import build_authorization_headers, get_validator_schema, validator_call_through


def test_module() -> None:
    assert isinstance(invitations.module, Blueprint)
    assert invitations.module.name == 'invitations'
    assert invitations.module.url_prefix == '/invitations'


class TestInvitations(object):
    def test_subclass(self) -> None:
        assert issubclass(invitations.Invitations, AdminResource)

    @patch('app.models.Invitation.get_all')
    def test_get(self, mock_get_all: Mock, app: Flask) -> None:
        mock_get_all.return_value = [
            Invitation(email='email', is_admin=True),
            Invitation(email='email2', is_admin=False),
        ]

        app.register_blueprint(invitations.module)

        client = app.test_client()

        response = client.get(  # type: ignore
            '/invitations',
            headers=build_authorization_headers(app, is_admin=True),
        )

        mock_get_all.assert_called_once_with()

        assert response.data == (b'[{"email": "email", "is_admin": true}, '
                                 b'{"email": "email2", "is_admin": false}]\n')
        assert response.status_code == HTTPStatus.OK

    @patch('app.models.Invitation')
    @patch('uuid.uuid4')
    @patch('app.time.get_invitation_expire')
    @patch('app.validator._validate_input')
    @patch('app.validator._validate_schema')
    def test_post(self, mock_validate_schema: Mock, mock_validate_input: Mock,
                  mock_get_invitation_expire: Mock, mock_uuid4: Mock, mock_invitation: Mock,
                  app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through
        mock_validate_input.side_effect = validator_call_through

        mock_get_invitation_expire.return_value = 123

        mock_uuid4.return_value = 'uuid value'

        invitation_instance = mock_invitation.return_value

        app.register_blueprint(invitations.module)

        client = app.test_client()

        response = client.post(  # type: ignore
            '/invitations',
            headers=build_authorization_headers(app, is_admin=True),
            json={
                'email': 'mail',
                'is_admin': True,
            },
        )

        assert get_validator_schema(mock_validate_schema) == schemas.INVITATION
        schema = get_validator_schema(mock_validate_input)

        assert list(schema.keys()) == ['email']
        assert isinstance(schema['email'], matcher.And)
        assert len(schema['email'].matchers) == 2
        assert isinstance(schema['email'].matchers[0], matcher.NotBlank)
        assert isinstance(schema['email'].matchers[1], matcher.UniqueInvitationEmail)

        mock_get_invitation_expire.assert_called_once_with()

        mock_invitation.assert_called_once_with(
            email='mail',
            is_admin=True,
            token='uuid value',
            expires=123,
        )
        invitation_instance.save.assert_called_once_with()

        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT
