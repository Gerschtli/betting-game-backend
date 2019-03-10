from typing import Any, Dict, List

from flask import jsonify
from jsonschema import ValidationError
from werkzeug.exceptions import BadRequest, UnprocessableEntity

from .response import Response


def _build_json_response(data: Any, code: int) -> Response:
    response = jsonify(data)
    response.status_code = code
    return response


class InputValidationError(BadRequest):
    def __init__(self, errors: Dict[str, Any]) -> None:
        response = _build_json_response(errors, self.code)
        super().__init__(response=response)


class SchemaValidationError(UnprocessableEntity):
    def __init__(self, errors: List[ValidationError]) -> None:
        response = _build_json_response([error.message for error in errors], self.code)
        super().__init__(response=response)
