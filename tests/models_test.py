from typing import Optional
from unittest.mock import Mock, patch

import pytest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.elements import BinaryExpression

from app.models import Invitation, Token, User, db


def test_init() -> None:
    assert isinstance(db, SQLAlchemy)


def _helper_column(  # type: ignore
        column: db.Column,
        name: str,
        type_cls,
        primary_key: bool = False,
        nullable: bool = True,
        unique: Optional[bool] = None,
        string_length: Optional[int] = None,
) -> None:
    assert column.key == name
    assert column.name == name
    assert isinstance(column.type, type_cls)
    assert column.primary_key == primary_key
    assert column.nullable == nullable
    assert column.unique == unique

    if string_length is not None:
        assert column.type.length == string_length


class _BinaryExpressionMatcher(object):
    def __init__(self, expected: BinaryExpression) -> None:
        self._expected = expected

    def __eq__(self, actual: BinaryExpression) -> bool:
        return self._expected.compare(actual)


class TestInvitation(object):
    def test_subclass(self) -> None:
        assert issubclass(User, db.Model)

    def test_properties(self) -> None:
        assert Invitation.__tablename__ == 'invitation'
        assert len(Invitation.__table__.columns) == 5

        _helper_column(
            Invitation.__table__.columns.id,
            'id',
            db.Integer,
            primary_key=True,
            nullable=False,
        )
        _helper_column(
            Invitation.__table__.columns.email,
            'email',
            db.String,
            nullable=False,
            unique=True,
            string_length=255,
        )
        _helper_column(
            Invitation.__table__.columns.is_admin,
            'is_admin',
            db.Boolean,
            nullable=False,
        )
        _helper_column(
            Invitation.__table__.columns.token,
            'token',
            db.String,
            nullable=False,
            unique=True,
            string_length=255,
        )
        _helper_column(
            Token.__table__.columns.expires,
            'expires',
            db.DateTime,
            nullable=False,
        )

    def test_delete(self) -> None:
        db.session.delete = Mock()
        db.session.commit = Mock()

        invitation = Invitation(id=123)
        invitation.delete()

        db.session.delete.assert_called_once_with(invitation)
        db.session.commit.assert_called_once_with()

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_find_by_email(self, mock_query: Mock) -> None:
        expected = Invitation(id=123)

        filter_by = mock_query.return_value.filter_by
        first = filter_by.return_value.first
        first.return_value = expected

        result = Invitation.find_by_email('name-xyz', None)

        filter_by.assert_called_once_with(email='name-xyz')
        first.assert_called_once_with()

        assert result == expected

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_find_by_email_with_id(self, mock_query: Mock) -> None:
        expected = Invitation(id=123)

        filter_by = mock_query.return_value.filter_by
        filter = filter_by.return_value.filter
        first = filter.return_value.first
        first.return_value = expected

        result = Invitation.find_by_email('name-xyz', 654)

        filter_by.assert_called_once_with(email='name-xyz')
        filter.assert_called_once_with(_BinaryExpressionMatcher(Invitation.id != 654))
        first.assert_called_once_with()

        assert result == expected

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_find_by_id(self, mock_query: Mock) -> None:
        expected = Invitation(id=123)

        filter_by = mock_query.return_value.filter_by
        first = filter_by.return_value.first
        first.return_value = expected

        result = Invitation.find_by_id(123)

        filter_by.assert_called_once_with(id=123)
        first.assert_called_once_with()

        assert result == expected

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_get_all(self, mock_query: Mock) -> None:
        expected = [Invitation(id=123)]

        all = mock_query.return_value.all
        all.return_value = expected

        result = Invitation.get_all()

        all.assert_called_once_with()

        assert result == expected

    def test_save(self) -> None:
        db.session.add = Mock()
        db.session.commit = Mock()

        invitation = Invitation(id=123)
        invitation.save()

        db.session.add.assert_called_once_with(invitation)
        db.session.commit.assert_called_once_with()


