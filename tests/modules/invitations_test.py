from http import HTTPStatus
from unittest.mock import Mock, call, patch

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
            Invitation(id=12, email='email', is_admin=True),
            Invitation(id=23, email='email2', is_admin=False),
        ]

        app.register_blueprint(invitations.module)

        client = app.test_client()

        response = client.get(  # type: ignore
            '/invitations',
            headers=build_authorization_headers(app, is_admin=True),
        )

        mock_get_all.assert_called_once_with()

        assert response.data == (b'[{"id": 12, "email": "email", "is_admin": true}, '
                                 b'{"id": 23, "email": "email2", "is_admin": false}]\n')
        assert response.status_code == HTTPStatus.OK

    @patch('app.models.Invitation')
    @patch('app.time.get_invitation_expire')
    @patch('app.mail.send_mail')
    @patch('app.config.get')
    @patch('app.uuid.generate')
    @patch('app.validator._validate_input')
    @patch('app.validator._validate_schema')
    def test_post(self, mock_validate_schema: Mock, mock_validate_input: Mock, mock_uuid: Mock,
                  mock_config: Mock, mock_send_mail: Mock, mock_get_invitation_expire: Mock,
                  mock_invitation: Mock, app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through
        mock_validate_input.side_effect = validator_call_through
        mock_uuid.return_value = 'uuid-value'
        mock_config.side_effect = ['http://base', 'name']
        mock_send_mail.return_value = True
        mock_get_invitation_expire.return_value = 123

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
        assert isinstance(schema['email'].matchers[0], matcher.Required)
        assert isinstance(schema['email'].matchers[1], matcher.UniqueInvitationEmail)
        assert not schema['email'].matchers[1].ignore_id

        mock_uuid.assert_called_once_with()
        mock_config.assert_has_calls([
            call('APP_BASE_URL'),
            call('APP_PROJECT_NAME'),
        ])
        mock_send_mail.assert_called_once_with('mail', 'invitation', {
            'project_name': 'name',
            'link': 'http://base/invitation/uuid-value',
        })
        mock_get_invitation_expire.assert_called_once_with()

        mock_invitation.assert_called_once_with(
            email='mail',
            is_admin=True,
            token='uuid-value',
            expires=123,
        )
        invitation_instance.save.assert_called_once_with()

        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT

    @patch('app.errors.InputValidationError.build_general_error')
    @patch('app.mail.send_mail')
    @patch('app.config.get')
    @patch('app.uuid.generate')
    @patch('app.validator._validate_input')
    @patch('app.validator._validate_schema')
    def test_post_with_error(self, mock_validate_schema: Mock, mock_validate_input: Mock,
                             mock_uuid: Mock, mock_config: Mock, mock_send_mail: Mock,
                             mock_build_general_error: Mock, app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through
        mock_validate_input.side_effect = validator_call_through
        mock_uuid.return_value = 'uuid-value'
        mock_config.side_effect = ['http://base', 'name']
        mock_send_mail.return_value = False

        mock_build_general_error.return_value = Exception('mail error')

        app.register_blueprint(invitations.module)

        client = app.test_client()

        exception = None
        try:
            client.post(  # type: ignore
                '/invitations',
                headers=build_authorization_headers(app, is_admin=True),
                json={
                    'email': 'mail',
                    'is_admin': True,
                },
            )
        except Exception as err:
            exception = err

        assert get_validator_schema(mock_validate_schema) == schemas.INVITATION
        schema = get_validator_schema(mock_validate_input)

        assert list(schema.keys()) == ['email']
        assert isinstance(schema['email'], matcher.And)
        assert len(schema['email'].matchers) == 2
        assert isinstance(schema['email'].matchers[0], matcher.Required)
        assert isinstance(schema['email'].matchers[1], matcher.UniqueInvitationEmail)
        assert not schema['email'].matchers[1].ignore_id

        mock_uuid.assert_called_once_with()
        mock_config.assert_has_calls([
            call('APP_BASE_URL'),
            call('APP_PROJECT_NAME'),
        ])
        mock_send_mail.assert_called_once_with('mail', 'invitation', {
            'project_name': 'name',
            'link': 'http://base/invitation/uuid-value',
        })

        mock_build_general_error.assert_called_once_with('mailSendFailed')

        assert exception is not None
        assert isinstance(exception, Exception)
        assert str(exception) == 'mail error'


class TestInvitation(object):
    def test_subclass(self) -> None:
        assert issubclass(invitations.Invitation, AdminResource)

    @patch('app.models.Invitation')
    @patch('app.validator._validate_input')
    @patch('app.validator._validate_schema')
    def test_put(self, mock_validate_schema: Mock, mock_validate_input: Mock, mock_invitation: Mock,
                 app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through
        mock_validate_input.side_effect = validator_call_through

        invitation_instance = Mock('app.models.Invitation')
        invitation_instance.save = Mock()
        mock_invitation.find_by_id.return_value = invitation_instance

        app.register_blueprint(invitations.module)

        client = app.test_client()

        response = client.put(  # type: ignore
            '/invitations/321',
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
        assert isinstance(schema['email'].matchers[0], matcher.Required)
        assert isinstance(schema['email'].matchers[1], matcher.UniqueInvitationEmail)
        assert schema['email'].matchers[1].ignore_id

        mock_invitation.find_by_id.assert_called_once_with(321)
        assert invitation_instance.email == 'mail'
        assert invitation_instance.is_admin
        invitation_instance.save.assert_called_once_with()

        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT

    @patch('app.models.Invitation')
    @patch('app.validator._validate_input')
    @patch('app.validator._validate_schema')
    def test_put_when_not_found(self, mock_validate_schema: Mock, mock_validate_input: Mock,
                                mock_invitation: Mock, app: Flask) -> None:
        mock_validate_schema.side_effect = validator_call_through
        mock_validate_input.side_effect = validator_call_through

        mock_invitation.find_by_id.return_value = None

        app.register_blueprint(invitations.module)

        client = app.test_client()

        response = client.put(  # type: ignore
            '/invitations/321',
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
        assert isinstance(schema['email'].matchers[0], matcher.Required)
        assert isinstance(schema['email'].matchers[1], matcher.UniqueInvitationEmail)
        assert schema['email'].matchers[1].ignore_id

        mock_invitation.find_by_id.assert_called_once_with(321)

        assert response.status_code == HTTPStatus.NOT_FOUND

    @patch('app.models.Invitation')
    def test_delete(self, mock_invitation: Mock, app: Flask) -> None:
        invitation_instance = Mock('app.models.Invitation')
        invitation_instance.delete = Mock()
        mock_invitation.find_by_id.return_value = invitation_instance

        app.register_blueprint(invitations.module)

        client = app.test_client()

        response = client.delete(  # type: ignore
            '/invitations/321',
            headers=build_authorization_headers(app, is_admin=True),
        )

        mock_invitation.find_by_id.assert_called_once_with(321)
        invitation_instance.delete.assert_called_once_with()

        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT

    @patch('app.models.Invitation')
    def test_delete_when_not_found(self, mock_invitation: Mock, app: Flask) -> None:
        mock_invitation.find_by_id.return_value = None

        app.register_blueprint(invitations.module)

        client = app.test_client()

        response = client.delete(  # type: ignore
            '/invitations/321',
            headers=build_authorization_headers(app, is_admin=True),
        )

        mock_invitation.find_by_id.assert_called_once_with(321)

        assert response.data == b''
        assert response.status_code == HTTPStatus.NO_CONTENT
