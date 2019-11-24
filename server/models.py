from typing import List
from sqlalchemy import Table, Column, Boolean, Integer, SmallInteger, Numeric, String, ForeignKey, UniqueConstraint, \
    desc, \
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
from helpers import sortListByLambda, generate_assets_url

'''Defining basic classes'''


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


class DBObject(EqMixin):
    def save_in_db(self):
        save_obj(self)

    def delete_in_db(self):
        delete_obj(self)


'''Initializing many-to-many relationships between tables'''

subscriptions_table = Table('subscriptions', Base.metadata,
                            Column('user_id', Integer, ForeignKey('users._User__id')),
                            Column('tmdb_id_serie', Integer,
                                   ForeignKey('series._Serie__tmdb_id_serie'))
                            )

series_genres_table = Table('series_genres', Base.metadata,
                            Column('tmdb_id_genre', Integer,
                                   ForeignKey('genres._Genre__tmdb_id_genre')),
                            Column('tmdb_id_serie', Integer,
                                   ForeignKey('series._Serie__tmdb_id_serie'))
                            )
series_productors_table = Table('series_productors', Base.metadata,
                                Column('tmdb_id_productor', Integer,
                                       ForeignKey('productors._Person__tmdb_id')),
                                Column('tmdb_id_serie', Integer, ForeignKey('series._Serie__tmdb_id_serie')))

'''Defining models'''
'''Please note that the methods are ordered to follow a "CRUD" order : static method(s) for creation, static method(s) for selection, method(s) for update and method(s) to delete'''


class Person:
    # Attributes and basic methods (init, as_dict)
    __tmdb_id = Column(Integer, primary_key=True)
    __credit_id = Column(String)
    __name = Column(String)
    __profile_path = Column(String)

    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path: str):
        self.__tmdb_id = tmdb_id
        self.__credit_id = credit_id
        self.__name = name
        self.__profile_path = profile_path

    def as_dict(self):
        return {'tmdb_id': self.__tmdb_id, 'credit_id': self.__credit_id, 'name': self.__name,
                'profile_path': self.__profile_path}

    # Getters

    @property
    def tmdb_id(self):
        return self.__tmdb_id

    @property
    def credit_id(self):
        return self.__credit_id

    @property
    def name(self):
        return self.__name

    @property
    def profile_path(self):
        return self.__profile_path


class Actor(Person, DBObject, Base):
    # Attributes and basic methods (init, compare_value, as_dict)
    __tablename__ = 'actors'
    __department = Column(String)
    __job = Column(String)

    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path: str, department: str, job: str):
        Person.__init__(self, tmdb_id, credit_id, name, profile_path)
        self.__department = department
        self.__job = job

    def compare_value(self):
        return self.__tmdb_id

    def as_dict(self):
        return {'department': self.__department, 'job': self.__job, **super().as_dict()}

    # Getters

    @property
    def department(self):
        return self.__department

    @property
    def job(self):
        return self.__job


