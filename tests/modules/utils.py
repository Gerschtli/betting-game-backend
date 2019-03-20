from typing import Any, Callable, Dict, List, TypeVar
from unittest.mock import Mock

RT = TypeVar('RT')


def get_validator_schema(mock: Mock) -> Dict[str, Any]:
    mock.assert_called_once()
    args, kwargs = mock.call_args_list[0]

    assert len(args) == 4
    assert kwargs == {}

    return args[0]


def validator_call_through(schema: Dict[str, Any], wrapped: Callable[..., RT], args: List[Any],
                           kwargs: Dict[str, Any]) -> RT:
    return wrapped(*args, **kwargs)
