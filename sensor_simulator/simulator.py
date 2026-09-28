import math, random, time, logging
from datetime import datetime, timezone
import httpx
from config import API_URL, DEVICE_ID, INTERVAL, API_KEY, OFFLINE_MODE

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

soil, temp, humidity = 55.0, 28.0, 62.0
tick = 0

def next_reading():
    global soil, temp, humidity, tick
    tick += 1
    # Gradual drying plus small environmental variation.
    soil = max(8, soil - random.uniform(0.8, 2.2))
    temp += random.uniform(-0.5, 0.5)
    humidity += random.uniform(-1.5, 1.5)
    temp = min(40, max(15, temp))
    humidity = min(90, max(30, humidity))
    light = max(0, min(100, 50 + 45 * math.sin(tick / 12) + random.uniform(-5, 5)))
    return {
        "device_id": DEVICE_ID,
        "soil_moisture": round(soil, 2),
        "temperature": round(temp, 2),
        "humidity": round(humidity, 2),
        "light_level": round(light, 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def send(data):
    if OFFLINE_MODE:
        logging.info("OFFLINE MODE | %s", data)
        return
    try:
        r = httpx.post(f"{API_URL}/api/sensors/data", json=data,
                       headers={"X-Device-Key": API_KEY}, timeout=5)
        r.raise_for_status()
        result = r.json()
        if result.get("watering_triggered"):
            # Simulate the pump physically changing soil moisture.
            global soil
            soil = min(100, soil + 14)
            logging.info("VIRTUAL PUMP ON | moisture boosted to %.1f%%", soil)
        logging.info("Sent reading | moisture=%.1f%% temp=%.1f°C", soil, temp)
    except Exception as exc:
        logging.error("API error: %s | reading retained for retry on next cycle", exc)

if __name__ == "__main__":
    logging.info("Starting virtual IoT sensor %s", DEVICE_ID)
    while True:
        send(next_reading())
        time.sleep(INTERVAL)
