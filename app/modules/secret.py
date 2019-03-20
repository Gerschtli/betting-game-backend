from typing import Dict

from flask import Blueprint
from flask_restful import Api

from ..resource import AuthenticatedResource

module = Blueprint('secret', __name__, url_prefix='/secret')
api = Api(module)


@api.resource('')
class SecretResource(AuthenticatedResource):
    @staticmethod
    def get() -> Dict[str, int]:  # pragma: no cover
        return {'answer': 42}
