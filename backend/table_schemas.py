from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import Column, Integer, String
base = declarative_base()

class User(base):
    __tablename__ = 'users' # __table__ or __tablename__
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(String)
    email=Column(String)
    password=Column(String)
    
class User2(base):
    __tablename__ = 'users2' # __table__ or __tablename__
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    

        