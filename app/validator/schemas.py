USER = {
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
