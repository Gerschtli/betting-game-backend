from app.config import cli


def test_config() -> None:
    assert len([value for value in dir(cli) if value.isupper()]) == 3

    assert cli.SECRET_KEY == 'secret'
    assert cli.JWT_SECRET_KEY == 'jwt-secret-string'
    assert cli.SQLALCHEMY_DATABASE_URI == 'mysql://betting_game:testpw@192.168.56.101/betting_game'