class TestToken(object):
    def test_subclass(self) -> None:
        assert issubclass(User, db.Model)

    def test_properties(self) -> None:
        assert Token.__tablename__ == 'token'
        assert len(Token.__table__.columns) == 5

        _helper_column(
            Token.__table__.columns.id,
            'id',
            db.Integer,
            primary_key=True,
            nullable=False,
        )
        _helper_column(
            Token.__table__.columns.jti,
            'jti',
            db.String,
            nullable=False,
            string_length=255,
        )
        _helper_column(
            Token.__table__.columns.user_id,
            'user_id',
            db.Integer,
            nullable=False,
        )
        _helper_column(
            Token.__table__.columns.expires,
            'expires',
            db.DateTime,
            nullable=False,
        )
        _helper_column(
            Token.__table__.columns.revoked,
            'revoked',
            db.Boolean,
            nullable=False,
        )

        # TODO: test user_id foreign_key

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_find_by_jti(self, mock_query: Mock) -> None:
        expected = Token(id=123)

        filter_by = mock_query.return_value.filter_by
        first = filter_by.return_value.first
        first.return_value = expected

        result = Token.find_by_jti('name-xyz')

        filter_by.assert_called_once_with(jti='name-xyz')
        first.assert_called_once_with()

        assert result == expected

    @pytest.mark.parametrize(
        'return_value,expected',
        [
            (Token(id=123), True),
            (None, False),
        ],
    )
    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_is_jti_blacklisted(self, mock_query: Mock, return_value: Optional[Token],
                                expected: bool) -> None:
        filter_by = mock_query.return_value.filter_by
        first = filter_by.return_value.first
        first.return_value = return_value

        result = Token.is_jti_blacklisted('name-xyz')

        filter_by.assert_called_once_with(jti='name-xyz', revoked=True)
        first.assert_called_once_with()

        assert result == expected

    def test_save(self) -> None:
        db.session.add = Mock()
        db.session.commit = Mock()

        token = Token(id=123)
        token.save()

        db.session.add.assert_called_once_with(token)
        db.session.commit.assert_called_once_with()


class TestUser(object):
    def test_subclass(self) -> None:
        assert issubclass(User, db.Model)

    def test_properties(self) -> None:
        assert User.__tablename__ == 'user'
        assert len(User.__table__.columns) == 5

        _helper_column(
            User.__table__.columns.id,
            'id',
            db.Integer,
            primary_key=True,
            nullable=False,
        )
        _helper_column(
            User.__table__.columns.username,
            'username',
            db.String,
            nullable=False,
            unique=True,
            string_length=255,
        )
        _helper_column(
            User.__table__.columns.password,
            'password',
            db.String,
            nullable=False,
            string_length=255,
        )
        _helper_column(
            User.__table__.columns.email,
            'email',
            db.String,
            nullable=False,
            string_length=255,
        )
        _helper_column(
            User.__table__.columns.is_admin,
            'is_admin',
            db.Boolean,
            nullable=False,
        )

    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_find_by_username(self, mock_query: Mock) -> None:
        expected = User(id=123)

        filter_by = mock_query.return_value.filter_by
        first = filter_by.return_value.first
        first.return_value = expected

        result = User.find_by_username('name-xyz')

        filter_by.assert_called_once_with(username='name-xyz')
        first.assert_called_once_with()

        assert result == expected

    @patch('passlib.hash.pbkdf2_sha256.hash')
    def test_generate_hash(self, mock_hash: Mock) -> None:
        mock_hash.return_value = 'haashi'

        result = User.generate_hash('gesundheit')

        mock_hash.assert_called_once_with('gesundheit')

        assert result == 'haashi'

    def test_save(self) -> None:
        db.session.add = Mock()
        db.session.commit = Mock()

        user = User(id=123)
        user.save()

        db.session.add.assert_called_once_with(user)
        db.session.commit.assert_called_once_with()

    @patch('passlib.hash.pbkdf2_sha256.verify')
    def test_verify_hash(self, mock_hash: Mock) -> None:
        mock_hash.return_value = True

        result = User.verify_hash('gesundheit', 'haashi')

        mock_hash.assert_called_once_with('gesundheit', 'haashi')

        assert result
