from typing import List

from sqlalchemy.sql.expression import and_

from src.commons.models import TCarrier, TShipment, TShipmentDetail
from src.services import Service


class ShipmentService(Service):
    def get_shipment_detail(
        self, tracking_number: str, carrier_name: str
    ) -> List[TShipmentDetail]:
        return (
            self.session.query(TShipmentDetail)
            .join(TShipment)
            .join(TCarrier)
            .filter(
                and_(
                    TShipment.tracking_number == tracking_number,
                    TCarrier.name == carrier_name,
                )
            )
            .all()
        )
