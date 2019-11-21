from typing import List
from sqlalchemy import Table, Column, Boolean, Integer, SmallInteger, Numeric, String, ForeignKey, UniqueConstraint, desc, \
    inspect
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relationship
from database import Base
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import current_app as app
from time import time
from database import save_obj, delete_obj
from tmdb_api import get_tv_serie, get_tv_serie_season


class EqMixin(object):
    def compare_value(self):
        """Return a value or tuple of values to use for comparisons.
        Return instance's primary key by default, which requires that it is persistent in the database.
        Override this in subclasses to get other behavior.
        """
        return inspect(self).identity

    def __eq__(self, other: any):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.compare_value() == other.compare_value()

    def __ne__(self, other: any):
        eq = self.__eq__(other)

        if eq is NotImplemented:
            return eq

        return not eq

    def __hash__(self):
        return hash(self.__class__) ^ hash(self.compare_value())


subscriptions_table = Table('subscriptions', Base.metadata,
                            Column('user_id', Integer, ForeignKey('users.id')),
                            Column('tmdb_id_serie', Integer,
                                   ForeignKey('series.tmdb_id_serie'))
                            )

series_genres_table = Table('series_genres', Base.metadata,
                            Column('tmdb_id_genre', Integer,
                                   ForeignKey('genres.tmdb_id_genre')),
                            Column('tmdb_id_serie', Integer,
                                   ForeignKey('series.tmdb_id_serie'))
                            )
series_productors_table = Table('series_productors', Base.metadata,
                                Column('tmdb_id_productor', Integer,
                                       ForeignKey('productors.tmdb_id')),
                                Column('tmdb_id_serie', Integer, ForeignKey('series.tmdb_id_serie')))


class Person(EqMixin):
    tmdb_id = Column(Integer, primary_key=True)
    credit_id = Column(String)
    name = Column(String)
    profile_path = Column(String)

    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path: str):
        self.tmdb_id = tmdb_id
        self.credit_id = credit_id
        self.name = name
        self.profile_path = profile_path

    def compare_value(self):
        return self.tmdb_id

    def as_dict(self):
        return {'tmdb_id': self.tmdb_id, 'credit_id': self.credit_id, 'name': self.name,
                'profile_path': self.profile_path}


class Actor(Person, Base):
    __tablename__ = 'actors'
    department = Column(String)
    job = Column(String)

    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path: str, department: str, job: str):
        Person.__init__(self, tmdb_id, credit_id, name, profile_path)
        self.department = department
        self.job = job

    def save_in_db(self):
        save_obj(self)

    def as_dict(self):
        d = {'department': self.department, 'job': self.job}
        d.update(super().as_dict())
        return d


