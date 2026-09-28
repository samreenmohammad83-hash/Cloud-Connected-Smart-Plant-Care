# Cloud-Connected Smart Plant Care & Watering System — Project Report

## Abstract
This project presents a cloud-connected plant monitoring and watering platform using synthetic IoT sensor data. A Python simulator behaves like a virtual device and sends soil moisture, temperature, humidity and light readings to a FastAPI backend. Readings are stored in a database and evaluated by an automation engine. When moisture falls below a configurable threshold, the system can create a virtual watering event. A React dashboard provides remote monitoring, historical charts, alerts and controls.

## Introduction
Plant watering is often based on fixed schedules rather than actual plant conditions. The proposed system demonstrates how IoT sensing, cloud APIs, databases and automation can be combined to make watering condition-driven. Physical hardware is optional; simulated data makes the complete workflow reproducible on a student laptop.

## Problem Statement
Manual monitoring can miss changes in soil moisture and may result in under-watering or over-watering. A connected platform can centralize sensor data and automate decisions.

## Objectives
1. Simulate IoT sensor readings.
2. Transfer readings through a REST API.
3. Store historical readings.
4. Apply configurable watering rules.
5. Generate alerts.
6. Provide remote dashboard monitoring.
7. Demonstrate cloud deployment and scalability concepts.
8. Apply basic API security and testing.

## Existing System
Traditional plant care often depends on manual observation or timers. These approaches have limited remote visibility and do not use current sensor measurements.

## Proposed System
The proposed architecture connects a virtual sensor or ESP32 to an API layer. The backend stores readings, evaluates automation rules and exposes data to a dashboard. A real deployment can replace the local database with a managed PostgreSQL/time-series service and REST with MQTT where appropriate.

## Industry Relevance
The same architecture is applicable to smart agriculture, precision farming, greenhouses, nurseries, vertical farms, hydroponics, landscaping and environmental monitoring.

## Cloud Computing Concepts
Cloud computing is represented through hosted application services, managed databases, APIs, serverless/event-driven alternatives, centralized monitoring, environment configuration, scalability and CI/CD.

## IoT Concepts
The project models a device identity, sensor payload, heartbeat/last-seen timestamp, command path and actuator event. The simulator can later be replaced by an ESP32 without changing the main backend contract.

## Technology Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite locally / PostgreSQL-ready
- React
- Vite
- Recharts
- HTTP/REST
- pytest

## Architecture
Virtual Sensor/ESP32 -> HTTPS/MQTT -> API Layer -> Cloud Backend -> Database + Automation -> Virtual/Real Pump -> Dashboard + Alerts.

## Sensor Simulation
The simulator generates bounded values and gradual trends. Soil moisture decreases over time; temperature and humidity vary gradually; light follows a simple periodic pattern. When the API reports watering, the simulator increases virtual moisture.

## Database Design
The core entities are Devices, SensorReadings, WateringEvents and Alerts. Devices identify plants and store thresholds. SensorReadings provide historical telemetry. WateringEvents record automatic/manual actions. Alerts provide operational visibility.

## REST API
The API supports device registration, sensor ingestion, latest readings, historical readings, threshold updates, auto-water configuration, manual watering, watering history and alert management.

## Watering Algorithm
If soil moisture is below the configured threshold, automatic watering is eligible. The engine also checks the auto-water flag and a cooldown interval. Maximum watering duration prevents unbounded activation.

## Dashboard
The dashboard displays current telemetry, plant status, historical soil moisture, threshold controls, automatic watering state, manual watering and alerts.

## Alerts
The system creates low-moisture and high-temperature alerts. A production deployment can add low-tank and offline-device alerts and route them to email/SMS/push providers.

## Device Monitoring
Every accepted sensor reading updates `last_seen`. A periodic cloud job can mark a device offline when its heartbeat becomes stale.

## Cloud Deployment
A student deployment can use a PaaS backend, static frontend hosting and managed PostgreSQL. An enterprise architecture can use AWS IoT Core, API Gateway, Lambda, DynamoDB/Timestream, SNS, S3 and CloudWatch or equivalent Azure/GCP services.

## Testing
Tests verify API health, valid ingestion, validation failures and unauthorized device requests. Additional manual test cases should cover watering thresholds, cooldown, dashboard updates and failure handling.

## Security
Device ingestion is protected by an API key in the demo. Production should use HTTPS, unique device credentials/certificates, secrets management, least-privilege database permissions, authorization, validation, rate limiting and monitoring.

## Scalability
At small scale, one API and database are sufficient. At larger scale, an IoT broker, API gateway, serverless workers, queues, autoscaling, time-series storage, caching and retention policies can distribute the workload.

## Analytics
Useful metrics include average/minimum/maximum soil moisture, average temperature/humidity, watering frequency, plant health status and device uptime. Water consumption can be estimated when pump flow rate and duration are measured.

## Failure Handling
The simulator retries on later cycles after an API failure. Validation rejects invalid sensor ranges. Authentication rejects invalid device keys. Production systems should add local buffering, idempotency keys, queues and stronger observability.

## Results
The virtual system demonstrates an end-to-end IoT-to-cloud workflow without physical hardware. A dry-soil condition can trigger a virtual watering event, after which the simulated moisture rises and the dashboard reflects the new state.

## Advantages
- No hardware required for demonstration
- Clear cloud/IoT separation
- Configurable plant rules
- Historical data
- Remote dashboard
- Testable REST API
- PostgreSQL-ready architecture

## Limitations
The simulator is synthetic and does not model real sensor calibration, soil types, flow rates or weather. Hardware safety requires a separate real-device validation phase.

## Future Scope
MQTT, cloud-native serverless processing, ML forecasting, real notifications, device certificates, role-based access, Terraform, containers, CI/CD and real hardware can be added.

## Conclusion
The project demonstrates how cloud computing can turn sensor telemetry into a remotely monitored and automated plant-care service. The virtual simulator makes the system reproducible for a student while preserving an architecture that can later connect to physical IoT hardware.
