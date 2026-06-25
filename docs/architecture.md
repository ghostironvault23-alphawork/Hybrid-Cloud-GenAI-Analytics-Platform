# Architecture Guide

## Goal

Build a hybrid cloud GenAI analytics platform that ingests enterprise data from public cloud systems, IoT devices, on-prem applications, and business workflows. The platform validates and masks the data, stores it in a data lake, retrieves relevant context, and generates AI-based business insights.

## End-to-End Flow

```text
Users / IoT / On-Prem / Public Cloud
        ↓
FastAPI Backend API
        ↓
Validation + Masking + Role Check
        ↓
Local Data Lake + Transaction Database
        ↓
RAG-Style Retrieval
        ↓
Mock GenAI Analyst / Amazon Bedrock
        ↓
Root Cause Analysis / Reports / Dashboards / Alerts
```

## Main Components

| Component | Local MVP | Production Cloud Mapping |
|---|---|---|
| API Layer | FastAPI | API Gateway + Lambda, ECS, or App Service |
| Data Lake | JSONL files | Amazon S3 or Azure Data Lake Storage Gen2 |
| Transaction DB | SQLite | DynamoDB, RDS, Cosmos DB, or Azure SQL |
| AI Layer | Mock GenAI service | Amazon Bedrock or Azure OpenAI |
| Retrieval | Keyword scoring | OpenSearch, Bedrock Knowledge Base, or Azure AI Search |
| Monitoring | Local logs | CloudWatch or Application Insights |
| Security | API key + RBAC | Cognito, IAM, KMS, WAF, CloudTrail |

## Why the Middle Layer Matters

The middle layer prevents raw and sensitive data from going directly to the AI model. It performs validation, PII masking, role checking, event normalization, audit logging, and routing.

## Security Controls

- role-based access control
- PII masking before storage
- audit logging for ingested events
- API key protection for local demo
- production-ready design for IAM, KMS, Cognito, CloudTrail, and WAF

## Business Value

The system reduces manual log analysis, improves incident response, supports faster reporting, and converts scattered enterprise data into clear business insights.
