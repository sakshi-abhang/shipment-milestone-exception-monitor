from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db
from app.services.exception_engine import calculate_eta_delay

models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Shipment Milestone & Exception Monitor",
    description="API for tracking synthetic shipment milestones and operational exceptions.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Shipment Milestone & Exception Monitor API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/shipments", status_code=201)
def create_shipment(
    shipment: schemas.ShipmentCreate,
    db: Session = Depends(get_db)
):
    new_shipment = models.Shipment(
        shipment_id=shipment.shipment_id,
        container_number=shipment.container_number,
        booking_number=shipment.booking_number,
        origin=shipment.origin,
        destination=shipment.destination,
        planned_departure=shipment.planned_departure,
        planned_arrival=shipment.planned_arrival,
        predicted_arrival=shipment.predicted_arrival,
        status=shipment.status
    )

    db.add(new_shipment)
    db.commit()
    db.refresh(new_shipment)

    return new_shipment

@app.get("/shipments")
def get_shipments(
    db: Session = Depends(get_db)
):
    shipments = db.query(models.Shipment).all()

    return shipments


@app.get("/shipments/{shipment_id}")
def get_shipment(
    shipment_id: str,
    db: Session = Depends(get_db)
):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.shipment_id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    return shipment

@app.put("/shipments/{shipment_id}")
def update_shipment(
    shipment_id: str,
    shipment_data: schemas.ShipmentUpdate,
    db: Session = Depends(get_db)
):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.shipment_id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    shipment.container_number = shipment_data.container_number
    shipment.booking_number = shipment_data.booking_number
    shipment.origin = shipment_data.origin
    shipment.destination = shipment_data.destination
    shipment.planned_departure = shipment_data.planned_departure
    shipment.planned_arrival = shipment_data.planned_arrival
    shipment.predicted_arrival = shipment_data.predicted_arrival
    shipment.status = shipment_data.status

    db.commit()
    db.refresh(shipment)

    return shipment

@app.delete("/shipments/{shipment_id}")
def delete_shipment(
    shipment_id: str,
    db: Session = Depends(get_db)
):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.shipment_id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    db.delete(shipment)
    db.commit()

    return {
        "message": "Shipment deleted successfully"
    }
    
@app.post("/shipments/{shipment_id}/events", status_code=201)
def create_shipment_event(
    shipment_id: str,
    event_data: schemas.ShipmentEventCreate,
    db: Session = Depends(get_db)
):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.shipment_id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    new_event = models.ShipmentEvent(
        shipment_id=shipment_id,
        event_type=event_data.event_type,
        location=event_data.location,
        event_time=event_data.event_time,
        description=event_data.description
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@app.get("/shipments/{shipment_id}/events")
def get_shipment_events(
    shipment_id: str,
    db: Session = Depends(get_db)
):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.shipment_id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    events = db.query(models.ShipmentEvent).filter(
        models.ShipmentEvent.shipment_id == shipment_id
    ).order_by(
        models.ShipmentEvent.event_time
    ).all()

    return events

@app.get("/shipments/{shipment_id}/delay-status")
def get_shipment_delay_status(
    shipment_id: str,
    db: Session = Depends(get_db)
):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.shipment_id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    delay_result = calculate_eta_delay(
        planned_arrival=shipment.planned_arrival,
        predicted_arrival=shipment.predicted_arrival
    )

    return {
        "shipment_id": shipment.shipment_id,
        "planned_arrival": shipment.planned_arrival,
        "predicted_arrival": shipment.predicted_arrival,
        **delay_result
    }
    
@app.post("/shipments/{shipment_id}/exceptions/detect")
def detect_shipment_exception(
    shipment_id: str,
    db: Session = Depends(get_db)
):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.shipment_id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    delay_result = calculate_eta_delay(
        planned_arrival=shipment.planned_arrival,
        predicted_arrival=shipment.predicted_arrival
    )

    if not delay_result["has_exception"]:
        return {
            "shipment_id": shipment_id,
            "message": "No ETA delay exception detected"
        }

    new_exception = models.ShipmentException(
        shipment_id=shipment_id,
        exception_type=delay_result["exception_type"],
        severity=delay_result["severity"],
        message=delay_result["message"],
        resolved=False
    )

    db.add(new_exception)
    db.commit()
    db.refresh(new_exception)

    return new_exception 

@app.get("/exceptions")
def get_exceptions(
    db: Session = Depends(get_db)
):
    exceptions = db.query(
        models.ShipmentException
    ).all()

    return exceptions

@app.get("/shipments/{shipment_id}/exceptions")
def get_shipment_exceptions(
    shipment_id: str,
    db: Session = Depends(get_db)
):
    shipment = db.query(models.Shipment).filter(
        models.Shipment.shipment_id == shipment_id
    ).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found"
        )

    exceptions = db.query(
        models.ShipmentException
    ).filter(
        models.ShipmentException.shipment_id == shipment_id
    ).all()

    return exceptions


@app.patch("/exceptions/{exception_id}/resolve")
def resolve_exception(
    exception_id: int,
    db: Session = Depends(get_db)
):
    exception = db.query(
        models.ShipmentException
    ).filter(
        models.ShipmentException.exception_id == exception_id
    ).first()

    if exception is None:
        raise HTTPException(
            status_code=404,
            detail="Exception not found"
        )

    exception.resolved = True

    db.commit()
    db.refresh(exception)

    return exception