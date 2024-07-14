from http import HTTPStatus
from unittest.mock import patch

from src.schemas.shipment_schema import (
    ShipmentDetailResponse,
    ShipmentDetailSchema,
    WeatherInfoSchema,
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
from tests.routes import TestRoutes


class TestShipmentRoutes(TestRoutes):
    def setUp(self):
        super().setUp()
        self.shipment_service = patch(
            "src.routes.shipment_routes.ShipmentService"
        ).start()
        self.weather_service = patch(
            "src.routes.shipment_routes.WeatherService"
        ).start()
        article = make_article()
        shipment = make_shipment(
            carrier=make_carrier(),
            address=make_address(),
            status=make_status_code(),
        )
        self.shipment_detail = make_shipment_detail(article, shipment)
        self.weather_info = make_weather()
        self.addCleanup(patch.stopall)

    def test_get_shipment_detail(self):
        self.shipment_service.return_value.get_shipment_detail.return_value = [
            self.shipment_detail
        ]
        self.weather_service.return_value.get_weather_detail.return_value = (
            self.weather_info
        )
        result = self.client.get("/shipment?tracking_number=tn&carrier_name=cn")
        self.assertEqual(result.status_code, HTTPStatus.OK)
        expected_response = ShipmentDetailResponse(
            shipments=[
                ShipmentDetailSchema.model_validate(self.shipment_detail)
            ],
            weather_info=WeatherInfoSchema.model_validate(self.weather_info),
        )
        self.assertEqual(result.json(), expected_response.model_dump())

    def test_get_shipment_detail_without_shipments(self):
        self.shipment_service.return_value.get_shipment_detail.return_value = []
        result = self.client.get("/shipment?tracking_number=tn&carrier_name=cn")
        self.assertEqual(result.status_code, HTTPStatus.OK)
        self.weather_service.return_value.get_weather_detail.assert_not_called()
        expected_response = ShipmentDetailResponse(
            shipments=[], weather_info=None
        )
        self.assertEqual(result.json(), expected_response.model_dump())