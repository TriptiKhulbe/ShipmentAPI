from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.commons.database import Database


def initialize_memory_database():
    Database.engine = create_engine("sqlite:///:memory:", echo=True)
    Database.session = scoped_session(sessionmaker(bind=Database.engine))
