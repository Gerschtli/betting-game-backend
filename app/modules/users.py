from flask import Blueprint
from flask_restful import Api

from .. import models, request
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
            matcher.Required(),
            matcher.UniqueUsername(),
        ),
        'password': matcher.MinLength(6),
        'email': matcher.Required(),
    })
    @staticmethod
    def post() -> Response:
        data = request.get_json()

        new_user = models.User(
            username=data['username'],
            password=models.User.generate_hash(data['password']),
            email=data['email'],
            is_admin=data['is_admin'],
        )
        new_user.save()

        return no_content()
