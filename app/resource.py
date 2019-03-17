import flask_restful
from flask_jwt_extended import jwt_required


class Resource(flask_restful.Resource):  # type: ignore
    pass


class AuthenticatedResource(Resource):
    method_decorators = [jwt_required]
