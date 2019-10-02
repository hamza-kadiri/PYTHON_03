from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, UniqueConstraint
from database import Base


# TODO : Add encapsulation

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
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