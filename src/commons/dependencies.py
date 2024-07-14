from .database import Database


def get_db_session():
    session = Database.session()
    try:
        yield session
    finally:
        session.close()
