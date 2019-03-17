from typing import Any, Dict, List, Tuple

from flask import Flask, jsonify
from jsonschema import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from .response import Response


class InputValidationError(Exception):
    def __init__(self, errors: List[Dict[str, Any]]) -> None:
        self.errors = errors


class SchemaValidationError(Exception):
    def __init__(self, errors: List[ValidationError]) -> None:
        self.errors = errors


def register_error_handler(app: Flask) -> None:
    @app.errorhandler(InputValidationError)
    def input_validation_error(error: InputValidationError) -> Tuple[Response, int]:
        return jsonify(error.errors), 400

    @app.errorhandler(NotFound)
    def not_found(error: NotFound) -> Tuple[Response, int]:
        return jsonify({'message': 'Not Found'}), 404

    @app.errorhandler(SchemaValidationError)
    def schema_validation_error(error: SchemaValidationError) -> Tuple[Response, int]:
        return jsonify(error.errors), 422

    @app.errorhandler(SQLAlchemyError)
    def database_error(error: SQLAlchemyError) -> Tuple[Response, int]:
        return jsonify({'message': 'Internal Server Error'}), 500
