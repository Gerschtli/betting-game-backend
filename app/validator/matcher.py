from abc import ABC, abstractmethod

from ..models import User


class Matcher(ABC):
    @abstractmethod
    def is_valid(self, data):
        pass

    def options(self):
        return {}

    @abstractmethod
    def type(self):
        pass


class MinLength(Matcher):
    def __init__(self, min_length):
        self._min_length = min_length

    def is_valid(self, data):
        return len(data) >= self._min_length

    def options(self):
        return {'value': self._min_length}

    def type(self):
        return 'min_length'


class UniqueUsername(Matcher):
    def is_valid(self, data):
        return not User.find_by_username(data)

    def type(self):
        return 'unique_username'
