from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, UniqueConstraint
from database import Base
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import current_app as app

# TODO : Add encapsulation

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    email = Column(String(80))
    password_hash = Column(String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = User.hash_password(password)

    # TODO : Add subscriptions / favorites series
    def as_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'password': self.password}

    @classmethod
    def get_user_by_id(cls, id: int):
        return User.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_username(cls, username:str):
        return User.query.filter_by(username=username).first()

    @classmethod
    def hash_password(cls, password:str):
        return pwd_context.encrypt(password)

    def verify_password(self, password:str):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.get_user_by_id(data['id'])
        return user

# TODO : Add genre (commented out because it is, in fact, a many-to-many relationship)
class Serie(Base):
    __tablename__ = 'series'
    id_tmdb = Column(Integer, primary_key=True)
    name = Column(String)
    overview = Column(String)
    backdrop_path = Column(String, nullable=True)
    # genre_id_tmdb = Column(Integer, ForeignKey('genres.id_tmdb'))
    vote_count = Column(Integer)
    vote_average = Column(Numeric(3, 1))

    def __init__(self, id_tmdb, name, overview, backdrop_path, tmdb_id_genre, vote_count, vote_average):
        self.id_tmdb = id_tmdb
        self.name = name
        self.overview = overview
        self.backdrop_path = backdrop_path
        self.tmdb_id_genre = tmdb_id_genre
        self.vote_count = vote_count
        self.vote_average = vote_average

    @classmethod
    def get_serie_by_id(cls, id_tmdb: int):
        return Serie.query.filter_by(id_tmdb=id_tmdb).first()

    @classmethod
    def from_json(cls, json):
        return Serie(json['id'], json['name'], json['overview'], json['backdrop_path'], 1, json['vote_count'],
                     json['vote_average'])


class Genre(Base):
    __tablename__ = 'genres'
    id_tmdb = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, tmdb_id_genre, name):
        self.tmdb_id_genre = tmdb_id_genre
        self.name = name


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    serie_id = Column(Integer, ForeignKey('series.id_tmdb'))

    def __init__(self, user_id, serie_id):
        self.user_id = user_id
        self.serie_id = serie_id

    def as_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'serie_id': self.serie_id}
