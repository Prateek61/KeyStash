from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from models import Base

# Creates engine
engine: Engine = create_engine("sqlite:///data.db")

# Creates database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url)

# Creates tables
Base.metadata.create_all(bind=engine)

# Creates session
SESSION: Session = sessionmaker(bind=engine)()
