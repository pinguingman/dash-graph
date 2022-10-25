from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
