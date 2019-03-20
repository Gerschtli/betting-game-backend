from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..models import User


def _error(type: str, path: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    error: Dict[str, Any] = {'type': type, 'path': path}
    if options is not None:
        error['options'] = options

    return error


class Matcher(ABC):
    @abstractmethod
    def validate(self, data: Any, path: str) -> List[Dict[str, Any]]:  # pragma: no cover
        pass


class And(Matcher):
    def __init__(self, *matchers: Matcher) -> None:
        self.matchers = matchers

    def validate(self, data: Any, path: str) -> List[Dict[str, Any]]:
        errors = []
        for matcher in self.matchers:
            errors.extend(matcher.validate(data, path))

        return errors


class MinLength(Matcher):
    def __init__(self, min_length: int) -> None:
        self.min_length = min_length

    def validate(self, data: str, path: str) -> List[Dict[str, Any]]:
        if len(data) >= self.min_length:
            return []

        return [_error('min_length', path, {'value': self.min_length})]


class NotBlank(Matcher):
    def validate(self, data: str, path: str) -> List[Dict[str, Any]]:
        if data:
            return []

        return [_error('not_blank', path)]


class UniqueUsername(Matcher):
    def validate(self, data: str, path: str) -> List[Dict[str, Any]]:
        if not User.find_by_username(data):
            return []

        return [_error('unique_username', path)]
