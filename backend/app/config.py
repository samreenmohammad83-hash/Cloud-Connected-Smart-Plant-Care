import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./plantcare.db")
DEVICE_API_KEY = os.getenv("DEVICE_API_KEY", "demo-device-key")
OFFLINE_AFTER_SECONDS = int(os.getenv("OFFLINE_AFTER_SECONDS", "30"))
DEFAULT_THRESHOLD = float(os.getenv("DEFAULT_THRESHOLD", "30"))
MAX_WATERING_SECONDS = int(os.getenv("MAX_WATERING_SECONDS", "8"))
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", "20"))
HIGH_TEMP_THRESHOLD = float(os.getenv("HIGH_TEMP_THRESHOLD", "38"))
