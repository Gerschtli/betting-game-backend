import smtplib
from typing import Any, Dict

import flask
import flask_mail

from . import config

mail = flask_mail.Mail()


def send_mail(email: str, template: str, params: Dict[str, Any]) -> bool:
    message = flask_mail.Message()

    message.sender = '{} <{}>'.format(
        config.get('APP_EMAIL_SENDER_NAME'),
        config.get('APP_EMAIL_SENDER_MAIL'),
    )
    message.recipients = [email]
    message.subject = flask.render_template(
        '{}/subject.txt'.format(template),
        **params,
    )
    message.body = flask.render_template(
        '{}/body.txt'.format(template),
        **params,
    )

    mail: flask_mail.Mail = flask.current_app.extensions['mail']
    try:
        mail.send(message)
    except smtplib.SMTPException:
        return False

    return True
