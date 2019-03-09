from flask import Blueprint, request
from flask_jwt_extended import get_raw_jwt
from flask_restful import Api

from ..models import Token, User
from ..resource import AuthenticatedResource, Resource
from ..response import no_content
from ..validator import matcher, schemas, validate_input, validate_schema
from .util import create_token


class UserRegistration(Resource):
    @validate_schema(schemas.USER)
    @validate_input({
        'username': matcher.And(matcher.NotBlank(), matcher.UniqueUsername()),
        'password': matcher.MinLength(6),
    })
    def post(self):
        data = request.get_json()

        new_user = User(username=data['username'], password=User.generate_hash(data['password']))
        new_user.save()

        return no_content()


class UserLogin(Resource):
    @validate_schema(schemas.USER)
    def post(self):
        data = request.get_json()
        current_user = User.find_by_username(data['username'])

        if not current_user or not User.verify_hash(data['password'], current_user.password):
            return {'message': 'Wrong credentials'}

        access_token = create_token(current_user)

        return {'access_token': access_token}


class UserLogout(AuthenticatedResource):
    def post(self):
        jti = get_raw_jwt()['jti']

        token = Token.find_by_jti(jti)
        token.revoked = True
        token.save()

        return no_content()


class SecretResource(AuthenticatedResource):
    def get(self):
        return {'answer': 42}


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(mod_auth)

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(SecretResource, '/secret')
