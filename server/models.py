from sqlalchemy import Table, Column, Integer, SmallInteger, Numeric, String, ForeignKey, UniqueConstraint, desc, inspect
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm import relationship
from database import Base
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import current_app as app
from time import time
from database import save_obj
from tmdb_api import get_tv_serie

class EqMixin(object):
    def compare_value(self):
        """Return a value or tuple of values to use for comparisons.
        Return instance's primary key by default, which requires that it is persistent in the database.
        Override this in subclasses to get other behavior.
        """
        return inspect(self).identity

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self.compare_value() == other.compare_value()

    def __ne__(self, other):
        eq = self.__eq__(other)

        if eq is NotImplemented:
            return eq

        return not eq

    def __hash__(self):
        return hash(self.__class__) ^ hash(self.compare_value())

subscriptions_table = Table('subscriptions', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('tmdb_id_serie', Integer, ForeignKey('series.tmdb_id_serie'))
)

series_genres_table = Table('series_genres', Base.metadata,
    Column('tmdb_id_genre', Integer, ForeignKey('genres.tmdb_id_genre')),
    Column('tmdb_id_serie', Integer, ForeignKey('series.tmdb_id_serie'))
)
series_productors_table = Table('series_productors', Base.metadata,
    Column('tmdb_id_productor', Integer, ForeignKey('productors.tmdb_id')),
    Column('tmdb_id_serie', Integer, ForeignKey('series.tmdb_id_serie')))

class Person():
    tmdb_id = Column(Integer, primary_key=True)
    credit_id = Column(String)
    name = Column(String)
    profile_path = Column(String)
    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path:str):
        self.tmdb_id = tmdb_id
        self.credit_id = credit_id
        self.name = name
        self.profile_path = profile_path

    def as_dict(self):
        return {'tmdb_id':self.tmdb_id, 'credit_id':self.credit_id,'name':self.name,'profile_path':self.profile_path}

class Actor(Person, Base):
    __tablename__ = 'actors'
    department = Column(String)
    job = Column(String)

    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path: str, department: str, job: str):
        Person.__init__(self, tmdb_id, credit_id, name, profile_path)
        self.department = department
        self.job = job

    def as_dict(self):
        d = {'department':self.department,'job':self.job}
        d.update(super(Person,self).as_dict())
        return d

class Productor(Person, Base):
    __tablename__ = 'productors'
    gender = Column(String)
    series = relationship("Serie", secondary=series_productors_table, back_populates="productors")

    def __init__(self, tmdb_id: int, credit_id: str, name: str, profile_path: str, gender: int):
        Person.__init(self, tmdb_id, credit_id, name, profile_path)
        self.gender = gender

    @classmethod
    def get_productor_by_id(cls, tmdb_id):
        return Productor.query.filter_by(tmdb_id=tmdb_id).one()

    def as_dict(self):
        d = {'gender':self.gender}
        d.update(super(Person,self).as_dict())
        return d

class Serie(Base, EqMixin):
    __tablename__ = 'series'
    tmdb_id_serie = Column(Integer, primary_key=True)
    name = Column(String)
    overview = Column(String)
    backdrop_path = Column(String, nullable=True)
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
    productors = relationship("Productor", secondary=series_productors_table, back_populates="series")
    genres = relationship("Genre", secondary=series_genres_table, back_populates="series")
    users = relationship("User", secondary=subscriptions_table, back_populates="series")

    def __init__(self, tmdb_id_serie, name, overview, backdrop_path, nb_seasons, nb_episodes, next_episode_name, next_episode_air_date, next_episode_season_number, next_episode_episode_number, vote_count, vote_average, genres):
        self.tmdb_id_serie = tmdb_id_serie
        self.name = name
        self.overview = overview
        self.backdrop_path = backdrop_path
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

    def save_in_db(self):
        save_obj(self)

    def update_info(self, name, overview, backdrop_path, nb_seasons, nb_episodes, next_episode_name,next_episode_air_date, next_episode_season_number,next_episode_episode_number,  vote_count, vote_average, genres):
        self.name = name
        self.overview = overview
        self.backdrop_path = backdrop_path
        self.nb_seasons = nb_seasons
        self.nb_episodes = nb_episodes
        self.next_episode_name = next_episode_name
        self.next_episode_air_date = next_episode_air_date
        self.next_episode_season_number = next_episode_season_number
        self.next_episode_episode_number = next_episode_episode_number
        self.vote_count = vote_count
        self.vote_average = vote_average
        self.last_update = time()
        self.genres = genres
        save_obj(self)

    def update_from_json(self, json):
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
        serie_genres = []
        for genre in json['genres']:
            new_genre = Genre.get_genre_by_id(genre['id'])
            if new_genre is None:
                new_genre = Genre(genre['id'], genre['name'])
            serie_genres.append(new_genre)
        return self.update_info(json['name'], json['overview'], json['backdrop_path'], json['number_of_seasons'], json['number_of_episodes'], next_episode_name, next_episode_air_date, next_episode_season_number, next_episode_episode_number, json['vote_count'], json['vote_average'], serie_genres)

    def compare_value(self):
        return self.tmdb_id_serie

    @classmethod
    def get_serie_by_id(cls, tmdb_id_serie: int):
        try:
            return Serie.query.filter_by(tmdb_id_serie=tmdb_id_serie).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    @classmethod
    def from_json(cls, json):
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
        serie_genres = []
        for genre in json['genres']:
            new_genre = Genre.get_genre_by_id(genre['id'])
            if new_genre is None:
                new_genre = Genre(genre['id'], genre['name'])
                save_obj(new_genre)
            serie_genres.append(new_genre)
        return Serie(json['id'], json['name'], json['overview'], json['backdrop_path'], json['number_of_seasons'], json['number_of_episodes'], next_episode_name, next_episode_air_date, next_episode_season_number, next_episode_episode_number, json['vote_count'], json['vote_average'], serie_genres)

    def as_dict(self):
        return {'tmdb_id_serie': self.tmdb_id_serie,'name': self.name,'overview': self.overview,'backdrop_path': self.backdrop_path,
                'nb_seasons': self.nb_seasons,'nb_episodes': self.nb_episodes,'next_episode_name': self.next_episode_name,'next_episode_air_date': self.next_episode_air_date, 'next_episode_season_number': self.next_episode_season_number,'next_episode_episode_number': self.next_episode_episode_number,
                'vote_count': self.vote_count,'genres': self.genres}

