from werkzeug.wrappers import Response


def no_content() -> Response:
    return Response(None, status=204)
