from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer

engine = create_engine('postgresql://admin:password@localhost:5432/series_app')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_new_user(self, session):
        session.add(self)
        session.commit()



#Test1
if __name__ == "__main__":
    User1 = User("clem","mdp")
    session = Session()
    User1.add_new_user(session)
    session.close()