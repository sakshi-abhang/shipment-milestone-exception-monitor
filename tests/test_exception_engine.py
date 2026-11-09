from datetime import datetime

from app.services.exception_engine import calculate_eta_delay


def test_on_time_shipment():
    planned_arrival = datetime(
        2026, 11, 21, 10, 0
    )

    predicted_arrival = datetime(
        2026, 11, 21, 10, 0
    )

    result = calculate_eta_delay(
        planned_arrival,
        predicted_arrival
    )

    assert result["has_exception"] is False
    assert result["severity"] is None
    assert result["delay_hours"] == 0
    
def test_24_hour_delay_is_medium():
    planned_arrival = datetime(
        2026, 11, 20, 10, 0
    )

    predicted_arrival = datetime(
        2026, 11, 21, 10, 0
    )

    result = calculate_eta_delay(
        planned_arrival,
        predicted_arrival
    )

    assert result["has_exception"] is True
    assert result["exception_type"] == "ETA_DELAY"
    assert result["severity"] == "MEDIUM"
    assert result["delay_hours"] == 24
    
def test_48_hour_delay_is_high():
    planned_arrival = datetime(
        2026, 11, 20, 10, 0
    )

    predicted_arrival = datetime(
        2026, 11, 22, 10, 0
    )

    result = calculate_eta_delay(
        planned_arrival,
        predicted_arrival
    )

    assert result["has_exception"] is True
    assert result["exception_type"] == "ETA_DELAY"
    assert result["severity"] == "HIGH"
    assert result["delay_hours"] == 48
    
def test_72_hour_delay_is_high():
    planned_arrival = datetime(
        2026, 11, 20, 10, 0
    )

    predicted_arrival = datetime(
        2026, 11, 23, 10, 0
    )

    result = calculate_eta_delay(
        planned_arrival,
        predicted_arrival
    )

    assert result["has_exception"] is True
    assert result["severity"] == "HIGH"
    assert result["delay_hours"] == 72
    
def test_delay_over_72_hours_is_critical():
    planned_arrival = datetime(
        2026, 11, 20, 10, 0
    )

    predicted_arrival = datetime(
        2026, 11, 24, 10, 0
    )

    result = calculate_eta_delay(
        planned_arrival,
        predicted_arrival
    )

    assert result["has_exception"] is True
    assert result["severity"] == "CRITICAL"
    assert result["delay_hours"] == 96
    
def test_missing_predicted_arrival():
    planned_arrival = datetime(
        2026, 11, 20, 10, 0
    )

    predicted_arrival = None

    result = calculate_eta_delay(
        planned_arrival,
        predicted_arrival
    )

    assert result["has_exception"] is False
    assert result["exception_type"] is None
    assert result["severity"] is None
    assert result["delay_hours"] == 0