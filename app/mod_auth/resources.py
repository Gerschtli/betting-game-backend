from flask import Blueprint, request
from flask_jwt_extended import get_raw_jwt, jwt_required
from flask_restful import Api, Resource

from ..models import Token, User
from ..validator import validate_input, validate_schema, schemas
from ..validator.matcher import MinLength, UniqueUsername
from .util import create_token


class UserRegistration(Resource):
    @staticmethod
    @validate_schema(schemas.USER)
    @validate_input({
        'username': UniqueUsername(),
        'password': MinLength(6),
    })
    def post():
        data = request.get_json()

        new_user = User(username=data['username'], password=User.generate_hash(data['password']))
        new_user.save()

        access_token = create_token(new_user)
        return {
            'message': 'User {} was created'.format(data['username']),
            'access_token': access_token,
        }


class UserLogin(Resource):
    @staticmethod
    @validate_schema(schemas.USER)
    def post():
        data = request.get_json()
        current_user = User.find_by_username(data['username'])

        if not current_user or not User.verify_hash(data['password'], current_user.password):
            return {'message': 'Wrong credentials'}

        access_token = create_token(current_user)

        return {
            'message': 'Logged in as {}'.format(current_user.username),
            'access_token': access_token,
        }


class UserLogout(Resource):
    @jwt_required
    @staticmethod
    def post():
        jti = get_raw_jwt()['jti']

        token = Token.find_by_jti(jti)
        token.revoked = True
        token.save()

        return {'message': 'Access token has been revoked'}


class SecretResource(Resource):
    @jwt_required
    @staticmethod
    def get():
        return {'answer': 42}


mod_auth = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(mod_auth)

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(SecretResource, '/secret')
