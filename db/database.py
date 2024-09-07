from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.getenv("DATABASE_URL", ""), pool_pre_ping=True)
default_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
