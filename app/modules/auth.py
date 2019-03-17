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


@api.resource('/login')
class Login(Resource):
    @validate_schema(schemas.USER)
    @staticmethod
    def post() -> Dict[str, str]:
        data = request.get_json()
        current_user = User.find_by_username(data['username'])

        if not current_user or not User.verify_hash(data['password'], current_user.password):
            raise Unauthorized()

        access_token = create_access_token(identity=current_user.id)
        decoded_token = decode_token(access_token)

        token = Token(
            jti=decoded_token['jti'],
            user_id=decoded_token['identity'],
            expires=datetime.datetime.fromtimestamp(decoded_token['exp']),
            revoked=False,
        )
        token.save()

        return {'access_token': access_token}


@api.resource('/logout')
class Logout(AuthenticatedResource):
    @staticmethod
    def post() -> Response:
        jti = get_raw_jwt()['jti']

        token = Token.find_by_jti(jti)
        token.revoked = True
        token.save()

        return no_content()