class Productor(Person, DBObject, Base):
    # Attributes and basic methods (init, compare_value, as_dict)
    __tablename__ = 'productors'
    __gender = Column(String)
    __series = relationship(
        "Serie", secondary=series_productors_table, back_populates="_Serie__productors")

    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path: str, gender: int):
        Person.__init__(self, tmdb_id, credit_id, name, profile_path)
        self.__gender = gender

    def compare_value(self):
        return self.__tmdb_id

    def as_dict(self):
        return {'gender': self.__gender, **super().as_dict()}

    # Getters

    @property
    def gender(self):
        return self.__gender

    # Static method for creation
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

    # Static method for selection
    @classmethod
    def get_productor_by_id(cls, tmdb_id):
        try:
            return Productor.query.filter_by(_Person__tmdb_id=tmdb_id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None


class Genre(DBObject, Base):
    # Attributes and basic methods (init, compare_value, as_dict)
    __tablename__ = 'genres'
    __tmdb_id_genre = Column(SmallInteger, primary_key=True)
    __name = Column(String)
    __series = relationship(
        "Serie", secondary=series_genres_table, back_populates="_Serie__genres")

    def __init__(self, tmdb_id_genre: int, name: str):
        self.__tmdb_id_genre = tmdb_id_genre
        self.__name = name

    def compare_value(self):
        return self.__tmdb_id_genre

    def as_dict(self):
        return {'tmdb_id_genre': self.__tmdb_id_genre, 'name': self.__name}

    # Getters

    @property
    def tmdb_id_genre(self):
        return self.__tmdb_id_genre

    @property
    def name(self):
        return self.__name

    @property
    def series(self):
        return self.__series

    # Static method for creation
    @classmethod
    def create_from_json(cls, json: dict):
        genre = Genre(json['id'], json['name'])
        genre.save_in_db()
        return genre

    # Static method for selection
    @classmethod
    def get_genre_by_id(cls, genre_id: int):
        try:
            return Genre.query.filter_by(_Genre__tmdb_id_genre=genre_id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None


class Episode(DBObject, Base):
    # Attributes and basic methods (init, compare_value, as_dict)
    __tablename__ = 'episodes'
    __tmdb_id_episode = Column(Integer, primary_key=True)
    __name = Column(String)
    __overview = Column(String)
    __season_number = Column(SmallInteger)
    __episode_number = Column(SmallInteger)
    __vote_count = Column(Integer)
    __vote_average = Column(Numeric(3, 1))
    __air_date = Column(String)
    __still_path = Column(String, nullable=True)
    __tmdb_id_season = Column(Integer, ForeignKey(
        'seasons._Season__tmdb_id_season'), nullable=False)

    def __init__(self, tmdb_id_episode: int, name: str, overview: str, season_number: int, episode_number: int,
                 vote_count: int, vote_average: float, air_date: str, still_path: str, tmdb_id_season: int):
        self.__tmdb_id_episode = tmdb_id_episode
        self.__name = name
        self.__overview = overview
        self.__season_number = season_number
        self.__episode_number = episode_number
        self.__vote_count = vote_count
        self.__vote_average = vote_average
        self.__air_date = air_date
        self.__still_path = still_path
        self.__tmdb_id_season = tmdb_id_season

    def compare_value(self):
        return self.__tmdb_id_episode

    def as_dict(self):
        dict = {'tmdb_id_episode': self.__tmdb_id_episode, 'name': self.__name, 'overview': self.__overview,
                'season_number': self.__season_number, 'episode_number': self.__episode_number,
                'vote_count': self.__vote_count, 'vote_average': str(self.__vote_average), 'air_date': self.__air_date,
                'still_path': self.__still_path}
        generate_assets_url(dict)
        return dict

    # Getters

    @property
    def tmdb_id_episode(self):
        return self.__tmdb_id_episode

    @property
    def name(self):
        return self.__name

    @property
    def overview(self):
        return self.__overview

    @property
    def season_number(self):
        return self.__season_number

    @property
    def episode_number(self):
        return self.__episode_number

    @property
    def vote_count(self):
        return self.__vote_count

    @property
    def vote_average(self):
        return self.__vote_average

    @property
    def air_date(self):
        return self.__air_date

    @property
    def still_path(self):
        return self.__still_path

    @property
    def tmdb_id_season(self):
        return self.__tmdb_id_season

    # Static method for creation
    @classmethod
    def create_from_json(cls, json: dict, season_poster_path: str, tmdb_id_season: int):
        if json['still_path'] is None or json['still_path'] == "" or json['still_path']  == "null":
            episode = Episode(json['id'], json['name'], json['overview'], json['season_number'], json['episode_number'],
                          json['vote_count'], json['vote_average'], json['air_date'],season_poster_path,
                          tmdb_id_season)
        else:
            episode = Episode(json['id'], json['name'], json['overview'], json['season_number'], json['episode_number'],
                          json['vote_count'], json['vote_average'], json['air_date'], json['still_path'],
                          tmdb_id_season)
        episode.save_in_db()
        return episode

    # Static method for selection
    @classmethod
    def get_episode_by_id(cls, tmdb_id_episode: int):
        try:
            return Episode.query.filter_by(_Episode__tmdb_id_episode=tmdb_id_episode).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None


class Season(DBObject, Base):
    # Attributes and basic methods (init, compare_value, as_dict)
    __tablename__ = 'seasons'
    __tmdb_id_season = Column(Integer, primary_key=True)
    __name = Column(String)
    __overview = Column(String)
    __season_number = Column(SmallInteger)
    __air_date = Column(String)
    __poster_path = Column(String, nullable=True)
    __tmdb_id_serie = Column(Integer, ForeignKey(
        'series._Serie__tmdb_id_serie'), nullable=False)
    __episodes = relationship('Episode', backref='seasons', lazy=True)

    def __init__(self, tmdb_id_season: int, name: str, overview: str, season_number: int, air_date: str,
                 poster_path: str, episodes: List[Episode], tmdb_id_serie: int):
        self.__tmdb_id_season = tmdb_id_season
        self.__name = name
        self.__overview = overview
        self.__season_number = season_number
        self.__air_date = air_date
        self.__poster_path = poster_path
        self.__episodes = episodes
        self.__tmdb_id_serie = tmdb_id_serie

    def compare_value(self):
        return self.__tmdb_id_season

    def as_dict(self):
        dict = {'tmdb_id_season': self.__tmdb_id_season, 'name': self.__name, 'overview': self.__overview,
                'season_number': self.__season_number, 'air_date': self.__air_date, 'poster_path': self.__poster_path,
                'episodes': [episode.as_dict() for episode in
                             sortListByLambda(self.__episodes, lambda x: x.episode_number)], }
        generate_assets_url(dict)
        return dict

    # Getters

    @property
    def tmdb_id_season(self):
        return self.__tmdb_id_season

    @property
    def name(self):
        return self.__name

    @property
    def overview(self):
        return self.__overview

    @property
    def season_number(self):
        return self.__season_number

    @property
    def air_date(self):
        return self.__air_date

    @property
    def poster_path(self):
        return self.__poster_path

    @property
    def tmdb_id_serie(self):
        return self.__tmdb_id_serie

    @property
    def episodes(self):
        return self.__episodes

        # Static method for creation

    @classmethod
    def create_season_from_json(cls, json: dict, serie_poster_path: str, tmdb_id_serie: int):
        if json['poster_path'] is None or json['poster_path'] == "null" or json['poster_path'] == "":
            season = Season(json['id'], json['name'], json['overview'], json['season_number'], json['air_date'],
                        serie_poster_path, [], tmdb_id_serie)
        else:
            season = Season(json['id'], json['name'], json['overview'], json['season_number'], json['air_date'],
                        json['poster_path'], [], tmdb_id_serie)
        season.save_in_db()
        for episode in json['episodes']:
            new_episode = Episode.get_episode_by_id(episode['id'])
            if new_episode is None:
                new_episode = Episode.create_from_json(episode, season.poster_path, json['id'])
            season.episodes.append(new_episode)
        season.save_in_db()
        return season


    # Static method for selection
    @classmethod
    def get_season_by_id(cls, tmdb_id_season: int):
        try:
            return Season.query.filter_by(_Season__tmdb_id_season=tmdb_id_season).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None
    #static method to create all the seasons from a json      
    @classmethod
    def create_seasons_from_json(cls, json):
        # Seasons informations
        seasons = []
        for season in json['seasons']:
            new_season = Season.get_season_by_id(season['id'])
            if new_season is None:
                new_season = Season.create_season_from_json(get_tv_serie_season(json['id'], season['season_number']), json['poster_path'],
                                                     json['id'])
            seasons.append(new_season)
        serie = Serie.get_serie_by_id(json['id'])
        serie.seasons = seasons
        serie.save_in_db()
        return serie



class Serie(DBObject, Base):
    # Attributes and basic methods (init, compare_value, as_dict)
    __tablename__ = 'series'
    __tmdb_id_serie = Column(Integer, primary_key=True)
    __name = Column(String)
    __overview = Column(String)
    __backdrop_path = Column(String, nullable=True)
    __poster_path = Column(String, nullable=True)
    __nb_seasons = Column(SmallInteger)
    __nb_episodes = Column(SmallInteger)
    __next_episode_name = Column(String)
    __next_episode_air_date = Column(String)
    __next_episode_season_number = Column(SmallInteger)
    __next_episode_episode_number = Column(SmallInteger)
    __vote_count = Column(Integer)
    __vote_average = Column(Numeric(3, 1))
    __creation = Column(Integer)
    __last_update = Column(Integer)
    __productors = relationship(
        "Productor", secondary=series_productors_table, back_populates="_Productor__series")
    __genres = relationship(
        "Genre", secondary=series_genres_table, back_populates="_Genre__series")
    __users = relationship(
        "User", secondary=subscriptions_table, back_populates="_User__series")
    __seasons = relationship('Season', backref='series', lazy=True)

    def __init__(self, tmdb_id_serie: int, name: str, overview: str, backdrop_path: str, poster_path: str,
                 nb_seasons: int,
                 nb_episodes: int, next_episode_name: str, next_episode_air_date: str, next_episode_season_number: int,
                 next_episode_episode_number: int, vote_count: int, vote_average: float, genres: List[Genre],
                 productors: List[Productor], seasons: List[Season]):
        self.__tmdb_id_serie = tmdb_id_serie
        self.__name = name
        self.__overview = overview
        self.__backdrop_path = backdrop_path
        self.__poster_path = poster_path
        self.__nb_seasons = nb_seasons
        self.__nb_episodes = nb_episodes
        self.__next_episode_name = next_episode_name
        self.__next_episode_air_date = next_episode_air_date
        self.__next_episode_season_number = next_episode_season_number
        self.__next_episode_episode_number = next_episode_episode_number
        self.__vote_count = vote_count
        self.__vote_average = vote_average
        self.__creation = time()
        self.__last_update = time()
        self.__genres = genres
        self.__productors = productors
        self.__seasons = seasons

    def compare_value(self):
        return self.__tmdb_id_serie

    def as_dict(self):
        dict = {'tmdb_id_serie': self.__tmdb_id_serie, 'name': self.__name, 'overview': self.__overview,
                'backdrop_path': self.__backdrop_path,
                'poster_path': self.__poster_path,
                'nb_seasons': self.__nb_seasons, 'nb_episodes': self.__nb_episodes,
                'next_episode_name': self.__next_episode_name, 'next_episode_air_date': self.__next_episode_air_date,
                'next_episode_season_number': self.__next_episode_season_number,
                'next_episode_episode_number': self.__next_episode_episode_number,
                'vote_count': self.__vote_count, 'vote_average': str(self.__vote_average),
                'genres': [genre.as_dict() for genre in self.__genres],
                'productors': [productor.as_dict() for productor in self.__productors],
                'seasons': [season.as_dict() for season in sortListByLambda(self.__seasons, lambda x: x.season_number)]}
        generate_assets_url(dict)
        return dict

    # Getters

    @property
    def tmdb_id_serie(self):
        return self.__tmdb_id_serie

    @property
    def name(self):
        return self.__name

    @property
    def overview(self):
        return self.__overview

    @property
    def backdrop_path(self):
        return self.__backdrop_path

    @property
    def poster_path(self):
        return self.__poster_path

    @property
    def nb_seasons(self):
        return self.__nb_seasons

    @property
    def nb_episodes(self):
        return self.__nb_episodes

    @property
    def next_episode_name(self):
        return self.__next_episode_name

    @property
    def next_episode_air_date(self):
        return self.__next_episode_air_date

    @property
    def next_episode_season_number(self):
        return self.__next_episode_season_number

    @property
    def next_episode_episode_number(self):
        return self.__next_episode_episode_number

    @property
    def vote_count(self):
        return self.__vote_count

    @property
    def vote_average(self):
        return self.__vote_average

    @property
    def creation(self):
        return self.__creation

    @property
    def last_update(self):
        return self.__last_update

    @property
    def productors(self):
        return self.__productors

    @property
    def genres(self):
        return self.__genres

    @property
    def users(self):
        return self.__users

    @property
    def seasons(self):
        return self.__seasons

    # Static method for creation
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
        serie = Serie(json['id'], json['name'], json['overview'], json['backdrop_path'], json['poster_path'],
                      json['number_of_seasons'],
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
        serie.save_in_db()
        return serie

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
                'seasons': [season.as_dict() for season in sortListByLambda(self.seasons, lambda x: x.season_number)]}


    # Static methods for selection
    @classmethod
    def get_serie_by_id(cls, tmdb_id_serie: int):
        try:
            return Serie.query.filter_by(_Serie__tmdb_id_serie=tmdb_id_serie).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def get_all_series(cls):
        return Serie.query.all()

        # Method to update

    def update_from_json(self, json: dict):
        self.__last_update = time()
        # Basic informations
        self.__name = json['name']
        self.__overview = json['overview']
        self.__backdrop_path = json['backdrop_path']
        self.__backdrop_path = json['poster_path']
        self.__nb_seasons = json['number_of_seasons']
        self.__nb_episodes = json['number_of_episodes']
        self.__vote_count = json['vote_count']
        self.__vote_average = json['vote_average']
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
        self.__next_episode_name = next_episode_name
        self.__next_episode_air_date = next_episode_air_date
        self.__next_episode_season_number = next_episode_season_number
        self.__next_episode_episode_number = next_episode_episode_number
        # Genres informations
        serie_genres = []
        for genre in json['genres']:
            new_genre = Genre.get_genre_by_id(genre['id'])
            if new_genre is None:
                new_genre = Genre.create_from_json(genre)
            serie_genres.append(new_genre)
        self.__genres = serie_genres
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
                new_season = Season.create_season_from_json(get_tv_serie_season(json['id'], season['season_number']), json['poster_path'],
                                                     json['id'])
            serie_seasons.append(new_season)
        self.seasons = serie_seasons
        # Saving changes
        self.save_in_db()
        return self


class User(DBObject, Base):
    # Attributes and basic methods (init, compare_value, as_dict)
    __tablename__ = 'users'
    __id = Column(SmallInteger, primary_key=True)
    __username = Column(String(20), unique=True)
    __email = Column(String(80), unique=True)
    __password_hash = Column(String(128))
    __series = relationship(
        "Serie", secondary=subscriptions_table, back_populates="_Serie__users")

    def __init__(self, username: str, email: str, password: str):
        self.__username = username
        self.__email = email
        self.__password_hash = User.hash_password(password)

    def compare_value(self):
        return self.__id

    def as_dict(self):
        return {'id': self.__id, 'username': self.__username, 'email': self.__email}

    # Getters

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username

    @property
    def email(self):
        return self.__email

    @property
    def series(self):
        return self.__series


    # Methods related to authentication

    def verify_password(self, password: str):
        return pwd_context.verify(password, self.__password_hash)

    def generate_auth_token(self, expiration: int = 6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.__id})

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

    # Static methods for selection

    @classmethod
    def get_user_by_id(cls, user_id: int):
        try:
            return User.query.filter_by(_User__id=user_id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def get_user_by_username(cls, username: str):
        try:
            return User.query.filter_by(_User__username=username).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def get_user_by_email(cls, email: str):
        try:
            return User.query.filter_by(_User__email=email).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    # Methods to update

    def get_subscription_by_serie_id(self, tmdb_id_serie: int):
        try:
            return User.query.join(Serie, User._User__series).filter(User._User__id == self.__id).filter(
                Serie._Serie__tmdb_id_serie == tmdb_id_serie).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    def add_favorite_serie(self, serie: Serie):
        self.__series.append(serie)
        self.save_in_db()

    def delete_favorite_serie(self, serie: Serie):
        self.__series.remove(serie)
        self.save_in_db()
        for notif in Notification.get_notifications_by_user_and_serie(self, serie):
            notif.delete_in_db()


class Notification(DBObject, Base):
    # Attributes and basic methods (init, compare_value, as_dict)
    __tablename__ = "notifications"
    __id = Column(SmallInteger, primary_key=True)
    __user_id = Column(SmallInteger, ForeignKey('users._User__id'), nullable=False)
    __tmdb_id_serie = Column(Integer, ForeignKey(
        'series._Serie__tmdb_id_serie'), nullable=False)
    __serie_name = Column(String)
    __name = Column(String)
    __season_number = Column(SmallInteger)
    __episode_number = Column(SmallInteger)
    __next_air_date = Column(String)
    __creation_date = Column(Integer)
    __backdrop_path = Column(String)
    __poster_path = Column(String)
    __read = Column(Boolean)

    def __init__(self, user_id: int, tmdb_id_serie: int, serie_name: str, name: str, season_number: int,
                 episode_number: int, next_air_date: str, backdrop_path: str, poster_path: str):
        self.__user_id = user_id
        self.__tmdb_id_serie = tmdb_id_serie
        self.__serie_name = serie_name
        self.__name = name
        self.__season_number = season_number
        self.__episode_number = episode_number
        self.__next_air_date = next_air_date
        self.__backdrop_path = backdrop_path
        self.__poster_path = poster_path
        self.__creation_date = time()
        self.__read = False

    def compare_value(self):
        return self.__id

    def as_dict(self):
        dict = {'id': self.__id, 'user_id': self.__user_id, 'tmdb_id_serie': self.__tmdb_id_serie,
                'serie_name': self.__serie_name, 'name': self.__name, 'episode_number': self.__episode_number,
                'season_number': self.__season_number, 'next_air_date': self.__next_air_date,
                'backdrop_path': self.__backdrop_path, 'read': self.__read, 'poster_path': self.__poster_path}
        generate_assets_url(dict)
        return dict

    # Getters

    @property
    def id(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def tmdb_id_serie(self):
        return self.__tmdb_id_serie

    @property
    def serie_name(self):
        return self.__serie_name

    @property
    def name(self):
        return self.__name

    @property
    def season_number(self):
        return self.__season_number

    @property
    def episode_number(self):
        return self.__episode_number

    @property
    def next_air_date(self):
        return self.__next_air_date

    @property
    def creation_date(self):
        return self.__creation_date

    @property
    def backdrop_path(self):
        return self.__backdrop_path

    @property
    def poster_path(self):
        return self.__poster_path

    @property
    def read(self):
        return self.__read

    # Static method for creation
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

    # Static methods for selection
    @classmethod
    def get_notifications_by_user(cls, user: User):
        return Notification.query.filter_by(_Notification__user_id=user.id).order_by(desc(Notification._Notification__creation_date)).limit(15).all()

    @classmethod
    def get_notifications_by_user_and_serie(cls, user: User, serie: Serie):
        return Notification.query.filter_by(_Notification__user_id=user.id, _Notification__tmdb_id_serie=serie.tmdb_id_serie).order_by(
            desc(Notification._Notification__creation_date)).all()

    @classmethod
    def get_notification_by_id(cls, notification_id: int):
        try:
            return Notification.query.filter_by(_Notification__id=notification_id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    # Method to update
    def mark_as_read(self):
        self.__read = True
        self.save_in_db()
