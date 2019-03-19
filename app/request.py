from typing import Any

import flask


def get_json() -> Any:
    return flask.request.get_json()
