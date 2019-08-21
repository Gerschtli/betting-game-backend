from typing import Dict, List

from flask import Blueprint
from flask_restful import Api
from werkzeug.exceptions import NotFound

from .. import config, mail, models, request, time, uuid
from ..errors import InputValidationError
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
            matcher.Required(),
            matcher.UniqueInvitationEmail(),
        ),
    })
    @staticmethod
    def post() -> Response:
        data = request.get_json()

        email = data['email']
        token = uuid.generate()
        link = '{}/invitation/{}'.format(config.get('APP_BASE_URL'), token)

        success = mail.send_mail(email, 'invitation', {
            'project_name': config.get('APP_PROJECT_NAME'),
            'link': link,
        })

        if not success:
            raise InputValidationError.build_general_error('mailSendFailed')

        invitation = models.Invitation(
            email=email,
            is_admin=data['is_admin'],
            token=token,
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
            matcher.Required(),
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
