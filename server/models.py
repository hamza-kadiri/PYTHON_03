from sqlalchemy import Column, Integer, Numeric, String, ForeignKey, UniqueConstraint
from database import Base



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

class Serie(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    id_tmdb = Column(Integer, unique=True)
    title = Column(String)
    overview = Column(String)
    picture = Column(String, nullable=True)
    tmdb_id_genre = Column(Integer, ForeignKey('Genre.tmdb_id_genre'))
    vote_count = Column(Integer)
    vote_average = Column(Numeric(3,1))


    def __init__(self, id_tmdb, title, overview, picture, tmdb_id_genre, vote_count, vote_average):
        self.id_tmdb = id_tmdb
        self.title = title
        self.overview = overview
        self.picture = picture
        self.tmdb_id_genre = tmdb_id_genre
        self.vote_count = vote_count
        self.vote_average = vote_average


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    serie_id = Column(Integer, ForeignKey('Serie_id_tmdb'))

    def __init__(self, user_id, serie_id):
        self.user_id = user_id
        self.serie_id = serie_id

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    tmdb_id_genre = Column(Integer, unique=True)
    name = Column(String)

    def __init__(self, tmdb_id_genre, name):
        self.tmdb_id_genre = tmdb_id_genre
        self.name = name