from typing import Any, Callable, Dict, List, TypeVar

import jsonschema
import wrapt
from flask import request

from ..errors import InputValidationError, SchemaValidationError
from .matcher import Matcher

RT = TypeVar('RT')


def validate_input(schema: Dict[str, Matcher]) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    @wrapt.decorator
    def wrapper(wrapped: Callable[..., RT], instance: Any, args: List[Any],
                kwargs: Dict[str, Any]) -> RT:
        errors = []
        data = request.get_json()

        for key in schema:
            errors.extend(schema[key].validate(data[key], key))

        if errors:
            raise InputValidationError(errors)

        return wrapped(*args, **kwargs)

    return wrapper


def validate_schema(schema: Dict[str, Any]) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    schema["$schema"] = "http://json-schema.org/draft-07/schema#"
    schema["additionalProperties"] = False

    validator = jsonschema.validators.Draft7Validator(schema)

    @wrapt.decorator
    def wrapper(wrapped: Callable[..., RT], instance: Any, args: List[Any],
                kwargs: Dict[str, Any]) -> RT:
        errors = list(validator.iter_errors(request.get_json()))

        if errors:
            raise SchemaValidationError(errors)

        return wrapped(*args, **kwargs)

    return wrapper
