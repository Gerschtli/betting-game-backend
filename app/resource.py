from typing import Any, Callable, Dict, List, TypeVar

import flask_jwt_extended
import flask_restful
import wrapt
from werkzeug.exceptions import Forbidden

RT = TypeVar('RT')


@wrapt.decorator
def admin_required(
        wrapped: Callable[..., RT],
        instance: Any,
        args: List[Any],
        kwargs: Dict[str, Any],
) -> RT:
    flask_jwt_extended.verify_jwt_in_request()
    claims = flask_jwt_extended.get_jwt_claims()

    if claims['is_admin']:
        return wrapped(*args, **kwargs)

    raise Forbidden()


class Resource(flask_restful.Resource):  # type: ignore
    pass


class AdminResource(Resource):
    method_decorators = [admin_required]


class AuthenticatedResource(Resource):
    method_decorators = [flask_jwt_extended.jwt_required]


class UserReadableResource(Resource):
    method_decorators = {
        'delete': [admin_required],
        'get': [flask_jwt_extended.jwt_required],
        'head': [flask_jwt_extended.jwt_required],
        'patch': [admin_required],
        'post': [admin_required],
        'put': [admin_required],
    }
