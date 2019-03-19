from app.validator import schemas


def test_schemas() -> None:
    assert len([schema for schema in dir(schemas) if schema.isupper()]) == 1

    assert schemas.USER == {
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
