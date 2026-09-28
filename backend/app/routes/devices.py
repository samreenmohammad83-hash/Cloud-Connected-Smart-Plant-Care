from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Device
from ..config import DEFAULT_THRESHOLD
from ..services.automation import plant_threshold

router = APIRouter()

class DeviceCreate(BaseModel):
    device_id: str
    plant_name: str
    plant_type: str = "INDOOR_PLANT"
    location: str = "Virtual Lab"
    moisture_threshold: float | None = Field(default=None, ge=0, le=100)

class ThresholdUpdate(BaseModel):
    moisture_threshold: float = Field(ge=0, le=100)

class AutoWaterUpdate(BaseModel):
    auto_water: bool

@router.get("/devices")
def list_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()

@router.post("/devices", status_code=201)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db)):
    if db.get(Device, payload.device_id):
        raise HTTPException(409, "Device already exists")
    threshold = payload.moisture_threshold
    if threshold is None:
        threshold = plant_threshold(payload.plant_type)
    d = Device(device_id=payload.device_id, plant_name=payload.plant_name,
               plant_type=payload.plant_type.upper(), location=payload.location,
               moisture_threshold=threshold)
    db.add(d); db.commit(); db.refresh(d)
    return d

@router.get("/devices/{device_id}")
def get_device(device_id: str, db: Session = Depends(get_db)):
    d = db.get(Device, device_id)
    if not d: raise HTTPException(404, "Device not found")
    return d

@router.put("/devices/{device_id}/threshold")
def update_threshold(device_id: str, payload: ThresholdUpdate, db: Session = Depends(get_db)):
    d = db.get(Device, device_id)
    if not d: raise HTTPException(404, "Device not found")
    d.moisture_threshold = payload.moisture_threshold
    db.commit(); db.refresh(d)
    return d

@router.put("/devices/{device_id}/auto-water")
def update_auto_water(device_id: str, payload: AutoWaterUpdate, db: Session = Depends(get_db)):
    d = db.get(Device, device_id)
    if not d: raise HTTPException(404, "Device not found")
    d.auto_water = payload.auto_water
    db.commit(); db.refresh(d)
    return d


@router.get("/devices/{device_id}/status")
def device_status(device_id: str, db: Session = Depends(get_db)):
    from datetime import datetime
    from ..config import OFFLINE_AFTER_SECONDS
    d = db.get(Device, device_id)
    if not d: raise HTTPException(404, "Device not found")
    if not d.last_seen:
        return {"device_id": device_id, "status": "OFFLINE", "last_seen": None}
    age = (datetime.utcnow() - d.last_seen).total_seconds()
    status = "ONLINE" if age <= OFFLINE_AFTER_SECONDS else "OFFLINE"
    return {"device_id": device_id, "status": status, "last_seen": d.last_seen, "age_seconds": round(age, 1)}
