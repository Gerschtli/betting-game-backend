import uuid
from typing import Dict, List

from flask import Blueprint
from flask_restful import Api
from werkzeug.exceptions import NotFound

from .. import models, request, time
from ..resource import AdminResource
from ..response import Response, no_content
from ..validator import matcher, schemas, validate_input, validate_schema

module = Blueprint('invitations', __name__, url_prefix='/invitations')
api = Api(module)


@api.resource('')
class Invitations(AdminResource):
    @staticmethod
    def get() -> List[Dict[str, str]]:
        invitations = models.Invitation.get_all()

        result = []
        for invitation in invitations:
            result.append({
                'id': invitation.id,
                'email': invitation.email,
                'is_admin': invitation.is_admin,
            })

        return result

    @validate_schema(schemas.INVITATION)
    @validate_input({
        'email': matcher.And(
            matcher.NotBlank(),
            matcher.UniqueInvitationEmail(),
        ),
    })
    @staticmethod
    def post() -> Response:
        data = request.get_json()

        invitation = models.Invitation(
            email=data['email'],
            is_admin=data['is_admin'],
            token=uuid.uuid4(),
            expires=time.get_invitation_expire(),
        )
        invitation.save()

        return no_content()


@api.resource('/<int:id>')
class Invitation(AdminResource):
    @validate_schema(schemas.INVITATION)
    @validate_input({
        'email':
        matcher.And(
            matcher.NotBlank(),
            matcher.UniqueInvitationEmail(ignore_id=True),
        ),
    })
    @staticmethod
    def put(id: int) -> Response:
        data = request.get_json()

        invitation = models.Invitation.find_by_id(id)
        if invitation is None:
            raise NotFound()

        invitation.email = data['email']
        invitation.is_admin = data['is_admin']
        invitation.save()

        return no_content()

    @staticmethod
    def delete(id: int) -> Response:
        invitation = models.Invitation.find_by_id(id)
        if invitation is not None:
            invitation.delete()

        return no_content()
