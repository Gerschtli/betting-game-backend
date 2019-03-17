from jsonschema import ValidationError

from app.errors import InputValidationError, SchemaValidationError


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
            ValidationError("a"),
            ValidationError("b"),
        ]

        error = SchemaValidationError(errors)

        assert errors == error.errors

    def test_subclass(self) -> None:
        assert issubclass(SchemaValidationError, Exception)
