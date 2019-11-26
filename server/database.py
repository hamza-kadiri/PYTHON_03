from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config

def init_sqlalchemy(Config):
    # Setting the parameters to connect to the database
    engine = create_engine(Config.DATABASE_URI, convert_unicode=True)

    # Creating a session in order to communicate with the database
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    # Creating a base in order to do the queries through the database session
    Base = declarative_base()
    Base.query = db_session.query_property()
    return engine, db_session, Base

engine, db_session, Base = init_sqlalchemy(Config)

def init_models():
    """Function to import the models"""
    import models

def deletion_db():
    """Function permitting to delete the database"""
    #Sorting the tables by dependency between the tables
    for tbl in reversed(Base.metadata.sorted_tables):
        tbl.drop(engine, checkfirst=True)

def creation_db():
    """Function creating the database following the defined model"""
    Base.metadata.create_all(bind=engine)


def initiation_db():
    """Initialize the database by importing the models then deleting the old database and creating the new one"""
    init_models()
    deletion_db()
    creation_db()

def save_obj(obj:Base):
    """Function to save an object in the database through the session"""
    db_session.add(obj)
    db_session.commit()

def delete_obj(obj:Base):
    """Function to delete an object in the database through the session"""
    db_session.delete(obj)
    db_session.commit()