from jsonschema import validators

from app.validator import schemas


def test_schemas() -> None:
    assert len([schema for schema in dir(schemas) if schema.isupper()]) == 3

    assert schemas.INVITATION == {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'additionalProperties': False,
        'type': 'object',
        'required': ['email', 'is_admin'],
        'properties': {
            'email': {
                'type': 'string',
            },
            'is_admin': {
                'type': 'boolean',
            },
        },
    }
    assert schemas.LOGIN == {
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
    assert schemas.USER == {
        '$schema': 'http://json-schema.org/draft-07/schema#',
        'additionalProperties': False,
        'type': 'object',
        'required': ['username', 'password', 'email', 'is_admin'],
        'properties': {
            'username': {
                'type': 'string',
            },
            'password': {
                'type': 'string',
            },
            'email': {
                'type': 'string',
            },
            'is_admin': {
                'type': 'boolean',
            },
        },
    }


def test_schema_validation() -> None:
    """
    Tests whether the schemas are valid. If not an jsonschema.exceptions.SchemaError is raised.
    """
    validators.Draft7Validator.check_schema(schemas.INVITATION)
    validators.Draft7Validator.check_schema(schemas.LOGIN)
    validators.Draft7Validator.check_schema(schemas.USER)
