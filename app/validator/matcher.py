from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..models import Invitation, User


def _error(type: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    error: Dict[str, Any] = {'type': type}
    if options is not None:
        error['options'] = options

    return error


class Matcher(ABC):
    @abstractmethod
    def validate(self, data: Any,
                 params: Dict[str, Any]) -> List[Dict[str, Any]]:  # pragma: no cover
        pass


class And(Matcher):
    def __init__(self, *matchers: Matcher) -> None:
        self.matchers = matchers

    def validate(self, data: Any, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        errors = []
        for matcher in self.matchers:
            errors.extend(matcher.validate(data, params))

        return errors


class MinLength(Matcher):
    def __init__(self, min_length: int) -> None:
        self.min_length = min_length

    def validate(self, data: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if len(data) >= self.min_length:
            return []

        return [_error('min_length', {'value': self.min_length})]


class Required(Matcher):
    def validate(self, data: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if data:
            return []

        return [_error('required')]


class UniqueInvitationEmail(Matcher):
    def __init__(self, ignore_id: bool = False) -> None:
        self.ignore_id = ignore_id

    def validate(self, data: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not Invitation.find_by_email(
                data,
                params['id'] if self.ignore_id else None,
        ):
            return []

        return [_error('unique_email')]


class UniqueUsername(Matcher):
    def validate(self, data: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not User.find_by_username(data):
            return []

        return [_error('unique_username')]
