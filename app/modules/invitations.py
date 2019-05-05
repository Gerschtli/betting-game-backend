import uuid
from typing import Dict, List

from flask import Blueprint
from flask_restful import Api

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
