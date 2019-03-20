from typing import Any, Dict

from flask_jwt_extended import JWTManager

from .models import Token

jwt = JWTManager()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token: Dict[str, Any]) -> bool:
    jti = decrypted_token['jti']
    return Token.is_jti_blacklisted(jti)
