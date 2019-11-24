from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Config

engine = create_engine(Config.DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_models():
    import models

def deletion_db():
    for tbl in reversed(Base.metadata.sorted_tables):
        tbl.drop(engine)

def creation_db():
    Base.metadata.create_all(bind=engine)

def initiation_db():
    init_models()
    deletion_db()
    creation_db()

def save_obj(obj:Base):
    db_session.add(obj)
    db_session.commit()

def delete_obj(obj:Base):
    db_session.delete(obj)
    db_session.commit()