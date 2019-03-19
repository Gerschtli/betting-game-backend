from http import HTTPStatus
from typing import NoReturn

from flask import Flask, Response
from jsonschema import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import NotFound

from app.errors import InputValidationError, SchemaValidationError, register_error_handler


class TestInputValidationError(object):
    def test_init(self) -> None:
        errors = [{
            'abc': 'xy',
            'de': 1,
        }, {
            'abc': '11',
            'de': 12,
        }]

        error = InputValidationError(errors)

        assert errors == error.errors

    def test_subclass(self) -> None:
        assert issubclass(InputValidationError, Exception)


class TestSchemaValidationError(object):
    def test_init(self) -> None:
        errors = [
            ValidationError('a'),
            ValidationError('b'),
        ]

        error = SchemaValidationError(errors)

        assert errors == error.errors

    def test_subclass(self) -> None:
        assert issubclass(SchemaValidationError, Exception)


class TestRegisterErrorHandler(object):
    def test_database_error(self, app: Flask) -> None:
        response = self._get_response(app, SQLAlchemyError())

        assert response.data == b'{"message":"Internal Server Error"}\n'
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_input_validation_error(self, app: Flask) -> None:
        response = self._get_response(app, InputValidationError([{'abc': 'def'}]))

        assert response.data == b'[{"abc":"def"}]\n'
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_not_found(self, app: Flask) -> None:
        response = self._get_response(app, NotFound())

        assert response.data == b'{"message":"Not Found"}\n'
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_schema_validation_error(self, app: Flask) -> None:
        response = self._get_response(
            app, SchemaValidationError([
                ValidationError('msg1'),
                ValidationError('msg2'),
            ]))

        assert response.data == b'["msg1","msg2"]\n'
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def _get_response(self, app: Flask, exception: Exception) -> Response:
        register_error_handler(app)

        @app.route('/')
        def test_route() -> NoReturn:
            raise exception

        client = app.test_client()

        response = client.get('/')

        assert response.is_json
        assert response.headers.get('Content-Type') == 'application/json'

        return response
