from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Alert

router = APIRouter()

@router.get("/alerts")
def get_alerts(device_id: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Alert).order_by(Alert.created_at.desc())
    if device_id: q = q.filter_by(device_id=device_id)
    return q.limit(100).all()

@router.put("/alerts/{alert_id}/acknowledge")
def acknowledge(alert_id: int, db: Session = Depends(get_db)):
    a = db.get(Alert, alert_id)
    if not a: raise HTTPException(404, "Alert not found")
    a.status = "ACKNOWLEDGED"
    db.commit()
    return a
