# Cloud-Connected Smart Plant Care & Watering System

A beginner-friendly, industry-oriented Cloud Computing + IoT project that uses a Python virtual sensor instead of physical hardware. It stores sensor readings, evaluates watering rules, creates alerts, and exposes a web dashboard.

## Why this project
The system demonstrates cloud/IoT concepts without requiring an ESP32, sensor, relay, or pump. A simulator behaves like an IoT device and sends synthetic readings to the REST API.

## Architecture

Virtual Sensor / ESP32
-> HTTPS REST API
-> FastAPI backend
-> SQL database
-> Automation engine
-> Virtual watering event
-> React dashboard + alerts

For production, the database can be switched from SQLite to PostgreSQL using `DATABASE_URL`.

## Features
- Simulated soil moisture, temperature, humidity and light
- Gradual sensor trends instead of pure random values
- REST API
- SQLite local database / PostgreSQL-ready configuration
- Plant-specific thresholds
- Automatic watering decision
- Manual watering
- Cooldown and maximum watering duration
- Alerts
- Device last-seen timestamp
- Historical readings
- React dashboard and chart
- API-key authentication for device ingestion
- Automated backend tests
- Cloud-deployment-ready environment variables

## Plant profiles
- SUCCULENT: 20%
- TOMATO: 40%
- HERB: 35%
- INDOOR_PLANT: 30%

The demo device can be configured to 30% to reproduce the assignment's 29% trigger example.

## Local installation

