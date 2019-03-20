from flask_jwt_extended import JWTManager

from app.jwt import jwt


def test_init() -> None:
    assert isinstance(jwt, JWTManager)
