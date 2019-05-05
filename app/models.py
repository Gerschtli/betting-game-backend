from typing import List

from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256 as sha256

db = SQLAlchemy()


class _SaveMixin(object):
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()


class Invitation(db.Model, _SaveMixin):  # type: ignore
    __tablename__ = 'invitation'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    @classmethod
    def find_by_email(cls, email: str) -> 'Invitation':
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_all(cls) -> List['Invitation']:
        return cls.query.all()


class Token(db.Model, _SaveMixin):  # type: ignore
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)

    @classmethod
    def find_by_jti(cls, jti: str) -> 'Token':
        return cls.query.filter_by(jti=jti).first()

    @classmethod
    def is_jti_blacklisted(cls, jti: str) -> bool:
        query = cls.query.filter_by(jti=jti, revoked=True).first()
        return bool(query)


class User(db.Model, _SaveMixin):  # type: ignore
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    @classmethod
    def find_by_username(cls, username: str) -> 'User':
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password: str) -> str:
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> bool:
        return sha256.verify(password, hash)
