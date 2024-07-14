from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

SQLALCHEMY_URL = (
    "postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database}"
)


class Database:
    engine: Engine
    session: scoped_session[Session]


def initialize_database(
    username: str, password: str, hostname: str, port: str, database: str
):
    connection_uri = SQLALCHEMY_URL.format(
        username=username,
        password=password,
        hostname=hostname,
        port=port,
        database=database,
    )
    Database.engine = create_engine(connection_uri)
    Database.session = scoped_session(sessionmaker(bind=Database.engine))