class User(Base, EqMixin):
    __tablename__ = 'users'
    id = Column(SmallInteger, primary_key=True)
    username = Column(String(20), unique=True)
    email = Column(String(80))
    password_hash = Column(String(128))
    series = relationship("Serie", secondary=subscriptions_table, back_populates="users")

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

    def generate_auth_token(self, expiration=6000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @classmethod
    def get_user_by_id(cls, id: int):
        try:
            return User.query.filter_by(id=id).one()
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

    def get_favorite_series(self):
        return Serie.query.join(User.series).filter(User.id == self.id).all()

    def add_favorite_serie(self, serie:Serie):
        self.series.append(serie)
        save_obj(self)

    def delete_favorite_serie(self, serie:Serie):
        self.series.remove(serie)
        save_obj(self)

    def update_series(self):
        current_time = time()
        for serie in self.series:
            if (serie.last_update < current_time - 24 * 3600):
                old_last_diff = serie.next_episode_air_date
                new_serie_json = get_tv_serie(serie.tmdb_id_serie)
                serie.update_from_json(new_serie_json)  # update serie information
                save_obj(serie)
                if (old_last_diff != serie.next_episode_air_date and serie.next_episode_air_date != "null"):
                    new_notif = Notification.from_serie(self.user_id, serie)  # create notification
                    save_obj(new_notif)

class Genre(Base):
    __tablename__ = 'genres'
    tmdb_id_genre = Column(SmallInteger, primary_key=True)
    name = Column(String)
    series = relationship("Serie", secondary=series_genres_table, back_populates="genres")

    def __init__(self, tmdb_id_genre, name):
        self.tmdb_id_genre = tmdb_id_genre
        self.name = name

    @classmethod
    def get_genre_by_id(cls, id):
        return Genre.query.filter_by(tmdb_id_genre=id).one()

    def as_dict(self):
        return {'tmdb_id_genre':self.tmdb_id_genre,'name':self.name}

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(SmallInteger, primary_key=True)
    user_id = Column(SmallInteger, )
    tmdb_serie_id = Column(Integer)
    serie_name = Column(String)
    name = Column(String)
    season = Column(SmallInteger)
    episode = Column(SmallInteger)
    next_date = Column(String)
    creation_date = Column(Integer)
    read = Column(SmallInteger)

    def __init__(self,user_id, tmdb_serie_id, serie_name, name, season, episode, next_date):
        self.user_id = user_id
        self.tmdb_serie_id = tmdb_serie_id
        self.serie_name = serie_name
        self.name = name
        self.season = season
        self.episode = episode
        self.next_date = next_date
        self.creation_date = time()
        self.read = 0

    def mark_as_read(self):
        self.read = 1
        save_obj(self)

    def save_in_db(self):
        save_obj(self)

    @classmethod
    def from_serie(cls, user_id, serie:Serie):
        return Notification(user_id, serie.tmdb_id_serie, serie.name, serie.next_episode_name, serie.next_episode_season_number, serie.next_episode_episode_number, serie.next_episode_air_date)

    @classmethod
    def get_notifications_by_user(cls, user:User):
        return Notification.query.filter_by(user_id=user.id).order_by(desc(Notification.creation_date)).limit(15).all()

    @classmethod
    def get_notification_by_id(cls, id):
        try:
            return Notification.query.filter_by(id=id).one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    def as_dict(self):
        return {'id':self.id, 'user_id':self.user_id, 'tmdb_serie_id':self.tmdb_serie_id, 'serie_name': self.serie_name, 'name':self.name, 'episode':self.episode,'season':self.season,'next_date':self.next_date, 'read': self.read}