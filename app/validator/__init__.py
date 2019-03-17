from functools import wraps
from typing import Any, Callable, Dict, TypeVar

import jsonschema
from flask import request

from ..errors import InputValidationError, SchemaValidationError
from .matcher import Matcher

RT = TypeVar('RT')


def validate_input(schema: Dict[str, Matcher]) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    def wrapper(fn: Callable[..., RT]) -> Callable[..., RT]:
        @wraps(fn)
        def decorated(*args: Any, **kwargs: Any) -> RT:
            errors = []
            data = request.get_json()

            for key in schema:
                errors.extend(schema[key].validate(data[key], key))

            if errors:
                raise InputValidationError(errors)

            return fn(*args, **kwargs)

        return decorated

    return wrapper


def validate_schema(schema: Dict[str, Any]) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    schema["$schema"] = "http://json-schema.org/draft-07/schema#"
    schema["additionalProperties"] = False

    validator = jsonschema.validators.Draft7Validator(schema)

    def wrapper(fn: Callable[..., RT]) -> Callable[..., RT]:
        @wraps(fn)
        def decorated(*args: Any, **kwargs: Any) -> RT:
            errors = list(validator.iter_errors(request.get_json()))

            if errors:
                raise SchemaValidationError(errors)

            return fn(*args, **kwargs)

        return decorated

    return wrapper
