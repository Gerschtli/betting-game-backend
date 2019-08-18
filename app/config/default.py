import datetime

from . import smtp

PROPAGATE_EXCEPTIONS = True
SECRET_KEY = 'secret'

JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=8)
JWT_BLACKLIST_ENABLED = True
JWT_SECRET_KEY = 'jwt-secret-string'

MAIL_SERVER = smtp.MAIL_SERVER
MAIL_PORT = smtp.MAIL_PORT
MAIL_USE_SSL = smtp.MAIL_USE_SSL
MAIL_USERNAME = smtp.MAIL_USERNAME
MAIL_PASSWORD = smtp.MAIL_PASSWORD

SQLALCHEMY_TRACK_MODIFICATIONS = False

APP_BASE_URL = 'http://localhost:8080'
APP_EMAIL_SENDER_MAIL = 'no-reply@bg.tobias-happ.de'
APP_EMAIL_SENDER_NAME = 'Fußball Tippspiel Team'
APP_PROJECT_NAME = 'Fußball Tippspiel'
