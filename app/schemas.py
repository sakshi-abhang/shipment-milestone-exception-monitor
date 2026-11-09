from datetime import datetime

from pydantic import BaseModel


class ShipmentCreate(BaseModel):
    shipment_id: str
    container_number: str
    booking_number: str
    origin: str
    destination: str
    planned_departure: datetime
    planned_arrival: datetime
    predicted_arrival: datetime | None = None
    status: str = "BOOKED"
    
class ShipmentUpdate(BaseModel):
    container_number: str
    booking_number: str
    origin: str
    destination: str
    planned_departure: datetime
    planned_arrival: datetime
    predicted_arrival: datetime | None = None
    status: str
    
class ShipmentEventCreate(BaseModel):
    event_type: str
    location: str
    event_time: datetime
    description: str | None = None
