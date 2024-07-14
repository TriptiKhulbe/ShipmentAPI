import os

from src.commons.weather_client import OpenWeather

from .database import Database


def get_db_session():
    session = Database.session()
    try:
        yield session
    finally:
        session.close()


def get_weather_client():
    yield OpenWeather(os.environ["API_KEY"])
