from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .utils import IS_DEV_ENV

engine = create_engine(getenv("DATABASE_URL"), echo=IS_DEV_ENV)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
