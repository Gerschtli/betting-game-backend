# pragma: no cover

import datetime

JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=8)
JWT_BLACKLIST_ENABLED = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