class Productor(Person, Base):
    __tablename__ = 'productors'
    gender = Column(String)
    series = relationship(
        "Serie", secondary=series_productors_table, back_populates="productors")

    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path: str, gender: int):
        Person.__init__(self, tmdb_id, credit_id, name, profile_path)
        self.gender = gender

    def save_in_db(self):
        save_obj(self)

    def as_dict(self):
        d = {'gender': self.gender}
        d.update(super().as_dict())
        return d

    @classmethod
    def create_from_json(cls, json):
        try:
            profile_path = json['profile_path']
        except KeyError:
            profile_path = "null"
        try:
            gender = json['gender']
        except KeyError:
            gender = "null"
        new_productor = Productor(json['id'], json['credit_id'], json['name'],
                                  profile_path, gender)
        new_productor.save_in_db()
        return new_productor

    @classmethod
    def get_productor_by_id(cls, tmdb_id):
        try:
            return Productor.query.filter_by(tmdb_id=tmdb_id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None


class Genre(Base, EqMixin):
    __tablename__ = 'genres'
    tmdb_id_genre = Column(SmallInteger, primary_key=True)
    name = Column(String)
    series = relationship(
        "Serie", secondary=series_genres_table, back_populates="genres")

    def __init__(self, tmdb_id_genre: int, name: str):
        self.tmdb_id_genre = tmdb_id_genre
        self.name = name

    def compare_value(self):
        return self.tmdb_id_genre

    def save_in_db(self):
        save_obj(self)

    def as_dict(self):
        return {'tmdb_id_genre': self.tmdb_id_genre, 'name': self.name}

    @classmethod
    def create_from_json(cls, json: dict):
        genre = Genre(json['id'], json['name'])
        genre.save_in_db()
        return genre

    @classmethod
    def get_genre_by_id(cls, genre_id: int):
        try:
            return Genre.query.filter_by(tmdb_id_genre=genre_id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None


class Episode(Base, EqMixin):
    __tablename__ = 'episodes'
    tmdb_id_episode = Column(Integer, primary_key=True)
    name = Column(String)
    overview = Column(String)
    season_number = Column(SmallInteger)
    episode_number = Column(SmallInteger)
    vote_count = Column(Integer)
    vote_average = Column(Numeric(3, 1))
    air_date = Column(String)
    still_path = Column(String, nullable=True)
    tmdb_id_season = Column(Integer, ForeignKey(
        'seasons.tmdb_id_season'), nullable=False)

    def compare_value(self):
        return self.tmdb_id_episode

    def save_in_db(self):
        save_obj(self)

    def __init__(self, tmdb_id_episode: int, name: str, overview: str, season_number: int, episode_number: int,
                 vote_count: int, vote_average: float, air_date: str, still_path: str, tmdb_id_season: int):
        self.tmdb_id_episode = tmdb_id_episode
        self.name = name
        self.overview = overview
        self.season_number = season_number
        self.episode_number = episode_number
        self.vote_count = vote_count
        self.vote_average = vote_average
        self.air_date = air_date
        self.still_path = still_path
        self.tmdb_id_season = tmdb_id_season

    def as_dict(self):
        return {'tmdb_id_episode': self.tmdb_id_episode, 'name': self.name, 'overview': self.overview,
                'season_number': self.season_number, 'episode_number': self.episode_number,
                'vote_count': self.vote_count, 'vote_average': str(self.vote_average), 'air_date': self.air_date,
                'still_path': self.still_path}

    @classmethod
    def get_episode_by_id(cls, tmdb_id_episode: int):
        try:
            return Episode.query.filter_by(tmdb_id_episode=tmdb_id_episode).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def create_from_json(cls, json: dict, tmdb_id_season: int):
        episode = Episode(json['id'], json['name'], json['overview'], json['season_number'], json['episode_number'],
                          json['vote_count'], json['vote_average'], json['air_date'], json['still_path'],
                          tmdb_id_season)
        episode.save_in_db()
        return episode


class Season(Base, EqMixin):
    __tablename__ = 'seasons'
    tmdb_id_season = Column(Integer, primary_key=True)
    name = Column(String)
    overview = Column(String)
    season_number = Column(SmallInteger)
    air_date = Column(String)
    poster_path = Column(String, nullable=True)
    tmdb_id_serie = Column(Integer, ForeignKey(
        'series.tmdb_id_serie'), nullable=False)
    episodes = relationship('Episode', backref='seasons', lazy=True)

    def compare_value(self):
        return self.tmdb_id_season

    def save_in_db(self):
        save_obj(self)

    def __init__(self, tmdb_id_season: int, name: str, overview: str, season_number: int, air_date: str,
                 poster_path: str, episodes: List[Episode], tmdb_id_serie: int):
        self.tmdb_id_season = tmdb_id_season
        self.name = name
        self.overview = overview
        self.season_number = season_number
        self.air_date = air_date
        self.poster_path = poster_path
        self.episodes = episodes
        self.tmdb_id_serie = tmdb_id_serie

    def as_dict(self):
        return {'tmdb_id_season': self.tmdb_id_season, 'name': self.name, 'overview': self.overview,
                'season_number': self.season_number, 'air_date': self.air_date, 'poster_path': self.poster_path,
                'episodes': [episode.as_dict() for episode in self.episodes]}

    @classmethod
    def get_season_by_id(cls, tmdb_id_season: int):
        try:
            return Season.query.filter_by(tmdb_id_season=tmdb_id_season).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def create_from_json(cls, json: dict, tmdb_id_serie: int):
        season = Season(json['id'], json['name'], json['overview'], json['season_number'], json['air_date'],
                        json['poster_path'], [], tmdb_id_serie)
        season.save_in_db()
        for episode in json['episodes']:
            new_episode = Episode.get_episode_by_id(episode['id'])
            if new_episode is None:
                new_episode = Episode.create_from_json(episode, json['id'])
            season.episodes.append(new_episode)
        season.save_in_db()
        return season


class Serie(Base, EqMixin):
    __tablename__ = 'series'
    tmdb_id_serie = Column(Integer, primary_key=True)
    name = Column(String)
    overview = Column(String)
    backdrop_path = Column(String, nullable=True)
    poster_path = Column(String, nullable=True)
    nb_seasons = Column(SmallInteger)
    nb_episodes = Column(SmallInteger)
    next_episode_name = Column(String)
    next_episode_air_date = Column(String)
    next_episode_season_number = Column(SmallInteger)
    next_episode_episode_number = Column(SmallInteger)
    vote_count = Column(Integer)
    vote_average = Column(Numeric(3, 1))
    creation = Column(Integer)
    last_update = Column(Integer)
    productors = relationship(
        "Productor", secondary=series_productors_table, back_populates="series")
    genres = relationship(
        "Genre", secondary=series_genres_table, back_populates="series")
    users = relationship(
        "User", secondary=subscriptions_table, back_populates="series")
    seasons = relationship('Season', backref='series', lazy=True)

    def __init__(self, tmdb_id_serie: int, name: str, overview: str, backdrop_path: str, poster_path: str, nb_seasons: int,
                 nb_episodes: int, next_episode_name: str, next_episode_air_date: str, next_episode_season_number: int,
                 next_episode_episode_number: int, vote_count: int, vote_average: float, genres: List[Genre],
                 productors: List[Productor], seasons: List[Season]):
        self.tmdb_id_serie = tmdb_id_serie
        self.name = name
        self.overview = overview
        self.backdrop_path = backdrop_path
        self.poster_path = poster_path
        self.nb_seasons = nb_seasons
        self.nb_episodes = nb_episodes
        self.next_episode_name = next_episode_name
        self.next_episode_air_date = next_episode_air_date
        self.next_episode_season_number = next_episode_season_number
        self.next_episode_episode_number = next_episode_episode_number
        self.vote_count = vote_count
        self.vote_average = vote_average
        self.creation = time()
        self.last_update = time()
        self.genres = genres
        self.productors = productors
        self.seasons = seasons

    def save_in_db(self):
        save_obj(self)

    def update_from_json(self, json: dict):
        self.last_update = time()
        # Basic informations
        self.name = json['name']
        self.overview = json['overview']
        self.backdrop_path = json['backdrop_path']
        self.backdrop_path = json['poster_path']
        self.nb_seasons = json['number_of_seasons']
        self.nb_episodes = json['number_of_episodes']
        self.vote_count = json['vote_count']
        self.vote_average = json['vote_average']
        # Next episode informations
        next_episode_name = None
        next_episode_air_date = None
        next_episode_season_number = None
        next_episode_episode_number = None
        next_episode = json['next_episode_to_air']
        if next_episode is not None:
            next_episode_name = next_episode['name']
            next_episode_air_date = next_episode['air_date']
            next_episode_season_number = next_episode['season_number']
            next_episode_episode_number = next_episode['episode_number']
        self.next_episode_name = next_episode_name
        self.next_episode_air_date = next_episode_air_date
        self.next_episode_season_number = next_episode_season_number
        self.next_episode_episode_number = next_episode_episode_number
        # Genres informations
        serie_genres = []
        for genre in json['genres']:
            new_genre = Genre.get_genre_by_id(genre['id'])
            if new_genre is None:
                new_genre = Genre.create_from_json(genre)
            serie_genres.append(new_genre)
        self.genres = serie_genres
        # Productors informations
        serie_productors = []
        for productor in json['created_by']:
            new_productor = Productor.get_productor_by_id(productor['id'])
            if new_productor is None:
                new_productor = Productor.create_from_json(productor)
            serie_productors.append(new_productor)
        self.productors = serie_productors
        # Seasons informations
        serie_seasons = []
        for season in json['seasons']:
            new_season = Season.get_season_by_id(season['id'])
            if new_season is None:
                new_season = Season.create_from_json(get_tv_serie_season(json['id'], season['season_number']),
                                                     json['id'])
            serie_seasons.append(new_season)
        self.seasons = serie_seasons
        # Saving changes
        self.save_in_db()

    def compare_value(self):
        return self.tmdb_id_serie

    def as_dict(self):
        return {'tmdb_id_serie': self.tmdb_id_serie, 'name': self.name, 'overview': self.overview,
                'backdrop_path': self.backdrop_path,
                'poster_path': self.poster_path,
                'nb_seasons': self.nb_seasons, 'nb_episodes': self.nb_episodes,
                'next_episode_name': self.next_episode_name, 'next_episode_air_date': self.next_episode_air_date,
                'next_episode_season_number': self.next_episode_season_number,
                'next_episode_episode_number': self.next_episode_episode_number,
                'vote_count': self.vote_count, 'vote_average': str(self.vote_average),
                'genres': [genre.as_dict() for genre in self.genres],
                'productors': [productor.as_dict() for productor in self.productors],
                'seasons': [season.as_dict() for season in self.seasons]}

    @classmethod
    def get_serie_by_id(cls, tmdb_id_serie: int):
        try:
            return Serie.query.filter_by(tmdb_id_serie=tmdb_id_serie).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def get_all_series(cls):
        return Serie.query.all()

    @classmethod
    def create_from_json(cls, json: dict):
        # Next episode information
        next_episode_name = None
        next_episode_air_date = None
        next_episode_season_number = None
        next_episode_episode_number = None
        next_episode = json['next_episode_to_air']
        if next_episode is not None:
            next_episode_name = next_episode['name']
            next_episode_air_date = next_episode['air_date']
            next_episode_season_number = next_episode['season_number']
            next_episode_episode_number = next_episode['episode_number']
        serie = Serie(json['id'], json['name'], json['overview'], json['backdrop_path'], json['poster_path'], json['number_of_seasons'],
                      json['number_of_episodes'], next_episode_name, next_episode_air_date, next_episode_season_number,
                      next_episode_episode_number, json['vote_count'], json['vote_average'], [], [], [])
        serie.save_in_db()
        # Genres informations
        for genre in json['genres']:
            new_genre = Genre.get_genre_by_id(genre['id'])
            if new_genre is None:
                new_genre = Genre.create_from_json(genre)
            serie.genres.append(new_genre)
        # Productors informations
        for productor in json['created_by']:
            new_productor = Productor.get_productor_by_id(productor['id'])
            if new_productor is None:
                new_productor = Productor.create_from_json(productor)
            serie.productors.append(new_productor)
        # Seasons informations
        for season in json['seasons']:
            new_season = Season.get_season_by_id(season['id'])
            if new_season is None:
                new_season = Season.create_from_json(get_tv_serie_season(json['id'], season['season_number']),
                                                     json['id'])
            serie.seasons.append(new_season)
        serie.save_in_db()
        return serie


class User(Base, EqMixin):
    __tablename__ = 'users'
    id = Column(SmallInteger, primary_key=True)
    username = Column(String(20), unique=True)
    email = Column(String(80), unique=True)
    password_hash = Column(String(128))
    series = relationship(
        "Serie", secondary=subscriptions_table, back_populates="users")

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password_hash = User.hash_password(password)
        self.last_connexion = time()

    def compare_value(self):
        return self.id

    def as_dict(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration: int = 6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def get_subscription_by_serie_id(self, tmdb_id_serie: int):
        try:
            return User.query.join(Serie, User.series).filter(User.id == self.id).filter(
                Serie.tmdb_id_serie == tmdb_id_serie).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    def save_in_db(self):
        save_obj(self)

    def add_favorite_serie(self, serie: Serie):
        self.series.append(serie)
        self.save_in_db()

    def delete_favorite_serie(self, serie: Serie):
        self.series.remove(serie)
        self.save_in_db()
        for notif in Notification.get_notifications_by_user_and_serie(self, serie):
            notif.delete_in_db()

    @classmethod
    def get_user_by_id(cls, user_id: int):
        try:
            return User.query.filter_by(id=user_id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def get_user_by_username(cls, username: str):
        try:
            return User.query.filter_by(username=username).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def hash_password(cls, password: str):
        return pwd_context.encrypt(password)

    @classmethod
    def verify_auth_token(cls, token: str):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.get_user_by_id(data['id'])
        return user


class Notification(Base, EqMixin):
    __tablename__ = "notifications"
    id = Column(SmallInteger, primary_key=True)
    user_id = Column(SmallInteger, ForeignKey('users.id'), nullable=False)
    tmdb_id_serie = Column(Integer, ForeignKey(
        'series.tmdb_id_serie'), nullable=False)
    serie_name = Column(String)
    name = Column(String)
    season_number = Column(SmallInteger)
    episode_number = Column(SmallInteger)
    next_air_date = Column(String)
    creation_date = Column(Integer)
    backdrop_path = Column(String)
    poster_path = Column(String)
    read = Column(Boolean)

    def __init__(self, user_id: int, tmdb_id_serie: int, serie_name: str, name: str, season_number: int,
                 episode_number: int, next_air_date: str, backdrop_path: str, poster_path: str):
        self.user_id = user_id
        self.tmdb_id_serie = tmdb_id_serie
        self.serie_name = serie_name
        self.name = name
        self.season_number = season_number
        self.episode_number = episode_number
        self.next_air_date = next_air_date
        self.backdrop_path = backdrop_path
        self.poster_path = poster_path
        self.creation_date = time()
        self.read = False

    def compare_value(self):
        return self.id

    def save_in_db(self):
        save_obj(self)

    def delete_in_db(self):
        delete_obj(self)

    def mark_as_read(self):
        self.read = True
        self.save_in_db()

    def as_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'tmdb_id_serie': self.tmdb_id_serie,
                'serie_name': self.serie_name, 'name': self.name, 'episode_number': self.episode_number,
                'season_number': self.season_number, 'next_air_date': self.next_air_date, 'backdrop_path': self.backdrop_path, 'read': self.read, 'poster_path': self.poster_path}

    @classmethod
    def create_from_serie(cls, user_id: int, serie: Serie):
        notif = Notification(user_id, serie.tmdb_id_serie, serie.name, serie.next_episode_name,
                             serie.next_episode_season_number, serie.next_episode_episode_number,
                             serie.next_episode_air_date, serie.backdrop_path, serie.poster_path)
        if notif.next_air_date is None or notif.next_air_date == "" or notif.next_air_date == "null":
            raise ValueError("No air date for the notification")
        else:
            notif.save_in_db()
            return notif

    @classmethod
    def get_notifications_by_user(cls, user: User):
        return Notification.query.filter_by(user_id=user.id).order_by(desc(Notification.creation_date)).limit(15).all()

    @classmethod
    def get_notifications_by_user_and_serie(cls, user: User, serie: Serie):
        return Notification.query.filter_by(user_id=user.id, tmdb_id_serie=serie.tmdb_id_serie).order_by(desc(Notification.creation_date)).all()

    @classmethod
    def get_notification_by_id(cls, notification_id: int):
        try:
            return Notification.query.filter_by(id=notification_id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None
