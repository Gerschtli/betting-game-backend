from app.config import dev


def test_config() -> None:
    assert len([value for value in dir(dev) if value.isupper()]) == 3

    assert dev.SECRET_KEY == 'secret'
    assert dev.JWT_SECRET_KEY == 'jwt-secret-string'
    assert dev.SQLALCHEMY_DATABASE_URI == 'mysql://betting_game:testpw@localhost/betting_game'
