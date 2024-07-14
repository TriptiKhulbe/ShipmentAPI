import os

from src.commons.cache import RedisCache
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


def get_cache_client():
    yield RedisCache(os.environ["REDIS_HOST"], int(os.environ["REDIS_TTL"]))
