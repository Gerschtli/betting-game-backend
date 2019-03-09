from flask import jsonify
from werkzeug.exceptions import BadRequest, UnprocessableEntity


def _build_json_response(data, code):
    response = jsonify(data)
    response.status_code = code
    return response


class InputValidationError(BadRequest):
    def __init__(self, errors):
        response = _build_json_response(errors, self.code)
        super().__init__(self, response=response)


class SchemaValidationError(UnprocessableEntity):
    def __init__(self, errors):
        response = _build_json_response([error.message for error in errors], self.code)
        super().__init__(self, response=response)
