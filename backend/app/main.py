from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db, save_ai_request
from .models import AIAnswer, AskAIRequest, BatchEventsIn, EventIn, IngestResponse, SummaryReport
from .security import ensure_role_can_access_ai, require_api_key
from .services.ai_service import generate_answer
from .services.analytics import build_summary_report
from .services.ingestion import ingest_event, ingest_events
from .services.retrieval import retrieve_context
from .services.storage import search_events


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Hybrid Cloud GenAI Analytics Platform API",
    description="Hybrid cloud GenAI data platform MVP with local RAG-style workflow.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "hybrid-cloud-genai-analytics-platform",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/ingest/event", response_model=IngestResponse, dependencies=[Depends(require_api_key)])
def ingest_single_event(event: EventIn) -> IngestResponse:
    ingest_event(event)
    return IngestResponse(status="success", ingested_count=1)


@app.post("/ingest/batch", response_model=IngestResponse, dependencies=[Depends(require_api_key)])
def ingest_batch(payload: BatchEventsIn) -> IngestResponse:
    ingested, rejected = ingest_events(payload.events)
    return IngestResponse(
        status="success" if rejected == 0 else "partial_success",
        ingested_count=ingested,
        rejected_count=rejected,
    )


@app.post("/ask-ai", response_model=AIAnswer, dependencies=[Depends(require_api_key)])
def ask_ai(payload: AskAIRequest) -> AIAnswer:
    ensure_role_can_access_ai(payload.role)

    context_events = retrieve_context(payload.question, max_events=payload.max_context_events)
    answer, confidence = generate_answer(payload.question, context_events)
    request_id = str(uuid4())

    save_ai_request(
        request_id=request_id,
        user_id=payload.user_id,
        role=payload.role.value,
        question=payload.question,
        answer=answer,
        confidence=confidence,
    )

    return AIAnswer(
        request_id=request_id,
        question=payload.question,
        answer=answer,
        confidence=confidence,
        retrieved_events=context_events,
        created_at=datetime.now(timezone.utc),
    )


@app.get("/events/search", dependencies=[Depends(require_api_key)])
def search_data_lake_events(
    q: str = Query(default="", description="Search query"),
    limit: int = Query(default=10, ge=1, le=50),
) -> List[dict]:
    return search_events(q, limit=limit)


@app.get("/reports/summary", response_model=SummaryReport, dependencies=[Depends(require_api_key)])
def summary_report() -> SummaryReport:
    return build_summary_report()
