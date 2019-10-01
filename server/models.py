from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base



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

class Serie(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)
    id_tmdb = Column(Integer)
    title = Column(String(80))

    def __init__(self, id_tmdb, title):
        self.id_tmdb = id_tmdb
        self.title = title


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id')
    serie_id = Column(Integer, ForeignKey('Serie_id'))

    def __init__(self, user_id, serie_id):
        self.user_id = user_id
        self.serie_id = serie_id
