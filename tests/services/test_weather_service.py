from unittest.mock import MagicMock

from src.services.weather_service import WeatherService
from tests.commons.factories import make_weather
from tests.services import TestServices


class TestWeatherService(TestServices):
    def setUp(self):
        super().setUp()
        self.weather_info = make_weather()
        self.weather_client = MagicMock()
        self.cache_client = MagicMock()
        self.service = WeatherService(self.weather_client, self.cache_client)

    def test_get_weather_detail_from_existing_record(self):
        self.cache_client.get.return_value = self.weather_info
        self.service.get_weather_detail(self.weather_info.zip_code)
        self.weather_client.get_weather_info.assert_not_called()

    def test_get_weather_detail_from_client_api(self):
        self.cache_client.get.return_value = None
        self.weather_client.get_weather_info.return_value = self.weather_info
        self.service.get_weather_detail(self.weather_info.zip_code)
        self.weather_client.get_weather_info.assert_called()
