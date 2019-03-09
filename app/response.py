from werkzeug.wrappers import Response


def no_content():
    return Response(None, status=204)
