INVITATION = {
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

LOGIN = {
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

USER = {
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
