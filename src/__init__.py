import os

from dotenv import load_dotenv
from fastapi import FastAPI

from src.commons.database import initialize_database
from src.routes.shipment_routes import shipment_router


def create_app() -> FastAPI:
    load_dotenv()

    app = FastAPI()
    initialize_database(
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        hostname=os.environ["POSTGRES_HOSTNAME"],
        port=os.environ["POSTGRES_PORT"],
        database=os.environ["POSTGRES_DB"],
    )

    app.include_router(shipment_router)
    return app
