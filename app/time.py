import datetime


def get_invitation_expire() -> datetime.datetime:
    return datetime.datetime.now() + datetime.timedelta(days=14)
