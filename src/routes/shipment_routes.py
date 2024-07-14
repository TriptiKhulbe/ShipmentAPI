from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.commons.dependencies import get_db_session
from src.schemas.shipment_schema import (
    ShipmentDetailRequest,
    ShipmentDetailResponse,
)
from src.services.shipment_service import ShipmentService

shipment_router = APIRouter(prefix="/shipment", tags=["shipment"])


@shipment_router.get("/", response_model=ShipmentDetailResponse)
def get_shipment_detail(
    session: Annotated[Session, Depends(get_db_session)],
    request: ShipmentDetailRequest = Depends(),
):
    service = ShipmentService(session)
    shipment_details = service.get_shipment_detail(
        request.tracking_number, request.carrier_name
    )
    return dict(shipments=shipment_details)