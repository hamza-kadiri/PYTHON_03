from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import object_session
from database import Base
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import current_app as app

subscriptions_table = Table('subscriptions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('tmdb_id_serie', Integer, ForeignKey('series.tmdb_id_serie'))
)

series_genres_table = Table('series_genres', Base.metadata,
    Column('tmdb_id_genre', Integer, ForeignKey('genres.tmdb_id_genre')),
    Column('tmdb_id_serie', Integer, ForeignKey('series.tmdb_id_serie'))
)

class Person():
    def __init__(self, id: int, credit_id: str, name: str):
        self.id = id
        self.credit_id = credit_id
        self.name = name
        self.profile_path = profile_path

class Actor(Person, Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    credit_id = Column(String)
    name = Column(String)
    profile_path = Column(String)
    department = Column(String)
    job = Column(String)

    def __init__(self, id: int, credit_id: str, name: str, profile_path: str, department: str, job: str):
        Person.__init__(self, id, credit_id, name, profile_path)
        self.department = department
        self.job = job

class Productor(Person, Base):
    __tablename__ = 'productors'
    id = Column(Integer, primary_key=True)
    credit_id = Column(String)
    name = Column(String)
    profile_path = Column(String)
    gender = Column(String)

    def __init__(self, id: int, credit_id: str, name: str, profile_path: str, gender: int):
        Person.__init(self, id, credit_id, name, profile_path)
        self.gender = gender

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    email = Column(String(80))
    password_hash = Column(String(128))
    series = relationship("Serie", secondary=subscriptions_table, back_populates="users")

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = User.hash_password(password)

    def as_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @classmethod
    def get_user_by_id(cls, id: int):
        return User.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_username(cls, username: str):
        return User.query.filter_by(username=username).first()

    @classmethod
    def hash_password(cls, password: str):
        return pwd_context.encrypt(password)

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
        return user    \

    @classmethod
    def get_subscription_by_user_id_and_serie_id(cls, user_id: int, tmdb_id_serie: int):
        return User.query.join(Serie, User.series).filter(User.id == user_id).filter(Serie.tmdb_id_serie == tmdb_id_serie).all()

class Serie(Base):
    __tablename__ = 'series'
    tmdb_id_serie = Column(Integer, primary_key=True)
    name = Column(String)
    overview = Column(String)
    backdrop_path = Column(String, nullable=True)
    nb_seasons = Column(Integer)
    nb_episodes = Column(Integer)
    next_air_date = Column(String)
    vote_count = Column(Integer)
    vote_average = Column(Numeric(3, 1))
    genres = relationship("Genre", secondary=series_genres_table, back_populates="series")
    users = relationship("User", secondary=subscriptions_table, back_populates="series")

    def __init__(self, tmdb_id_serie, name, overview, backdrop_path, nb_seasons, nb_episodes, next_air_date, vote_count, vote_average):
        self.tmdb_id_serie = tmdb_id_serie
        self.name = name
        self.overview = overview
        self.backdrop_path = backdrop_path
        self.nb_seasons = nb_seasons
        self.nb_episodes = nb_episodes
        self.next_air_date = next_air_date
        self.vote_count = vote_count
        self.vote_average = vote_average

    @classmethod
    def get_serie_by_id(cls, tmdb_id_serie: int):
        return Serie.query.filter_by(tmdb_id_serie=tmdb_id_serie).first()

    @classmethod
    def get_favorite_series_by_user_id(cls, userid):
        return Serie.query.join(User).filter(User.id == userid).all()

    @classmethod
    def from_json(cls, json):
        if json['next_episode_to_air'] != None:
            next_air_date = json['next_episode_to_air']['air_date']
        else:
            next_air_date = "null"
        return Serie(json['id'], json['name'], json['overview'], json['backdrop_path'], json['number_of_seasons'], json['number_of_episodes'], next_air_date, json['vote_count'], json['vote_average'])

class Genre(Base):
    __tablename__ = 'genres'
    tmdb_id_genre = Column(Integer, primary_key=True)
    name = Column(String)
    series = relationship("Serie", secondary=series_genres_table, back_populates="genres")

    def __init__(self, tmdb_id_genre, name):
        self.tmdb_id_genre = tmdb_id_genre
        self.name = name

    @classmethod
    def get_genre_from_id(cls, ids):
        return Genre.query(name).filter_by(tmdb_id_genre.in_(ids))

