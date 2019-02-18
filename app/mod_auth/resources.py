from flask import Blueprint
from flask_jwt_extended import get_raw_jwt, jwt_required
from flask_restful import Api, Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError

from app.mod_auth.models import Token, User
from app.mod_auth.util import create_token

mod_auth = Blueprint('auth', __name__, url_prefix='/auth')

PARSER = reqparse.RequestParser()
PARSER.add_argument('username', help='This field cannot be blank', required=True)
PARSER.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    @staticmethod
    def post():
        data = PARSER.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

        new_user = User(username=data['username'], password=User.generate_hash(data['password']))

        try:
            new_user.save()
        except SQLAlchemyError:
            return {'message': 'Something went wrong'}, 500

        access_token = create_token(new_user)
        return {
            'message': 'User {} was created'.format(data['username']),
            'access_token': access_token,
        }


class UserLogin(Resource):
    @staticmethod
    def post():
        data = PARSER.parse_args()
        current_user = User.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_token(current_user)

            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
            }

        return {'message': 'Wrong credentials'}


class UserLogout(Resource):
    @jwt_required
    @staticmethod
    def post():
        jti = get_raw_jwt()['jti']
        try:
            token = Token.find_by_jti(jti)
            token.revoked = True
            token.save()

            return {'message': 'Access token has been revoked'}
        except SQLAlchemyError:
            return {'message': 'Something went wrong'}, 500


class SecretResource(Resource):
    @jwt_required
    @staticmethod
    def get():
        return {'answer': 42}


api = Api(mod_auth)

api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(SecretResource, '/secret')
