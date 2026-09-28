import os
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
DEVICE_ID = os.getenv("DEVICE_ID", "PLANT-001")
INTERVAL = float(os.getenv("INTERVAL", "3"))
API_KEY = os.getenv("DEVICE_API_KEY", "demo-device-key")
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "false").lower() == "true"
