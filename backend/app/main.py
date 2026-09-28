from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import devices, sensors, watering, alerts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cloud Smart Plant Care API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)
app.include_router(devices.router, prefix="/api")
app.include_router(sensors.router, prefix="/api")
app.include_router(watering.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")

@app.get("/")
def root():
    return {"service": "Cloud-Connected Smart Plant Care", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
