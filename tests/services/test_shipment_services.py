from src.commons.database import Database
from src.commons.models import TShipmentDetail
from src.services.shipment_service import ShipmentService
from tests.commons.factories import (
    make_address,
    make_article,
    make_carrier,
    make_shipment,
    make_shipment_detail,
    make_status_code,
)
from tests.services import TestServices


class TestShipmentService(TestServices):
    def setUp(self):
        super().setUp()
        article = make_article()
        shipment = make_shipment(
            carrier=make_carrier(),
            address=make_address(),
            status=make_status_code(),
        )
        self.shipment_detail = make_shipment_detail(article, shipment)
        self.session = Database.session()
        self.session.add(self.shipment_detail)
        self.session.commit()
        self.service = ShipmentService(self.session)

    def test_get_shipment_detail(self):
        result = self.service.get_shipment_detail(
            "tracking-number", "carrier-name"
        )
        self.assertEqual(len(result), 1)
        self.assertTrue(isinstance(result[0], TShipmentDetail))
        self.assertEqual(result[0].id, self.shipment_detail.id)
        self.assertEqual(result[0].article_id, self.shipment_detail.article_id)
        self.assertEqual(
            result[0].shipment_id, self.shipment_detail.shipment_id
        )
        self.assertEqual(result[0].quantity, self.shipment_detail.quantity)
