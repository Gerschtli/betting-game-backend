from typing import Any, Dict

from flask_jwt_extended import JWTManager

from . import models

jwt = JWTManager()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token: Dict[str, Any]) -> bool:
    jti = decrypted_token['jti']
    return models.Token.is_jti_blacklisted(jti)
