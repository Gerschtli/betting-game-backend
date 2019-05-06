from typing import Any, Callable, Dict, List, TypeVar

import wrapt
from jsonschema import validators

from .. import request
from ..errors import InputValidationError, SchemaValidationError
from .matcher import Matcher

RT = TypeVar('RT')


def _validate_input(schema: Dict[str, Matcher], wrapped: Callable[..., RT], args: List[Any],
                    kwargs: Dict[str, Any]) -> RT:
    errors = []
    data = request.get_json()

    for key in schema:
        errors.extend(schema[key].validate(data[key], key, kwargs))

    if errors:
        raise InputValidationError(errors)

    return wrapped(*args, **kwargs)


def validate_input(schema: Dict[str, Matcher]) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    @wrapt.decorator
    def wrapper(wrapped: Callable[..., RT], instance: Any, args: List[Any],
                kwargs: Dict[str, Any]) -> RT:
        return _validate_input(schema, wrapped, args, kwargs)

    return wrapper


def _validate_schema(schema: Dict[str, Any], wrapped: Callable[..., RT], args: List[Any],
                     kwargs: Dict[str, Any]) -> RT:
    validator = validators.Draft7Validator(schema)
    errors = list(validator.iter_errors(request.get_json()))

    if errors:
        raise SchemaValidationError(errors)

    return wrapped(*args, **kwargs)


def validate_schema(schema: Dict[str, Any]) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    @wrapt.decorator
    def wrapper(wrapped: Callable[..., RT], instance: Any, args: List[Any],
                kwargs: Dict[str, Any]) -> RT:
        return _validate_schema(schema, wrapped, args, kwargs)

    return wrapper
