from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config

# Setting the parameters to connect to the database
engine = create_engine(Config.DATABASE_URI, convert_unicode=True)

# Creating a session in order to communicate with the database
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
# Creating a base in order to do the queries through the database session
Base = declarative_base()
Base.query = db_session.query_property()

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

def import_data():
    """Function to import some data to test the app"""
    sql = open("data_init.sql", "r")
    text = ""
    for line in sql:
        text += line
    engine.execute(text)


def initiation_db(init_data=False):
    """Initialize the database by importing the models then deleting the old database and creating the new one"""
    init_models()
    deletion_db()
    creation_db()
    if (init_data):
        import_data()

def save_obj(obj:Base):
    """Function to save an object in the database through the session"""
    db_session.add(obj)
    db_session.commit()

def delete_obj(obj:Base):
    """Function to delete an object in the database through the session"""
    db_session.delete(obj)
    db_session.commit()