from unittest.mock import Mock, patch

import flask_restful
from flask_jwt_extended import jwt_required
from flask_jwt_extended.exceptions import UserClaimsVerificationError
from werkzeug.exceptions import Forbidden

from app.resource import (AdminResource, AuthenticatedResource, Resource, UserReadableResource,
                          admin_required)


@patch('flask_jwt_extended.get_jwt_claims')
@patch('flask_jwt_extended.verify_jwt_in_request')
def test_admin_required(mock_verify_jwt_in_request: Mock, mock_get_jwt_claims: Mock) -> None:
    called = False

    @admin_required
    def function(arg1: str, arg2: int) -> int:
        nonlocal called
        called = True

        assert arg1 == 'bla'
        assert arg2 == 342

        return 17

    mock_get_jwt_claims.return_value = {'is_admin': True}

    result = function('bla', arg2=342)

    mock_verify_jwt_in_request.assert_called_once_with()
    mock_get_jwt_claims.assert_called_once_with()

    assert result == 17


@patch('flask_jwt_extended.get_jwt_claims')
@patch('flask_jwt_extended.verify_jwt_in_request')
def test_admin_required_when_not_admin(mock_verify_jwt_in_request: Mock,
                                       mock_get_jwt_claims: Mock) -> None:
    called = False

    @admin_required
    def function() -> None:
        nonlocal called
        called = True

    mock_get_jwt_claims.return_value = {'is_admin': False}

    exception = None
    try:
        function()
    except Exception as e:
        exception = e

    mock_verify_jwt_in_request.assert_called_once_with()
    mock_get_jwt_claims.assert_called_once_with()

    assert exception is not None
    assert isinstance(exception, Forbidden)


@patch('flask_jwt_extended.get_jwt_claims')
@patch('flask_jwt_extended.verify_jwt_in_request')
def test_admin_required_with_invalid_jwt(mock_verify_jwt_in_request: Mock,
                                         mock_get_jwt_claims: Mock) -> None:
    called = False

    @admin_required
    def function() -> None:
        nonlocal called
        called = True

    mock_verify_jwt_in_request.side_effect = UserClaimsVerificationError('error')

    exception = None
    try:
        function()
    except Exception as e:
        exception = e

    mock_verify_jwt_in_request.assert_called_once_with()
    mock_get_jwt_claims.assert_not_called()

    assert exception is not None
    assert isinstance(exception, UserClaimsVerificationError)


def test_resource() -> None:
    assert issubclass(Resource, flask_restful.Resource)
    assert Resource.method_decorators == []


def test_admin_resource() -> None:
    assert issubclass(AdminResource, flask_restful.Resource)
    assert issubclass(AdminResource, Resource)
    assert AdminResource.method_decorators == [admin_required]


def test_authenticated_resource() -> None:
    assert issubclass(AuthenticatedResource, flask_restful.Resource)
    assert issubclass(AuthenticatedResource, Resource)
    assert AuthenticatedResource.method_decorators == [jwt_required]


def test_user_readable_resource() -> None:
    assert issubclass(UserReadableResource, flask_restful.Resource)
    assert issubclass(UserReadableResource, Resource)
    assert UserReadableResource.method_decorators == {
        'delete': [admin_required],
        'get': [jwt_required],
        'head': [jwt_required],
        'patch': [admin_required],
        'post': [admin_required],
        'put': [admin_required],
    }
