import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import Database
from .models import (
    Model,
    TAddress,
    TArticle,
    TCarrier,
    TShipment,
    TShipmentDetail,
    TStatusCode,
)


def clean_db():
    session = Database.session()
    for tbl in reversed(Model.metadata.sorted_tables):
        try:
            session.execute(text("DROP TABLE IF EXISTS " + tbl.name))
            session.commit()
        except Exception as e:
            print(e)
            print("Skipping %r" % tbl)
    session.commit()
    session.close()


def init_db():
    session = Database.session()
    Model.metadata.drop_all(Database.engine)
    Model.metadata.create_all(Database.engine)
    session.commit()
    session.close()


def load_csv(filename: str):
    session = Database.session()

    df = pd.read_csv(filename)
    count_ = 1
    for _, row in df.iterrows():
        if count_ == 8:
            breakpoint()
        count_ +=1
        carrier = _get_or_create_carrier(session, row["carrier"])
        article = _get_or_create_article(
            session, row["article_name"], row["article_price"], row["SKU"]
        )
        sender_address = _get_or_create_address(session, row["sender_address"])
        receiver_address = _get_or_create_address(
            session, row["receiver_address"]
        )
        status = _get_or_create_status(session, row["status"])
        shipment = _get_or_create_shipment(
            session,
            row["tracking_number"],
            carrier.id,
            sender_address.id,
            receiver_address.id,
            status.id,
        )
        _create_shipment_detail(
            session, shipment.id, article.id, row["article_quantity"]
        )
    print(f"{len(df)} records loaded successfully.")
    session.close()


def _get_or_create_carrier(session: Session, carrier_name: str) -> TCarrier:
    carrier = (
        session.query(TCarrier).filter(TCarrier.name == carrier_name).first()
    )
    if carrier is None:
        carrier = TCarrier(name=carrier_name)
        session.add(carrier)
        session.commit()
    return carrier


def _get_or_create_address(session: Session, address: str) -> TAddress:
    street_name, zip_code_city, country = address.split(",")
    zip_code, city = zip_code_city.strip().split(" ")
    record = (
        session.query(TAddress)
        .filter(
            TAddress.street_name == street_name,
            TAddress.zip_code == zip_code,
            TAddress.city_name == city,
            TAddress.country_name == country,
        )
        .first()
    )
    if record is None:
        record = TAddress(
            street_name=street_name,
            zip_code=zip_code,
            city_name=city,
            country_name=country,
        )
        session.add(record)
        session.commit()
    return record


def _get_or_create_article(
    session: Session,
    name: str,
    price: float,
    sku: str,
) -> TArticle:
    article = session.query(TArticle).filter(TArticle.sku == sku).first()
    if article is None:
        article = TArticle(
            name=name,
            price=price,
            sku=sku,
        )
        session.add(article)
        session.commit()
    return article


def _get_or_create_status(session: Session, status: str) -> TStatusCode:
    record = (
        session.query(TStatusCode).filter(TStatusCode.name == status).first()
    )
    if record is None:
        record = TStatusCode(
            name=status,
        )
        session.add(record)
        session.commit()
    return record


def _get_or_create_shipment(
    session: Session,
    tracking_number: str,
    carrier_id: int,
    sender_address_id: int,
    receiver_address_id: int,
    status_id: int,
) -> TShipment:
    record = (
        session.query(TShipment)
        .filter(TShipment.tracking_number == tracking_number)
        .first()
    )
    if record is None:
        record = TShipment(
            tracking_number=tracking_number,
            carrier_id=carrier_id,
            sender_address_id=sender_address_id,
            receiver_address_id=receiver_address_id,
            status_id=status_id,
        )
        session.add(record)
        session.commit()
    return record


def _create_shipment_detail(
    session: Session, shipment_id: int, article_id: int, quantity: int
):
    record = TShipmentDetail(
        article_id=article_id,
        shipment_id=shipment_id,
        quantity=quantity,
    )
    session.add(record)
    session.commit()