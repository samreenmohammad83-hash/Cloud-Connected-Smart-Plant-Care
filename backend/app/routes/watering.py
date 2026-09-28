from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Device, WateringEvent

router = APIRouter()

class WaterRequest(BaseModel):
    duration: float = Field(default=5, ge=1, le=8)

@router.post("/devices/{device_id}/water")
def manual_water(device_id: str, payload: WaterRequest, db: Session = Depends(get_db)):
    d = db.get(Device, device_id)
    if not d: raise HTTPException(404, "Device not found")
    last = db.query(WateringEvent).filter_by(device_id=device_id).order_by(WateringEvent.timestamp.desc()).first()
    moisture = None
    if last and last.moisture_after is not None:
        moisture = last.moisture_after
    event = WateringEvent(device_id=device_id, trigger_type="MANUAL",
                          moisture_before=moisture or 0, duration=payload.duration)
    db.add(event); db.commit(); db.refresh(event)
    return {"message": "virtual pump activated", "event_id": event.event_id, "duration": payload.duration}

@router.get("/devices/{device_id}/watering-history")
def watering_history(device_id: str, db: Session = Depends(get_db)):
    return db.query(WateringEvent).filter_by(device_id=device_id)\
        .order_by(WateringEvent.timestamp.desc()).limit(100).all()
