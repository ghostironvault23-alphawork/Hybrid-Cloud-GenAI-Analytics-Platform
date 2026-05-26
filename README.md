# Enterprise GenAI Data Platform

**Hybrid Cloud AI Analytics with Data Lake, RAG, IoT, On-Prem Integration, and Business Intelligence**

This project is a recruiter-ready GitHub showcase for an enterprise GenAI architecture. It demonstrates how users, IoT devices, public cloud systems, and on-prem systems can send data into a secure middle layer, store it in a data lake or transaction database, and use a GenAI/RAG-style workflow to produce business outputs like summaries, root cause analysis, alerts, and reports.

> Local MVP runs without AWS or paid AI APIs. The AI response is deterministic and mock-based by default, so you can demo the full flow safely. Optional Amazon Bedrock integration can be added later.

---

## Key Features

- Secure API backend using FastAPI
- Local RAG-style retrieval over uploaded enterprise events
- Mock GenAI analyst for offline demo
- Optional Amazon Bedrock-ready service layer
- Data ingestion for:
  - cloud logs
  - IoT telemetry
  - on-prem tickets
  - business events
- Local file-based data lake simulation
- SQLite transaction database for requests and responses
- Static frontend demo UI
- Dockerfile and Docker Compose
- AWS SAM and Terraform starter infrastructure
- CI workflow for syntax checks and tests
- Recruiter explanation docs and interview Q&A

---

## Architecture Summary

```text
Users / IoT / On-Prem / Public Cloud
        ↓
API Gateway / Backend API
        ↓
Validation + Processing + Masking
        ↓
Data Lake + Transaction DB
        ↓
RAG Retrieval + AI Layer
        ↓
Reports / Summaries / Root Cause / Business Insights
```

---

## Repository Structure

```text
enterprise-genai-data-platform/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── security.py
│   │   ├── lambda_handler.py
│   │   ├── services/
│   │   └── utils/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── data/
│   └── sample/
├── docs/
├── infrastructure/
│   ├── aws-sam/
│   └── terraform/
├── scripts/
├── .github/workflows/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Quick Start: Local Demo

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/enterprise-genai-data-platform.git
cd enterprise-genai-data-platform
```

### 2. Create Python environment

```bash
cd backend
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start backend

```bash
uvicorn app.main:app --reload --port 8000
```

Backend will run at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### 5. Seed sample data

Open a second terminal from the project root:

```bash
python scripts/seed_data.py
```

### 6. Open frontend

Open this file in your browser:

```text
frontend/index.html
```

Ask:

```text
Why did payment service fail?
```

or

```text
Show IoT anomalies
```

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check backend status |
| POST | `/ingest/event` | Ingest one event |
| POST | `/ingest/batch` | Ingest multiple events |
| POST | `/ask-ai` | Ask AI analyst a question |
| GET | `/reports/summary` | Get platform summary |
| GET | `/events/search` | Search local data lake events |

---

## Example Request

```bash
curl -X POST http://localhost:8000/ask-ai \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Why did payment service fail?\",\"user_id\":\"demo-user\",\"role\":\"Engineer\"}"
```

---

## Recruiter Pitch

“I built a hybrid enterprise GenAI data platform that ingests data from on-prem systems, IoT devices, and public cloud logs. The middle layer validates, masks, and stores the data in a data lake and transaction database. Then a RAG-style AI layer retrieves relevant context and generates business outputs like summaries, root cause analysis, alerts, and reports. The MVP runs locally using FastAPI, SQLite, and a mock GenAI service, and it is designed to scale on AWS using S3, Lambda, API Gateway, DynamoDB, Bedrock, Glue, Athena, QuickSight, IAM, and CloudWatch.”

---

## AWS Mapping

| Local MVP | AWS Production Equivalent |
|---|---|
| FastAPI | Lambda/ECS/EKS |
| Local files | S3 Data Lake |
| SQLite | DynamoDB/RDS |
| Mock AI service | Amazon Bedrock |
| Static frontend | S3 + CloudFront / Amplify |
| Local logs | CloudWatch |
| Local scripts | Glue / Step Functions |
| Manual auth header | Cognito + JWT |
| Local search | Bedrock Knowledge Base / OpenSearch |

---

## Future Improvements

- Add Cognito authentication
- Add Amazon Bedrock Knowledge Base
- Add OpenSearch vector database
- Add real IoT Core ingestion
- Add QuickSight dashboards
- Add CI/CD deployment pipeline
- Add PII detection and advanced data masking
- Add multi-cloud connectors for Azure and GCP

---

## License

MIT License


## Reference Architecture Diagram

![Architecture Reference](docs/images/architecture-reference.png)
