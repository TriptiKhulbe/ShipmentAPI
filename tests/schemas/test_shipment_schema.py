from unittest import TestCase

from src.schemas.shipment_schema import (
    ShipmentDetailRequest,
    ShipmentDetailResponse,
)
from tests.commons.factories import (
    make_address,
    make_article,
    make_carrier,
    make_shipment,
    make_shipment_detail,
    make_status_code,
    make_weather,
)


class TestShipmentSchema(TestCase):
    def setUp(self):
        article = make_article()
        shipment = make_shipment(
            carrier=make_carrier(),
            address=make_address(),
            status=make_status_code(),
        )
        self.shipment_detail = make_shipment_detail(article, shipment)
        self.weather_info = make_weather()

    def test_shipment_detail_request(self):
        request = ShipmentDetailRequest(
            tracking_number="tracking-number", carrier_name="carrier-name"
        )
        self.assertIsNotNone(request.tracking_number)
        self.assertIsNotNone(request.carrier_name)

    def test_shipment_detail_response_without_weather(self):
        response = ShipmentDetailResponse.model_validate(
            {
                "shipments": [
                    self.shipment_detail,
                ],
                "weather_info": None,
            }
        )
        response_shipment = response.shipments[0]
        self.assertEqual(
            response_shipment.article_name, self.shipment_detail.article.name
        )
        self.assertEqual(
            response_shipment.article_sku, self.shipment_detail.article.sku
        )
        self.assertEqual(
            response_shipment.article_price, self.shipment_detail.article.price
        )
        self.assertEqual(
            response_shipment.article_quantity, self.shipment_detail.quantity
        )
        self.assertEqual(
            response_shipment.status, self.shipment_detail.shipment.status.name
        )
        self.assertTrue(
            self.shipment_detail.shipment.receiver_address.street_name
            in response_shipment.receiver_address
        )
        self.assertIsNone(response.weather_info)

    def test_shipment_detail_response_with_weather(self):
        response = ShipmentDetailResponse.model_validate(
            {
                "shipments": [
                    self.shipment_detail,
                ],
                "weather_info": self.weather_info,
            }
        )
        self.assertEqual(
            response.weather_info.description, self.weather_info.description
        )
        self.assertEqual(
            response.weather_info.temperature, self.weather_info.temp
        )
        self.assertEqual(
            response.weather_info.feels_like, self.weather_info.feels_like
        )
        self.assertEqual(
            response.weather_info.temp_min, self.weather_info.temp_min
        )
        self.assertEqual(
            response.weather_info.temp_max, self.weather_info.temp_max
        )
        self.assertEqual(
            response.weather_info.pressure, self.weather_info.pressure
        )
        self.assertEqual(
            response.weather_info.humidity, self.weather_info.humidity
        )
        self.assertEqual(response.weather_info.units, self.weather_info.units)
        self.assertEqual(
            response.weather_info.zip_code, self.weather_info.zip_code
        )