import logging
from http import HTTPStatus
from typing import Any, Dict, List, Tuple

from flask import Flask, jsonify
from jsonschema import ValidationError
from werkzeug.exceptions import NotFound

from .response import Response

LOGGER: logging.Logger = logging.getLogger(__name__)


class InputValidationError(Exception):
    def __init__(self, errors: Dict[str, Any]) -> None:
        self.errors = errors

    @staticmethod
    def build_general_error(type: str) -> 'InputValidationError':
        return InputValidationError({'_general': {'type': type}})


class SchemaValidationError(Exception):
    def __init__(self, errors: List[ValidationError]) -> None:
        self.errors = errors


def register_error_handler(app: Flask) -> None:
    @app.errorhandler(Exception)
    def catch_all(error: Exception) -> Tuple[Response, int]:
        LOGGER.exception('Uncaught exception in endpoint: %s', error)
        return jsonify({'message': 'Internal Server Error'}), HTTPStatus.INTERNAL_SERVER_ERROR

    @app.errorhandler(InputValidationError)
    def input_validation_error(error: InputValidationError) -> Tuple[Response, int]:
        return jsonify(error.errors), HTTPStatus.BAD_REQUEST

    @app.errorhandler(NotFound)
    def not_found(error: NotFound) -> Tuple[Response, int]:
        return jsonify({'message': 'Not Found'}), HTTPStatus.NOT_FOUND

    @app.errorhandler(SchemaValidationError)
    def schema_validation_error(error: SchemaValidationError) -> Tuple[Response, int]:
        return jsonify([err.message for err in error.errors]), HTTPStatus.UNPROCESSABLE_ENTITY
