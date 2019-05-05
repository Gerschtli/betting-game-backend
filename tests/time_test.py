import datetime

from freezegun import freeze_time

from app.time import get_invitation_expire


@freeze_time('2019-01-14')
def test_get_invitation_expire() -> None:
    assert get_invitation_expire() == datetime.datetime(2019, 1, 28)
