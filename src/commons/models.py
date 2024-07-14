from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Model = declarative_base()


class TArticle(Model):
    __tablename__ = "t_article"

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    price = Column(Float)
    sku = Column(String(10))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<TArticle-{self.sku}>"


class TShipment(Model):
    __tablename__ = "t_shipment"

    id = Column(Integer, primary_key=True)
    tracking_number = Column(String(15), index=True)

    carrier_id = Column(Integer, ForeignKey("t_carrier.id"), index=True)
    carrier = relationship("TCarrier", backref="shipments", uselist=False)

    sender_address_id = Column(Integer, ForeignKey("t_address.id"))
    sender_address = relationship(
        "TAddress",
        backref="sent_shipments",
        foreign_keys=[sender_address_id],
        uselist=False,
    )

    receiver_address_id = Column(Integer, ForeignKey("t_address.id"))
    receiver_address = relationship(
        "TAddress",
        backref="received_shipments",
        foreign_keys=[receiver_address_id],
        uselist=False,
    )

    status_id = Column(Integer, ForeignKey("t_status_code.id"))
    status = relationship("TStatusCode", backref="shipments", uselist=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<TShipment-{self.tracking_number}>"


class TShipmentDetail(Model):
    __tablename__ = "t_shipment_detail"

    id = Column(Integer, primary_key=True)

    article_id = Column(Integer, ForeignKey("t_article.id"))
    article = relationship("TArticle", backref="shipment_detail", uselist=False)

    shipment_id = Column(Integer, ForeignKey("t_shipment.id"))
    shipment = relationship(
        "TShipment", backref="shipment_detail", uselist=False
    )
    quantity = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TShipmentDetail-{self.id}>"


class TStatusCode(Model):
    __tablename__ = "t_status_code"

    id = Column(Integer, primary_key=True)
    name = Column(String(25))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TStatus-{self.name}>"


class TCarrier(Model):
    __tablename__ = "t_carrier"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TCarrier-{self.name}>"


class TAddress(Model):
    __tablename__ = "t_address"

    id = Column(Integer, primary_key=True)
    street_name = Column(String(100))
    city_name = Column(String(50))
    country_name = Column(String(20))
    zip_code = Column(String(10))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<TAddress-{self.zip_code}>"


class TWeather(Model):
    __tablename__ = "t_weather"

    id = Column(Integer, primary_key=True)
    temp = Column(Float)
    feels_like = Column(Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    description = Column(String(50))
    units = Column(String(15))  # imperial, metric, standard
    zip_code = Column(String(10), unique=True, index=True)
    modified_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<TWeather-{self.zip_code}>"
