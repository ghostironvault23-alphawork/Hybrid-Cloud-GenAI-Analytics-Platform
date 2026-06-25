# API Guide

Base URL for local demo:

```text
http://localhost:8000
```

## Health Check

```http
GET /health
```

Returns service status and timestamp.

## Ingest One Event

```http
POST /ingest/event
```

Example body:

```json
{
  "source_type": "cloud_log",
  "source_name": "aws-cloudwatch-payment-service",
  "event_id": "cloud-100",
  "timestamp": "2026-05-26T09:10:00Z",
  "severity": "error",
  "message": "Payment service returned HTTP 503.",
  "attributes": {
    "service": "payment-api"
  }
}
```

## Ingest Batch Events

```http
POST /ingest/batch
```

Body:

```json
{
  "events": [
    {
      "source_type": "iot_telemetry",
      "source_name": "factory-sensor-cluster",
      "event_id": "iot-100",
      "timestamp": "2026-05-26T09:12:00Z",
      "severity": "critical",
      "message": "Temperature threshold breached.",
      "attributes": {
        "device_id": "sensor-101"
      }
    }
  ]
}
```

## Ask AI

```http
POST /ask-ai
```

Example:

```json
{
  "question": "Why did payment service fail?",
  "user_id": "demo-user",
  "role": "Engineer",
  "max_context_events": 5
}
```

## Search Events

```http
GET /events/search?q=payment&limit=5
```

## Summary Report

```http
GET /reports/summary
```

Returns event counts by source and severity.
