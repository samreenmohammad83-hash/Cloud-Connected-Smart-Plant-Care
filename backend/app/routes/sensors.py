from datetime import datetime
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Device, SensorReading
from ..security import verify_device_key
from ..services.automation import process_reading

router = APIRouter()

class SensorData(BaseModel):
    device_id: str
    soil_moisture: float = Field(ge=0, le=100)
    temperature: float = Field(ge=-20, le=80)
    humidity: float = Field(ge=0, le=100)
    light_level: float = Field(ge=0, le=100)
    timestamp: datetime | None = None

@router.post("/sensors/data")
def receive_sensor_data(payload: SensorData, db: Session = Depends(get_db), _: bool = Depends(verify_device_key)):
    device = db.get(Device, payload.device_id)
    if not device: raise HTTPException(404, "Device not registered")
    reading = SensorReading(
        device_id=payload.device_id,
        soil_moisture=payload.soil_moisture,
        temperature=payload.temperature,
        humidity=payload.humidity,
        light_level=payload.light_level,
        timestamp=payload.timestamp or datetime.utcnow()
    )
    device.last_seen = datetime.utcnow()
    db.add(reading)
    decision = process_reading(db, device, payload.soil_moisture, payload.temperature)
    db.commit()
    return {"message": "reading accepted", "reading_id": reading.reading_id, **decision}

@router.get("/devices/{device_id}/latest")
def latest(device_id: str, db: Session = Depends(get_db)):
    r = db.query(SensorReading).filter_by(device_id=device_id).order_by(SensorReading.timestamp.desc()).first()
    if not r: raise HTTPException(404, "No readings found")
    return r

@router.get("/devices/{device_id}/history")
def history(device_id: str, limit: int = 100, db: Session = Depends(get_db)):
    limit = min(max(limit, 1), 1000)
    return db.query(SensorReading).filter_by(device_id=device_id)\
        .order_by(SensorReading.timestamp.desc()).limit(limit).all()
