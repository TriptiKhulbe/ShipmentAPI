from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from src.commons.models import TWeather
from src.commons.weather_client import WeatherClient
from src.services import Service


class WeatherService(Service):
    def __init__(self, session: Session, weather_client: WeatherClient):
        super().__init__(session)
        self.weather_client = weather_client

    def get_weather_detail(self, zip_code: str) -> Optional[TWeather]:
        existing_weather = (
            self.session.query(TWeather)
            .filter(TWeather.zip_code == zip_code)
            .first()
        )

        if self.is_valid(existing_weather):
            return existing_weather

        self.log.debug(f"requesting weather API in ZIP code - {zip_code}")
        try:
            updated_weather = self.weather_client.get_weather_info(zip_code)
        except Exception as e:
            self.log.exception(e)
            # API request failed, unable to get the weather info.
            return

        if existing_weather:
            self.session.delete(existing_weather)
            self.session.commit()
        
        self.session.add(updated_weather)
        self.session.commit()

        return updated_weather

    def is_valid(self, weather: TWeather) -> bool:
        """Checks if the weather info was last updated in less than 2 hours
        from the time of request.
        """
        return (weather is not None) and (
            not self._is_outdated(weather.modified_at)
        )

    def _is_outdated(self, timestamp: datetime) -> bool:
        if timestamp.tzinfo is None:
            # If no timezone is provided, assume it's UTC
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return datetime.now(tz=timezone.utc) > timestamp + timedelta(hours=2)
