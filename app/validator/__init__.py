from functools import wraps
from typing import Any, Dict

import jsonschema
from flask import request

from ..errors import InputValidationError, SchemaValidationError
from .matcher import Matcher


def validate_input(schema: Dict[str, Matcher]):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            errors = []
            data = request.get_json()

            for key in schema:
                errors.extend(schema[key].validate(data[key], key))

            if errors:
                raise InputValidationError(errors)

            return fn(*args, **kwargs)

        return decorated

    return wrapper


def validate_schema(schema: Dict[str, Any]):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            schema["$schema"] = "http://json-schema.org/draft-07/schema#"
            schema["additionalProperties"] = False

            validator = jsonschema.validators.Draft7Validator(schema)
            errors = list(validator.iter_errors(request.get_json()))

            if len(errors) > 0:
                raise SchemaValidationError(errors)

            return fn(*args, **kwargs)

        return decorated

    return wrapper
