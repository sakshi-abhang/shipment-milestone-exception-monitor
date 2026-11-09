from datetime import datetime


def calculate_eta_delay(
    planned_arrival: datetime,
    predicted_arrival: datetime | None
):
    if predicted_arrival is None:
        return {
            "has_exception": False,
            "exception_type": None,
            "severity": None,
            "delay_hours": 0,
            "message": "Predicted arrival is not available"
        }

    delay = predicted_arrival - planned_arrival
    delay_hours = delay.total_seconds() / 3600

    if delay_hours < 24:
        return {
            "has_exception": False,
            "exception_type": None,
            "severity": None,
            "delay_hours": round(max(delay_hours, 0), 2),
            "message": "Shipment is within the acceptable ETA range"
        }

    if delay_hours < 48:
        severity = "MEDIUM"
    elif delay_hours <= 72:
        severity = "HIGH"
    else:
        severity = "CRITICAL"

    return {
        "has_exception": True,
        "exception_type": "ETA_DELAY",
        "severity": severity,
        "delay_hours": round(delay_hours, 2),
        "message": f"Shipment is predicted to arrive {round(delay_hours, 2)} hours late"
    }