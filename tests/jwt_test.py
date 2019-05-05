from unittest.mock import Mock, patch

import pytest
from flask_jwt_extended import JWTManager

from app.jwt import (add_claims_to_access_token, check_if_token_in_blacklist, jwt,
                     user_identity_lookup)
from app.models import User


def test_init() -> None:
    assert isinstance(jwt, JWTManager)
    assert jwt._token_in_blacklist_callback == check_if_token_in_blacklist
    assert jwt._user_claims_callback == add_claims_to_access_token
    assert jwt._user_identity_callback == user_identity_lookup


@pytest.mark.parametrize(
    'is_admin',
    [True, False],
)
def test_add_claims_to_access_token(is_admin: bool) -> None:
    user = User(is_admin=is_admin)

    assert add_claims_to_access_token(user) == {'is_admin': is_admin}


@patch('app.models.Token')
def test_check_if_token_in_blacklist(mock_token: Mock) -> None:
    mock_token.is_jti_blacklisted = Mock(return_value=True)

    assert check_if_token_in_blacklist({'jti': 'token_jti'})

    mock_token.is_jti_blacklisted.assert_called_once_with('token_jti')


def test_user_identity_lookup() -> None:
    user = User(id=123)

    assert user_identity_lookup(user) == 123
