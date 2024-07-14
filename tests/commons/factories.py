from datetime import datetime, timezone

from src.commons.models import (
    TAddress,
    TArticle,
    TCarrier,
    TShipment,
    TShipmentDetail,
    TStatusCode,
    TWeather,
)


def make_shipment_detail(article: TArticle, shipment: TShipment):
    shipment_detail = TShipmentDetail(
        id=1,
        article_id=article.id,
        shipment_id=shipment.id,
        quantity=1,
    )
    shipment_detail.article = article
    shipment_detail.shipment = shipment
    return shipment_detail


def make_shipment(
    carrier: TCarrier, address: TAddress, status: TStatusCode
) -> TShipment:
    shipment = TShipment(
        id=1,
        tracking_number="tracking-number",
        carrier_id=carrier.id,
        sender_address_id=address.id,
        receiver_address_id=address.id,
        status_id=status.id,
    )
    shipment.carrier = carrier
    shipment.sender_address = address
    shipment.receiver_address = address
    shipment.status = status
    return shipment


def make_carrier() -> TCarrier:
    return TCarrier(
        id=1,
        name="carrier-name",
    )


def make_address() -> TAddress:
    return TAddress(
        id=1,
        street_name="street-name",
        city_name="city-name",
        country_name="country-name",
        zip_code="zip-code",
    )


def make_status_code() -> TStatusCode:
    return TStatusCode(id=1, name="status-code")


def make_article() -> TArticle:
    return TArticle(
        id=1,
        name="article-name",
        price=0.2,
        sku="article-sku",
    )


def make_weather() -> TWeather:
    return TWeather(
        id=1,
        temp=21.42,
        feels_like=21.84,
        temp_min=20.54,
        temp_max=22.32,
        pressure=1011,
        humidity=85,
        description="few clouds",
        units="metric",
        zip_code="zip-code",
        modified_at=datetime.now(tz=timezone.utc),
    )