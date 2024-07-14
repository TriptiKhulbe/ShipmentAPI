from datetime import timedelta
from unittest.mock import MagicMock

from src.commons.database import Database
from src.services.weather_service import WeatherService
from tests.commons.factories import make_weather
from tests.services import TestServices


class TestWeatherService(TestServices):
    def setUp(self):
        super().setUp()
        self.weather_info = make_weather()
        self.session = Database.session()
        self.weather_client = MagicMock()
        self.service = WeatherService(self.session, self.weather_client)

    def test_get_weather_detail_from_existing_record(self):
        self.session.add(self.weather_info)
        self.session.commit()
        self.service.get_weather_detail(self.weather_info.zip_code)
        self.weather_client.get_weather_info.assert_not_called()

    def test_get_weather_detail_from_client_api(self):
        self.weather_client.get_weather_info.return_value = self.weather_info
        self.service.get_weather_detail(self.weather_info.zip_code)
        self.weather_client.get_weather_info.assert_called()

    def test_get_weather_detail_from_client_api_for_outdated(self):
        self.weather_info.modified_at = (
            self.weather_info.modified_at - timedelta(hours=3)
        )
        self.session.add(self.weather_info)
        self.session.commit()
        self.weather_client.get_weather_info.return_value = make_weather()
        self.service.get_weather_detail(self.weather_info.zip_code)
        self.weather_client.get_weather_info.assert_called()