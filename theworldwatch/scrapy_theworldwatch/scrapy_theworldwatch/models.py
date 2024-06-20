from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LastVideo(Base):
    __tablename__ = "last_video"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    profile_url = Column(String)
    last_active = Column(DateTime)
