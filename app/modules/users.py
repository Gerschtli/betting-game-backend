from flask import Blueprint, request
from flask_restful import Api

from ..models import User
from ..resource import Resource
from ..response import Response, no_content
from ..validator import matcher, schemas, validate_input, validate_schema

module = Blueprint('users', __name__, url_prefix='/users')
api = Api(module)


@api.resource('')
class Users(Resource):
    @validate_schema(schemas.USER)
    @validate_input({
        'username': matcher.And(
            matcher.NotBlank(),
            matcher.UniqueUsername(),
        ),
        'password': matcher.MinLength(6),
    })
    @staticmethod
    def post() -> Response:
        data = request.get_json()

        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password']),
        )
        new_user.save()

        return no_content()
