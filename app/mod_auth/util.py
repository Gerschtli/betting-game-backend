import datetime

from flask_jwt_extended import create_access_token, decode_token

from ..models import Token


def _epoch_utc_to_datetime(epoch_utc):
    return datetime.datetime.fromtimestamp(epoch_utc)


def add_token_to_database(encoded_token):
    decoded_token = decode_token(encoded_token)

    jti = decoded_token['jti']
    user_id = decoded_token['identity']
    expires = _epoch_utc_to_datetime(decoded_token['exp'])
    revoked = False

    token = Token(
        jti=jti,
        user_id=user_id,
        expires=expires,
        revoked=revoked,
    )
    token.save()


def create_token(user):
    access_token = create_access_token(identity=user.id)
    add_token_to_database(access_token)

    return access_token
