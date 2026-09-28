# Interview Preparation — 10 Questions and Answers

## 1. Explain your project.
I built a Cloud-Connected Smart Plant Care and Watering System. A Python simulator behaves like an IoT device and sends soil moisture, temperature, humidity and light data to a FastAPI REST API. The backend stores the readings, checks plant-specific moisture thresholds, generates alerts and creates virtual watering events. A React dashboard shows current and historical data. The design can later connect an ESP32 and a managed cloud database.

## 2. Why did you use a simulator instead of hardware?
I wanted the project to be completely reproducible without depending on ESP32 boards or sensors. The simulator produces realistic gradual trends, so I can test the same cloud workflow. The API contract is designed so an ESP32 can replace the simulator later.

## 3. How does IoT-to-cloud communication work?
The simulator sends a JSON sensor payload over HTTP to `/api/sensors/data` with a device API key. The backend validates the payload, stores it and runs the automation logic. In a production IoT architecture I would consider MQTT through an IoT broker.

## 4. How does automatic watering work?
Each device has a configurable moisture threshold. If moisture falls below that threshold and automatic watering is enabled and the cooldown has completed, the automation engine creates a watering event. A maximum duration protects against continuous activation.

## 5. Why is a cloud database useful?
It centralizes historical sensor data so users can monitor plants remotely and analyze trends. SQLite is convenient for local development, while the same SQLAlchemy application can use PostgreSQL in a cloud deployment.

## 6. How did you handle security?
The demo uses a device API key stored through environment configuration instead of hardcoding a secret in source code. The API validates sensor ranges. For production I would use HTTPS, unique device credentials/certificates, secret management, authorization and rate limiting.

## 7. How would the system scale to thousands of plants?
I would separate ingestion from processing using an IoT broker/API gateway and queue or event stream. Serverless workers or autoscaling services can process events, while a managed time-series/database layer stores telemetry. Caching and retention policies can reduce database load.

## 8. What happens if the API is unavailable?
The simulator catches request errors, logs them and tries again on the next cycle. A production device should buffer readings locally and retry with exponential backoff. Monitoring should alert operators when the service is unhealthy.

## 9. How do you detect an offline device?
Every accepted reading updates `last_seen`. A periodic job compares the current time with `last_seen`. If the heartbeat is older than the configured interval, the device is marked offline and an alert is generated.

## 10. How would you deploy it?
I would deploy the React frontend as a static application, FastAPI as a managed web service/container, and PostgreSQL as a managed database. Environment variables would hold service URLs and secrets. GitHub Actions could run tests and deploy on approved pushes.
