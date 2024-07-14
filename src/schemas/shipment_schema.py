from datetime import datetime, timedelta, timezone
from typing import List, Optional

from pydantic import AliasPath, BaseModel, ConfigDict, Field, computed_field


class ShipmentDetailRequest(BaseModel):
    tracking_number: str = Field(max_length=15)
    carrier_name: str = Field(max_length=20)


class StatusCodeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class AddressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    street_name: str
    city_name: str
    country_name: str
    zip_code: str


class ShipmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    receiver_address: AddressSchema
    status: StatusCodeSchema


class ShipmentDetailSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    article_name: str = Field(validation_alias=AliasPath("article", "name"))
    article_sku: str = Field(validation_alias=AliasPath("article", "sku"))
    article_price: float = Field(validation_alias=AliasPath("article", "price"))
    article_quantity: int = Field(validation_alias="quantity")
    shipment: ShipmentSchema = Field(exclude=True)
    status: str = Field(
        validation_alias=AliasPath("shipment", "status", "name")
    )

    @computed_field
    @property
    def receiver_address(self) -> str:
        address = self.shipment.receiver_address
        return (
            f"{address.street_name}, {address.zip_code} "
            f"{address.city_name}, {address.country_name}"
        )


class WeatherInfoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    temperature: float = Field(validation_alias="temp")
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: float
    description: str
    units: str
    zip_code: str
    modified_at: datetime = Field(exclude=True)

    @computed_field
    @property
    def last_updated_on(self) -> str:
        now = datetime.now(tz=timezone.utc)
        delta = now - self.modified_at
        if delta < timedelta(minutes=1):
            return "just now"
        elif delta < timedelta(hours=1):
            minutes = delta.seconds // 60
            return f"{minutes} minute(s) ago"
        elif delta < timedelta(days=1):
            hours = delta.seconds // 3600
            return f"{hours} hour(s) ago"
        return self.modified_at.strftime("%Y-%m-%d %H:%M:%S")


class ShipmentDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    shipments: List[ShipmentDetailSchema]
    weather_info: Optional[WeatherInfoSchema]
