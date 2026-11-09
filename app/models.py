from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.database import Base


class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id = Column(
        String,
        primary_key=True,
        index=True
    )

    container_number = Column(
        String,
        nullable=False
    )

    booking_number = Column(
        String,
        nullable=False
    )

    origin = Column(
        String,
        nullable=False
    )

    destination = Column(
        String,
        nullable=False
    )

    planned_departure = Column(
        DateTime,
        nullable=False
    )

    planned_arrival = Column(
        DateTime,
        nullable=False
    )

    predicted_arrival = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String,
        nullable=False,
        default="BOOKED"
    )
    
class ShipmentEvent(Base):
    __tablename__ = "shipment_events"

    event_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    shipment_id = Column(
        String,
        ForeignKey("shipments.shipment_id"),
        nullable=False
    )

    event_type = Column(
        String,
        nullable=False
    )

    location = Column(
        String,
        nullable=False
    )

    event_time = Column(
        DateTime,
        nullable=False
    )

    description = Column(
        String,
        nullable=True
    )
    

class ShipmentException(Base):
    __tablename__ = "shipment_exceptions"

    exception_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    shipment_id = Column(
        String,
        ForeignKey("shipments.shipment_id"),
        nullable=False
    )

    exception_type = Column(
        String,
        nullable=False
    )

    severity = Column(
        String,
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    resolved = Column(
        Boolean,
        nullable=False,
        default=False
    )