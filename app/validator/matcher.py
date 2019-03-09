from abc import ABC, abstractmethod

from ..models import User


def _error(type, path, options=None):
    dict = {'type': type, 'path': path}
    if options is not None:
        dict['options'] = options

    return dict


class Matcher(ABC):
    @abstractmethod
    def validate(self, data, path):
        pass


class And(Matcher):
    def __init__(self, *matchers):
        self._matchers = matchers

    def validate(self, data, path):
        errors = []
        for matcher in self._matchers:
            errors.extend(matcher.validate(data, path))

        return errors


class MinLength(Matcher):
    def __init__(self, min_length):
        self._min_length = min_length

    def validate(self, data, path):
        if len(data) >= self._min_length:
            return []

        return [_error('min_length', path, {'value': self._min_length})]


class NotBlank(Matcher):
    def validate(self, data, path):
        if data:
            return []

        return [_error('not_blank', path)]


class UniqueUsername(Matcher):
    def validate(self, data, path):
        if not User.find_by_username(data):
            return []

        return [_error('unique_username', path)]
