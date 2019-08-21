import smtplib
from unittest.mock import Mock, call, patch

from flask import Flask
from flask_mail import Mail

from app import mail


def test_init() -> None:
    assert isinstance(mail.mail, Mail)


@patch('app.mail.mail')
@patch('flask.render_template')
@patch('app.config.get')
@patch('flask_mail.Message')
def test_send_mail(
        mock_message: Mock,
        mock_config: Mock,
        mock_render: Mock,
        mock_mail: Mock,
        app: Flask,
) -> None:
    with app.app_context():  # type: ignore
        mock_config.side_effect = ['name', 'sender@mail.com']
        mock_render.side_effect = ['subject', 'body']

        app.extensions = {'mail': Mock()}
        app.extensions['mail'].send = Mock()

        message_instance = mock_message.return_value

        assert mail.send_mail(
            'mail@example.com',
            'template-dir',
            {'key': 'value'},
        )

        mock_message.assert_called_once_with()
        mock_config.assert_has_calls([  # type: ignore
            call('APP_EMAIL_SENDER_NAME'),
            call('APP_EMAIL_SENDER_MAIL'),
        ])
        mock_render.assert_has_calls([
            call('template-dir/subject.txt', key='value'),
            call('template-dir/body.txt', key='value'),
        ])
        app.extensions['mail'].send.assert_called_once_with(message_instance)

        assert message_instance.sender == 'name <sender@mail.com>'
        assert message_instance.recipients == ['mail@example.com']
        assert message_instance.subject == 'subject'
        assert message_instance.body == 'body'


@patch('app.mail.mail')
@patch('flask.render_template')
@patch('app.config.get')
@patch('flask_mail.Message')
def test_send_mail_with_exception(
        mock_message: Mock,
        mock_config: Mock,
        mock_render: Mock,
        mock_mail: Mock,
        app: Flask,
) -> None:
    with app.app_context():  # type: ignore
        mock_config.side_effect = ['name', 'sender@mail.com']
        mock_render.side_effect = ['subject', 'body']

        app.extensions = {'mail': Mock()}
        app.extensions['mail'].send = Mock(side_effect=smtplib.SMTPException())

        message_instance = mock_message.return_value

        assert not mail.send_mail(
            'mail@example.com',
            'template-dir',
            {'key': 'value'},
        )

        mock_message.assert_called_once_with()
        mock_config.assert_has_calls([
            call('APP_EMAIL_SENDER_NAME'),
            call('APP_EMAIL_SENDER_MAIL'),
        ])
        mock_render.assert_has_calls([
            call('template-dir/subject.txt', key='value'),
            call('template-dir/body.txt', key='value'),
        ])
        app.extensions['mail'].send.assert_called_once_with(message_instance)

        assert message_instance.sender == 'name <sender@mail.com>'
        assert message_instance.recipients == ['mail@example.com']
        assert message_instance.subject == 'subject'
        assert message_instance.body == 'body'
