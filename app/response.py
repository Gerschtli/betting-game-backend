from http import HTTPStatus

from werkzeug.wrappers import Response


def no_content() -> Response:
    return Response(None, status=HTTPStatus.NO_CONTENT)
