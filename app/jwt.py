from typing import Any, Dict

from flask_jwt_extended import JWTManager

from . import models

jwt = JWTManager()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token: Dict[str, Any]) -> bool:
    jti = decrypted_token['jti']
    return models.Token.is_jti_blacklisted(jti)


# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what the identity
# of the access token should be.
@jwt.user_identity_loader
def user_identity_lookup(user: models.User) -> int:
    return user.id
