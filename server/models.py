from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, UniqueConstraint
from database import Base

# TODO : Add encapsulation

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20))
    email = Column(String(80))
    password = Column(String(20))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    # TODO : Add subscriptions / favorites series
    def as_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email, 'password': self.password}

    @classmethod
    def get_user_by_id(cls, id: int):
        return User.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_username(cls, username):
        return User.query.filter_by(username=username).first()

class Serie(Base):
    __tablename__ = 'series'
    tmdb_id_serie = Column(Integer, primary_key=True)
    name = Column(String)
    overview = Column(String)
    backdrop_path = Column(String, nullable=True)
    vote_count = Column(Integer)
    vote_average = Column(Numeric(3, 1))

    def __init__(self, tmdb_id_serie, name, overview, backdrop_path, vote_count, vote_average):
        self.tmdb_id_serie = id_tmdb_serie
        self.name = name
        self.overview = overview
        self.backdrop_path = backdrop_path
        self.vote_count = vote_count
        self.vote_average = vote_average

    @classmethod
    def get_serie_by_id(cls, id_tmdb_serie: int):
        return Serie.query.filter_by(id_tmdb_serie=id_tmdb_serie).first()

    @classmethod
    def get_serie_by_username(cls, username: str):
        return Serie.query.filter_by(username=username).first()

    @classmethod
    def from_json(cls, json):
        return Serie(json['id'], json['name'], json['overview'], json['backdrop_path'], 1, json['vote_count'],
                     json['vote_average'])

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tmdb_id_serie = Column(Integer, ForeignKey('series.tmdb_id_serie'))

    def __init__(self, user_id, tmdb_id_serie):
        self.user_id = user_id
        self.tmdb_id_serie = tmdb_id_serie

    def as_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'tmdb_id_serie': self.tmdb_id_serie}

class Genre(Base):
    __tablename__ = 'genres'
    tmdb_id_genre = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, tmdb_id_genre, name):
        self.tmdb_id_genre = tmdb_id_genre
        self.name = name

    @classmethod
    def get_genre_from_id(cls, ids):
        return Genre.query(name).filter_by(tmdb_id_genre.in_(ids))

class Serie_Genre(Base):
    __tablename__ = 'series_genres'
    id = Column(Integer, primary_key=True)
    tmdb_id_genre = Column(Integer, ForeignKey('genres.tmdb_id_genre'))
    tmdb_id_serie = Column(Integer, ForeignKey('series.tmdb_id_serie'))

    def __init__(self, tmdb_id_genre, tmdb_id_serie):
        self.tmdb_id_genre = tmdb_id_genre
        self.tmdb_id_serie = tmdb_id_serie

    @classmethod
    def get_id_genre_from_id_serie(cls, tmdb_id_serie):
        return Serie_Genre(tmdb_id_genre).query.filter_by(tmdb_id_seriee=tmdb_id_serie)

