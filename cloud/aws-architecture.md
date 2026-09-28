# AWS-Style Enterprise Architecture

ESP32 / Python Simulator
-> AWS IoT Core or HTTPS API
-> API Gateway
-> Lambda
-> DynamoDB or Amazon Timestream
-> SNS notifications
-> React dashboard

Static frontend:
S3 + CloudFront

Monitoring:
CloudWatch

Security:
IAM least privilege, Secrets Manager, TLS, IoT device certificates.

For high volume, add SQS/Kinesis between ingestion and processing. Use retention policies for telemetry and alarms for ingestion latency, function errors and device offline counts.
