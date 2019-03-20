from jsonschema import validators

from app.validator import schemas


def test_schemas() -> None:
    assert len([schema for schema in dir(schemas) if schema.isupper()]) == 1

    assert schemas.USER == {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'additionalProperties': False,
        'type': 'object',
        'required': ['username', 'password'],
        'properties': {
            'username': {
                'type': 'string',
            },
            'password': {
                'type': 'string',
            },
        },
    }


def test_schema_validation() -> None:
    """
    Tests whether the schemas are valid. If not an jsonschema.exceptions.SchemaError is raised.
    """
    validators.Draft7Validator.check_schema(schemas.USER)
