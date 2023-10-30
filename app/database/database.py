from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta, sessionmaker

from config import DB_HOST, DB_PORT, DB_NAME, DB_PASS, DB_USER

database_url = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


engine = create_engine(database_url)
Base: DeclarativeMeta = declarative_base()
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
