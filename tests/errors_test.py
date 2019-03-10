from jsonschema import ValidationError

from app.errors import InputValidationError, SchemaValidationError


def test_input_validation_error() -> None:
    errors = {
        'abc': 'xy',
        'de': 1,
    }

    error = InputValidationError(errors)

    assert isinstance(error, Exception)
    assert errors == error.errors


def test_schema_validation_error() -> None:
    errors = [
        ValidationError("a"),
        ValidationError("b"),
    ]

    error = SchemaValidationError(errors)

    assert isinstance(error, Exception)
    assert errors == error.errors
