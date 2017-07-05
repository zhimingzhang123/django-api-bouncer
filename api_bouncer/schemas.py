plugins = {
    'key-auth': {
        'type': 'object',
        'properties': {
            'key_names': {
                'type': 'array',
            },
            'key_in_body': {
                'type': 'boolean',
            },
            'hide_credentials': {
                'type': 'boolean',
            },
            'anonymous': {
                'type': 'string',
            }
        },
        'required': ['key_names'],
        'additionalProperties': False
    },
    'ip-restriction': {
        'type': 'object',
        'properties': {
            'whitelist': {
                'type': 'array',
            },
            'blacklist': {
                'type': 'array',
            },
            'consumer_id': {
                'type': 'string',
            }
        },
        'additionalProperties': False
    },
}

defaults = {
    'key-auth': {
        'key_names': ['apikey'],
        'key_in_body': False,
        'hide_credentials': False,
        'anonymous': '',
    },
    'ip-restriction': {
        'consumer_id': '',
        'whitelist': [],
        'blacklist': [],
    },
}
