import logging
from abc import ABC, abstractmethod

import requests

from src.commons.models import TWeather


class WeatherClient(ABC):
    TIMEOUT = 10

    @abstractmethod
    def get_weather_info(self, zip_code: str) -> TWeather:
        pass


class OpenWeather(WeatherClient):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    UNITS = "metric"

    def __init__(self, api_key: str):
        self.log = logging.getLogger(self.__class__.__name__)
        self.api_key = api_key

    def get_weather_info(self, zip_code: str) -> TWeather:
        response = requests.get(
            self.URL,
            params={
                "q": zip_code,
                "APPID": self.api_key,
                "units": self.UNITS,
            },
            timeout=self.TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        return TWeather(
            temp=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            pressure=data["main"]["pressure"],
            humidity=data["main"]["humidity"],
            description=data["weather"][0]["description"],
            units=self.UNITS,
            zip_code=zip_code,
        )
