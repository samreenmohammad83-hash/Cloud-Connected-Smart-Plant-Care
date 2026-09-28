from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Device, WateringEvent, Alert
from ..config import MAX_WATERING_SECONDS, COOLDOWN_SECONDS, HIGH_TEMP_THRESHOLD

PLANT_PROFILES = {
    "SUCCULENT": 20,
    "TOMATO": 40,
    "HERB": 35,
    "INDOOR_PLANT": 30,
}

def plant_threshold(plant_type: str) -> float:
    return PLANT_PROFILES.get(plant_type.upper(), 30)

def cooldown_complete(db: Session, device_id: str) -> bool:
    last = db.query(WateringEvent).filter_by(device_id=device_id)\
        .order_by(WateringEvent.timestamp.desc()).first()
    if not last:
        return True
    return (datetime.utcnow() - last.timestamp).total_seconds() >= COOLDOWN_SECONDS

def process_reading(db: Session, device: Device, moisture: float, temperature: float):
    if temperature > HIGH_TEMP_THRESHOLD:
        db.add(Alert(device_id=device.device_id, alert_type="HIGH_TEMPERATURE",
                     level="WARNING",
                     message=f"{device.plant_name} temperature exceeded {HIGH_TEMP_THRESHOLD}°C."))

    if moisture < device.moisture_threshold:
        db.add(Alert(device_id=device.device_id, alert_type="LOW_SOIL_MOISTURE",
                     level="WARNING",
                     message=f"{device.plant_name} moisture dropped below {device.moisture_threshold:.0f}%."))

    if device.auto_water and moisture < device.moisture_threshold and cooldown_complete(db, device.device_id):
        event = WateringEvent(
            device_id=device.device_id, trigger_type="AUTO",
            moisture_before=moisture, duration=MAX_WATERING_SECONDS
        )
        db.add(event)
        return {"watering_triggered": True, "duration": MAX_WATERING_SECONDS}
    return {"watering_triggered": False, "duration": 0}
