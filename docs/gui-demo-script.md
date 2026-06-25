# Recruiter GUI Demo Script

Use this script when explaining the project in an interview or portfolio walkthrough.

## 1. Show the Architecture

Say:

> This is a hybrid cloud GenAI analytics platform. It collects data from cloud logs, IoT devices, and on-prem systems. The middle layer validates, masks, and stores the data. The AI layer retrieves relevant context and produces root cause analysis, summaries, reports, and recommendations.

## 2. Show the GitHub Structure

Point to:

- `backend/` for FastAPI backend
- `frontend/` for demo UI
- `data/sample/` for enterprise sample data
- `docs/` for architecture and interview preparation
- `infrastructure/` for AWS deployment starters
- `.github/workflows/ci.yml` for CI validation

Say:

> I kept the repo structured like a production project so recruiters can quickly understand the backend, frontend, data, infrastructure, and documentation layers.

## 3. Run Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Show:

```text
http://localhost:8000/docs
```

Say:

> This Swagger UI shows the backend APIs for ingestion, search, reports, and AI Q&A.

## 4. Seed Data

```bash
python scripts/seed_data.py
```

Say:

> This simulates enterprise data from cloud logs, IoT telemetry, and on-prem tickets.

## 5. Test AI Q&A

Ask:

```text
Why did payment service fail?
```

Say:

> The platform retrieves relevant enterprise context from the local data lake and generates a structured AI answer with summary, root cause, business impact, fix, and prevention steps.

## 6. Explain Cloud Mapping

Say:

> Locally, this uses FastAPI, SQLite, and JSONL data lake files. In production, this maps to API Gateway, Lambda, S3, DynamoDB, Bedrock, Glue, Athena, QuickSight, IAM, Cognito, and CloudWatch.

## 7. Strong Closing Pitch

> The main value is that this project combines cloud architecture, data engineering, security, RAG, AI analysis, and business reporting in one end-to-end system.
