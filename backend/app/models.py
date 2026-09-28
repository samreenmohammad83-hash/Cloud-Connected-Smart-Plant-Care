from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from .database import Base

class Device(Base):
    __tablename__ = "devices"
    device_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=True)
    plant_name = Column(String, nullable=False)
    plant_type = Column(String, nullable=False)
    location = Column(String, default="Virtual Lab")
    moisture_threshold = Column(Float, default=30)
    auto_water = Column(Boolean, default=True)
    last_seen = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    reading_id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"), index=True)
    soil_moisture = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    light_level = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

class WateringEvent(Base):
    __tablename__ = "watering_events"
    event_id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    trigger_type = Column(String)
    moisture_before = Column(Float)
    moisture_after = Column(Float, nullable=True)
    duration = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    alert_id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    alert_type = Column(String)
    level = Column(String)
    message = Column(String)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)
