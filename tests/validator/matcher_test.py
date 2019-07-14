from unittest.mock import Mock, patch

import pytest

from app.validator.matcher import (And, Matcher, MinLength, Required, UniqueInvitationEmail,
                                   UniqueUsername)


class TestAnd(object):
    def test_subclass(self) -> None:
        assert issubclass(And, Matcher)

    def test_success(self) -> None:
        matcher1 = Mock('app.matcher.Matcher', autospec=True)
        matcher1.validate = Mock(return_value=[])
        matcher2 = Mock('app.matcher.Matcher', autospec=True)
        matcher2.validate = Mock(return_value=[])

        matcher = And(matcher1, matcher2)

        assert matcher.validate('data', {'test': 'value'}) == []

        matcher1.validate.assert_called_once_with('data', {'test': 'value'})
        matcher2.validate.assert_called_once_with('data', {'test': 'value'})

    def test_fail(self) -> None:
        matcher1 = Mock('app.matcher.Matcher', autospec=True)
        matcher1.validate = Mock(return_value=[{'error': 1}])
        matcher2 = Mock('app.matcher.Matcher', autospec=True)
        matcher2.validate = Mock(return_value=[{'error': 2}])

        matcher = And(matcher1, matcher2)

        assert matcher.validate('data', {'test': 'value'}) == [{'error': 1}, {'error': 2}]

        matcher1.validate.assert_called_once_with('data', {'test': 'value'})
        matcher2.validate.assert_called_once_with('data', {'test': 'value'})


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

        assert matcher.validate(value, {}) == []

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

        assert matcher.validate(value, {}) == [{
            'type': 'min',
            'options': {
                'value': 3
            },
        }]


class TestRequired(object):
    def test_subclass(self) -> None:
        assert issubclass(Required, Matcher)

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
        matcher = Required()

        assert matcher.validate(value, {}) == []

    def test_fail(self) -> None:
        matcher = Required()

        assert matcher.validate('', {}) == [{'type': 'required'}]


class TestUniqueInvitationEmail(object):
    def test_subclass(self) -> None:
        assert issubclass(UniqueInvitationEmail, Matcher)

    @patch('app.models.Invitation.find_by_email')
    def test_success(self, mock_find_by_email: Mock) -> None:
        mock_find_by_email.return_value = False

        matcher = UniqueInvitationEmail()

        assert matcher.validate('value', {'id': 123}) == []

        mock_find_by_email.assert_called_once_with('value', None)

    @patch('app.models.Invitation.find_by_email')
    def test_fail(self, mock_find_by_email: Mock) -> None:
        mock_find_by_email.return_value = True

        matcher = UniqueInvitationEmail()

        assert matcher.validate('value', {'id': 123}) == [{'type': 'unique_email'}]

        mock_find_by_email.assert_called_once_with('value', None)

    @patch('app.models.Invitation.find_by_email')
    def test_success_with_id(self, mock_find_by_email: Mock) -> None:
        mock_find_by_email.return_value = False

        matcher = UniqueInvitationEmail(True)

        assert matcher.validate('value', {'id': 123}) == []

        mock_find_by_email.assert_called_once_with('value', 123)

    @patch('app.models.Invitation.find_by_email')
    def test_fail_with_id(self, mock_find_by_email: Mock) -> None:
        mock_find_by_email.return_value = True

        matcher = UniqueInvitationEmail(True)

        assert matcher.validate('value', {'id': 123}) == [{'type': 'unique_email'}]

        mock_find_by_email.assert_called_once_with('value', 123)


class TestUniqueUsername(object):
    def test_subclass(self) -> None:
        assert issubclass(UniqueUsername, Matcher)

    @patch('app.models.User.find_by_username')
    def test_success(self, mock_find_by_username: Mock) -> None:
        mock_find_by_username.return_value = False

        matcher = UniqueUsername()

        assert matcher.validate('value', {}) == []

        mock_find_by_username.assert_called_once_with('value')

    @patch('app.models.User.find_by_username')
    def test_fail(self, mock_find_by_username: Mock) -> None:
        mock_find_by_username.return_value = True

        matcher = UniqueUsername()

        assert matcher.validate('value', {}) == [{'type': 'unique_username'}]

        mock_find_by_username.assert_called_once_with('value')
