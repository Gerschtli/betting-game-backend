from unittest.mock import Mock, patch

import pytest

from app.validator.matcher import And, Matcher, MinLength, NotBlank, UniqueUsername


class TestAnd(object):
    def test_subclass(self) -> None:
        assert issubclass(And, Matcher)

    def test_success(self) -> None:
        matcher1 = Mock('app.matcher.Matcher', autospec=True)
        matcher1.validate = Mock(return_value=[])
        matcher2 = Mock('app.matcher.Matcher', autospec=True)
        matcher2.validate = Mock(return_value=[])

        matcher = And(matcher1, matcher2)

        assert matcher.validate('data', 'path') == []

        matcher1.validate.assert_called_once_with('data', 'path')
        matcher2.validate.assert_called_once_with('data', 'path')

    def test_fail(self) -> None:
        matcher1 = Mock('app.matcher.Matcher', autospec=True)
        matcher1.validate = Mock(return_value=[{'error': 1}])
        matcher2 = Mock('app.matcher.Matcher', autospec=True)
        matcher2.validate = Mock(return_value=[{'error': 2}])

        matcher = And(matcher1, matcher2)

        assert matcher.validate('data', 'path') == [{'error': 1}, {'error': 2}]

        matcher1.validate.assert_called_once_with('data', 'path')
        matcher2.validate.assert_called_once_with('data', 'path')


class TestMinLength(object):
    def test_subclass(self) -> None:
        assert issubclass(MinLength, Matcher)

    @pytest.mark.parametrize(
        'value',
        [
            '123',
            '1234',
            '12345',
        ],
    )
    def test_success(self, value: str) -> None:
        matcher = MinLength(3)

        assert matcher.validate(value, 'path') == []

    @pytest.mark.parametrize(
        'value',
        [
            '',
            '1',
            '12',
        ],
    )
    def test_fail(self, value: str) -> None:
        matcher = MinLength(3)

        assert matcher.validate(value, 'path') == [{
            'type': 'min_length',
            'path': 'path',
            'options': {
                'value': 3
            },
        }]


class TestNotBlank(object):
    def test_subclass(self) -> None:
        assert issubclass(NotBlank, Matcher)

    @pytest.mark.parametrize(
        'value',
        [
            '0',
            'False',
            'None',
            'abc',
        ],
    )
    def test_success(self, value: str) -> None:
        matcher = NotBlank()

        assert matcher.validate(value, 'path') == []

    def test_fail(self) -> None:
        matcher = NotBlank()

        assert matcher.validate('', 'path') == [{
            'type': 'not_blank',
            'path': 'path',
        }]


class TestUniqueUsername(object):
    def test_subclass(self) -> None:
        assert issubclass(UniqueUsername, Matcher)

    @patch('app.models.User.find_by_username')
    def test_success(self, mock_find_by_username: Mock) -> None:
        mock_find_by_username.return_value = False

        matcher = UniqueUsername()

        assert matcher.validate('value', 'path') == []

        mock_find_by_username.assert_called_once_with('value')

    @patch('app.models.User.find_by_username')
    def test_fail(self, mock_find_by_username: Mock) -> None:
        mock_find_by_username.return_value = True

        matcher = UniqueUsername()

        assert matcher.validate('value', 'path') == [{
            'type': 'unique_username',
            'path': 'path',
        }]

        mock_find_by_username.assert_called_once_with('value')
