import datetime
from typing import Dict

import flask_jwt_extended
from flask import Blueprint
from flask_restful import Api

from .. import models, request
from ..errors import InputValidationError
from ..resource import Resource
from ..response import Response, no_content
from ..validator import schemas, validate_schema

module = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(module)


@api.resource('/login')
class Login(Resource):
    @validate_schema(schemas.LOGIN)
    @staticmethod
    def post() -> Dict[str, str]:
        data = request.get_json()
        current_user = models.User.find_by_username(data['username'])

        if not current_user or not models.User.verify_hash(data['password'], current_user.password):
            raise InputValidationError.build_general_error('loginFailed')

        access_token = flask_jwt_extended.create_access_token(identity=current_user)
        decoded_token = flask_jwt_extended.decode_token(access_token)

        token = models.Token(
            jti=decoded_token['jti'],
            user_id=decoded_token['identity'],
            expires=datetime.datetime.fromtimestamp(decoded_token['exp']),
            revoked=False,
        )
        token.save()

        return {
            'access_token': access_token,
            'id': current_user.id,
        }


@api.resource('/logout')
class Logout(Resource):
    @staticmethod
    def post() -> Response:
        raw_jwt = flask_jwt_extended.get_raw_jwt()

        if 'jti' in raw_jwt:
            jti = raw_jwt['jti']

            token = models.Token.find_by_jti(jti)
            if token is not None:
                token.revoked = True
                token.save()

        return no_content()
