from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///instance/sample.sqlite')
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String)
    password = Column(String)
    role = Column(String)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


# Base.metadata.create_all(engine)
