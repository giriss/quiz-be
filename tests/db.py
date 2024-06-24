from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

engine = create_engine(getenv("DATABASE_URL"), poolclass=StaticPool)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
