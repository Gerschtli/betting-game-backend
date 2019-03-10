import datetime
from typing import Dict

from flask import Blueprint, request
from flask_jwt_extended import create_access_token, decode_token, get_raw_jwt
from flask_restful import Api
from werkzeug.exceptions import Unauthorized

from ..models import Token, User
from ..resource import AuthenticatedResource, Resource
from ..response import Response, no_content
from ..validator import schemas, validate_schema

module = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(module)


def _epoch_utc_to_datetime(epoch_utc: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(epoch_utc)


def _add_token_to_database(encoded_token: str) -> None:
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


def _create_token(user: User) -> str:
    access_token = create_access_token(identity=user.id)
    _add_token_to_database(access_token)

    return access_token


@api.resource('/login')
class Login(Resource):
    @validate_schema(schemas.USER)
    def post(self) -> Dict[str, str]:
        data = request.get_json()
        current_user = User.find_by_username(data['username'])

        if not current_user or not User.verify_hash(data['password'], current_user.password):
            raise Unauthorized()

        access_token = _create_token(current_user)

        return {'access_token': access_token}


@api.resource('/logout')
class Logout(AuthenticatedResource):
    def post(self) -> Response:
        jti = get_raw_jwt()['jti']

        token = Token.find_by_jti(jti)
        token.revoked = True
        token.save()

        return no_content()
