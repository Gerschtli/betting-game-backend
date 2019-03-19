import flask_restful
from flask_jwt_extended import jwt_required

from app.resource import AuthenticatedResource, Resource


def test_resource() -> None:
    assert issubclass(Resource, flask_restful.Resource)
    assert Resource.method_decorators == []


def test_authenticated_resource() -> None:
    assert issubclass(AuthenticatedResource, flask_restful.Resource)
    assert issubclass(AuthenticatedResource, Resource)
    assert AuthenticatedResource.method_decorators == [jwt_required]
