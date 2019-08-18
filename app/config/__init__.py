from typing import Any, Optional

import flask


def get(key: str) -> Optional[Any]:
    return flask.current_app.config.get(key)
