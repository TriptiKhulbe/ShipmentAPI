from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from src.commons.dependencies import get_db_session, get_weather_client
from src.commons.weather_client import WeatherClient
from src.schemas.shipment_schema import (
    ShipmentDetailRequest,
    ShipmentDetailResponse,
)
from src.services.shipment_service import ShipmentService
from src.services.weather_service import WeatherService

shipment_router = APIRouter(prefix="/shipment", tags=["shipment"])


@shipment_router.get("/", response_model=ShipmentDetailResponse)
def get_shipment_detail(
    session: Annotated[Session, Depends(get_db_session)],
    weather_client: Annotated[WeatherClient, Depends(get_weather_client)],
    request: ShipmentDetailRequest = Depends(),
):
    """Get shipment details along with weather information."""
    shipment_service = ShipmentService(session)
    shipment_details = shipment_service.get_shipment_detail(
        request.tracking_number, request.carrier_name
    )

    if shipment_details:
        weather_service = WeatherService(session, weather_client)
        weather_info = weather_service.get_weather_detail(
            shipment_details[0].shipment.receiver_address.zip_code
        )
    else:
        weather_info = None

    return dict(shipments=shipment_details, weather_info=weather_info)
