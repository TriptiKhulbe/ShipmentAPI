import logging
import os
from logging.handlers import TimedRotatingFileHandler

from dotenv import load_dotenv
from fastapi import FastAPI

from src.commons.database import initialize_database


def create_app() -> FastAPI:
    load_dotenv()

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            TimedRotatingFileHandler(
                "logs/system.log", when="midnight", interval=1
            ),
            logging.StreamHandler(),
        ],
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logging.getLogger("sqlalchemy").setLevel(logging.CRITICAL)

    app = FastAPI()
    initialize_database(
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        hostname=os.environ["POSTGRES_HOSTNAME"],
        port=os.environ["POSTGRES_PORT"],
        database=os.environ["POSTGRES_DB"],
    )

    return app