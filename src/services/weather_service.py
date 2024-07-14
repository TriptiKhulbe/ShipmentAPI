from typing import Optional

from src.commons.cache import Cache
from src.commons.entity import Weather
from src.commons.weather_client import WeatherClient
from src.services import Service


class WeatherService(Service):
    def __init__(self, weather_client: WeatherClient, cache: Cache):
        super().__init__()
        self.weather_client = weather_client
        self.cache = cache

    def get_weather_detail(self, zip_code: str) -> Optional[Weather]:
        existing_weather = self.cache.get(zip_code)

        if existing_weather is not None:
            return existing_weather

        self.log.debug(f"requesting weather API in ZIP code - {zip_code}")
        try:
            updated_weather = self.weather_client.get_weather_info(zip_code)
        except Exception as e:
            self.log.exception(e)
            # API request failed, unable to get the weather info.
            return

        # update cache
        self.cache.set(zip_code, updated_weather)

        return updated_weather
