import os, tempfile
os.environ["DATABASE_URL"] = "sqlite:///./test_plantcare.db"
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal
from backend.app.models import Device

client = TestClient(app)

def setup_device():
    db=SessionLocal()
    if not db.get(Device,"PLANT-001"):
        db.add(Device(device_id="PLANT-001", plant_name="Tomato Plant",
                      plant_type="TOMATO", location="Virtual Lab", moisture_threshold=30))
        db.commit()
    db.close()

def test_health():
    assert client.get("/health").status_code == 200

def test_device_and_sensor():
    setup_device()
    r=client.post("/api/sensors/data",
        json={"device_id":"PLANT-001","soil_moisture":55,"temperature":28,
              "humidity":60,"light_level":70},
        headers={"X-Device-Key":"demo-device-key"})
    assert r.status_code == 200
    assert client.get("/api/devices/PLANT-001/latest").status_code == 200

def test_invalid_sensor_rejected():
    setup_device()
    r=client.post("/api/sensors/data",
        json={"device_id":"PLANT-001","soil_moisture":150,"temperature":28,
              "humidity":60,"light_level":70},
        headers={"X-Device-Key":"demo-device-key"})
    assert r.status_code == 422

def test_unauthorized_sensor_rejected():
    setup_device()
    r=client.post("/api/sensors/data",
        json={"device_id":"PLANT-001","soil_moisture":40,"temperature":28,
              "humidity":60,"light_level":70},
        headers={"X-Device-Key":"wrong"})
    assert r.status_code == 401
