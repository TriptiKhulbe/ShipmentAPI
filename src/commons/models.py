from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.sql import func

Model = declarative_base()


class TArticle(Model):
    __tablename__ = "t_article"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    price: Mapped[float] = mapped_column(Float)
    sku: Mapped[str] = mapped_column(String(10))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<TArticle-{self.sku}>"


class TAddress(Model):
    __tablename__ = "t_address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    street_name: Mapped[str] = mapped_column(String(100))
    city_name: Mapped[str] = mapped_column(String(50))
    country_name: Mapped[str] = mapped_column(String(20))
    zip_code: Mapped[str] = mapped_column(String(10))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TAddress-{self.zip_code}>"


class TStatusCode(Model):
    __tablename__ = "t_status_code"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(25))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f"<TStatus-{self.name}>"


class TShipment(Model):
    __tablename__ = "t_shipment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tracking_number: Mapped[str] = mapped_column(String(15), index=True)

    carrier_id: Mapped[int] = mapped_column(Integer, ForeignKey("t_carrier.id"), index=True)
    carrier = relationship("TCarrier", backref="shipments", uselist=False)

    sender_address_id: Mapped[int] = mapped_column(Integer, ForeignKey("t_address.id"))
    sender_address = relationship(
        "TAddress",
        backref="sent_shipments",
        foreign_keys=[sender_address_id],
        uselist=False,
    )

    receiver_address_id: Mapped[int] = mapped_column(Integer, ForeignKey("t_address.id"))
    receiver_address: Mapped[TAddress] = relationship(
        "TAddress",
        backref="received_shipments",
        foreign_keys=[receiver_address_id],
        uselist=False,
    )

    status_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("t_status_code.id")
    )
    status: Mapped[TStatusCode] = relationship(
        "TStatusCode", backref="shipments", uselist=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<TShipment-{self.tracking_number}>"


class TShipmentDetail(Model):
    __tablename__ = "t_shipment_detail"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("t_article.id"))
    article: Mapped[TArticle] = relationship(
        "TArticle", backref="shipment_detail", uselist=False
    )

    shipment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("t_shipment.id")
    )
    shipment: Mapped[TShipment] = relationship(
        "TShipment", backref="shipment_detail", uselist=False
    )
    quantity: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self):
        return f"<TShipmentDetail-{self.id}>"


class TCarrier(Model):
    __tablename__ = "t_carrier"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(20), index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TCarrier-{self.name}>"


class TWeather(Model):
    __tablename__ = "t_weather"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    temp: Mapped[float] = mapped_column(Float)
    feels_like: Mapped[float] = mapped_column(Float)
    temp_min: Mapped[float] = mapped_column(Float)
    temp_max: Mapped[float] = mapped_column(Float)
    pressure: Mapped[float] = mapped_column(Float)
    humidity: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(50))
    units: Mapped[str] = mapped_column(String(15))  # imperial, metric, standard
    zip_code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    
    def __repr__(self):
        return f"<TWeather-{self.zip_code}>"