### 1. Backend
PowerShell:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Create the demo device:
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/devices -Method POST -ContentType "application/json" -Body '{"device_id":"PLANT-001","plant_name":"Tomato Plant","plant_type":"INDOOR_PLANT","location":"Virtual Lab","moisture_threshold":30}'
```

### 2. Frontend
Open another PowerShell:
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL shown in the terminal.

### 3. Sensor simulator
Open another PowerShell:
```powershell
cd sensor_simulator
python -m pip install httpx
python simulator.py
```

The simulator sends readings every 3 seconds. Moisture gradually decreases. When it crosses the threshold, the backend can create an automatic watering event and the simulator increases its virtual moisture value.

## API endpoints
- POST `/api/sensors/data`
- GET `/api/devices`
- POST `/api/devices`
- GET `/api/devices/{id}`
- GET `/api/devices/{id}/latest`
- GET `/api/devices/{id}/history`
- PUT `/api/devices/{id}/threshold`
- PUT `/api/devices/{id}/auto-water`
- POST `/api/devices/{id}/water`
- GET `/api/devices/{id}/watering-history`
- GET `/api/alerts`
- GET `/api/devices/{id}/status`
- PUT `/api/alerts/{id}/acknowledge`

Swagger API documentation is available at `/docs`.

## Cloud Computing mapping
- **SaaS:** the completed dashboard/application consumed by a user.
- **PaaS:** a managed application host can run the FastAPI service.
- **IaaS:** a VM/container host can run the same services.
- **Cloud database:** PostgreSQL or another managed database can replace SQLite.
- **REST API:** HTTPS ingestion and dashboard APIs.
- **MQTT:** recommended for a production IoT broker; the simulator currently uses REST for simplicity.
- **Serverless:** the automation logic can be moved to Lambda/Azure Functions/Cloud Functions.
- **Event-driven:** a sensor event can trigger a function and database write.
- **Scalability:** managed database, broker, queues and autoscaling can support many devices.
- **Secrets:** `.env` values are kept out of Git.
- **Logging/monitoring:** application logs plus cloud monitoring in deployment.
- **CI/CD:** GitHub Actions can run tests and deploy after push.

## Authentication scope
The implemented authentication is device-level API-key authentication for telemetry ingestion. Full user login/registration is intentionally kept outside this compact student MVP; a production version can add Firebase Auth/Supabase Auth/JWT plus role-based authorization for dashboard users.

## Security
The demo protects device ingestion with `X-Device-Key`. In production, use per-device credentials/certificates, HTTPS, secret management, authorization, rate limiting, database least privilege and audit logs. Never expose an unauthenticated pump-control endpoint publicly.

## Offline detection
Each accepted reading updates `last_seen`. A production scheduler should periodically compare the current time with `last_seen`; if the difference exceeds the configured heartbeat interval, create a DEVICE_OFFLINE alert.

## Failure handling
- API timeout -> simulator logs the error and tries again next cycle.
- Invalid values -> FastAPI/Pydantic rejects the request.
- Wrong device key -> 401.
- Unknown device -> 404.
- Database outage -> service should report an error and cloud monitoring should alert.
- Duplicate messages -> production version should add a device message ID/idempotency key.
- Internet outage -> a production simulator/device should buffer readings locally before retrying.

## Optional ESP32 version
Replace `sensor_simulator/simulator.py` with ESP32 firmware that reads:
- capacitive soil moisture sensor
- DHT11/DHT22
- optional LDR
and sends JSON over HTTPS or MQTT.

Conceptual wiring:
- Sensor VCC -> suitable low-voltage supply
- Sensor GND -> ESP32 GND
- Analog moisture output -> ESP32 ADC pin
- DHT data -> GPIO
- Relay control -> GPIO
- Pump must use a separate appropriate low-voltage power supply and safe switching circuit.

Do not connect a mains-powered pump directly to an ESP32. Use an appropriately rated relay/MOSFET and safe low-voltage setup.

## Cloud deployment options

### Student-friendly
- Frontend: Vercel/Netlify/static hosting
- Backend: Render/Railway/Fly.io or another student-friendly container/PaaS provider
- Database: Supabase/Neon/PostgreSQL provider
- Set `VITE_API_URL` on the frontend and `DATABASE_URL`, `DEVICE_API_KEY` on the backend.

Free tiers change over time, so verify current limits before deployment.

### AWS-style enterprise architecture
ESP32/Simulator -> AWS IoT Core or HTTPS -> API Gateway -> Lambda -> DynamoDB/Timestream -> SNS -> Dashboard. Static frontend assets can use S3 + CloudFront and monitoring can use CloudWatch.

Azure equivalents: IoT Hub, API Management, Azure Functions, Cosmos DB/Time Series Insights-compatible services, Notification Hubs/Communication Services, Static Web Apps, Azure Monitor.

GCP equivalents: Pub/Sub or IoT-compatible gateway architecture, API Gateway, Cloud Run/Cloud Functions, Firestore/BigQuery/managed SQL, Cloud Monitoring and static hosting.

## Testing
Run:
```powershell
pip install -r backend/requirements.txt
pytest -q
```
The included tests cover health, sensor ingestion, validation and unauthorized access.

## GitHub strategy
Recommended repository name:
`Cloud-Connected-Smart-Plant-Care`

Suggested topics:
`cloud-computing`, `iot`, `smart-agriculture`, `python`, `fastapi`, `react`, `cloud-database`, `rest-api`, `automation`, `smart-irrigation`, `sensor-data`, `cloud-monitoring`

Suggested commits:
1. Initialize smart plant cloud project
2. Add virtual IoT sensor simulator
3. Implement sensor REST API
4. Integrate cloud database
5. Add automated watering engine
6. Implement plant-specific thresholds
7. Add watering event tracking
8. Build monitoring dashboard
9. Implement alert system
10. Add device offline detection
11. Add historical analytics
12. Add automated tests
13. Deploy application to cloud
14. Complete README and documentation

## Screenshots to capture
1. Folder structure
2. Architecture diagram
3. Simulator terminal
4. API/Swagger page
5. Database rows
6. Dashboard
7. Moisture graph
8. Low-moisture alert
9. Auto-watering event
10. Manual watering
11. Threshold configuration
12. Tests passing
13. Cloud deployment
14. GitHub commits
15. README

## Limitations
This student edition uses a simulated device and virtual pump. Real plant calibration, sensor noise, irrigation volume and hardware safety require field testing. Email/SMS/push notifications are integration points rather than mandatory local components.

## Future improvements
- MQTT broker
- per-device certificates
- WebSockets
- real cloud time-series database
- email/SMS/push notifications
- weather-aware watering
- ML-based moisture forecasting
- role-based user management
- multi-tenant organizations
- IaC with Terraform
- GitHub Actions deployment
- containerization with Docker/Kubernetes for larger deployments

## Resume bullets
- Built a cloud-connected smart plant monitoring platform using FastAPI, React and a virtual IoT sensor simulator, with REST ingestion, historical storage and dashboard analytics.
- Implemented configurable plant-specific watering automation with threshold checks, cooldown protection, virtual pump events and low-moisture alerts.
- Designed a cloud-ready IoT architecture with device authentication, environment-based configuration, failure handling, automated tests and PostgreSQL-compatible persistence.

## Project description
Cloud-connected smart plant monitoring and watering platform featuring simulated IoT sensors, REST APIs, database-backed historical analytics, automated irrigation logic, alerts and scalable cloud architecture.
