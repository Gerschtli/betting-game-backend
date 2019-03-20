import datetime

from app.config import default


def test_config() -> None:
    assert len([value for value in dir(default) if value.isupper()]) == 4

    assert default.PROPAGATE_EXCEPTIONS
    assert default.JWT_ACCESS_TOKEN_EXPIRES == datetime.timedelta(hours=8)
    assert default.JWT_BLACKLIST_ENABLED
    assert not default.SQLALCHEMY_TRACK_MODIFICATIONS
