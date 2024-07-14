from dataclasses import dataclass, field 
from datetime import datetime, timezone


@dataclass
class Weather:
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: float
    humidity: float
    description: str
    units: str  # imperial, metric, standard
    zip_code: str
    modified_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Weather-{self.zip_code}>"
