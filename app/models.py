import datetime

from passlib.hash import pbkdf2_sha256 as sha256

from . import db


class _SaveMixin(object):
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()


class User(db.Model, _SaveMixin):  # type: ignore
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @classmethod
    def find_by_username(cls, username: str) -> 'User':
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password: str) -> str:
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password: str, hash: str) -> bool:
        return sha256.verify(password, hash)


class Token(db.Model, _SaveMixin):  # type: ignore
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    expires = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    revoked = db.Column(db.Boolean, nullable=False)

    @classmethod
    def find_by_jti(cls, jti: str) -> 'Token':
        return cls.query.filter_by(jti=jti).first()

    @classmethod
    def is_jti_blacklisted(cls, jti: str) -> bool:
        query = cls.query.filter_by(jti=jti, revoked=True).first()
        return bool(query)
