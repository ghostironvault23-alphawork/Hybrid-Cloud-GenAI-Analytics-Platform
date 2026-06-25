from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SourceType(str, Enum):
    cloud_log = "cloud_log"
    iot_telemetry = "iot_telemetry"
    onprem_ticket = "onprem_ticket"
    business_event = "business_event"


class UserRole(str, Enum):
    admin = "Admin"
    analyst = "Analyst"
    engineer = "Engineer"
    viewer = "Viewer"


class EventIn(BaseModel):
    source_type: SourceType
    source_name: str = Field(..., min_length=2, max_length=120)
    event_id: str = Field(..., min_length=3, max_length=120)
    timestamp: datetime
    severity: str = Field(default="info", max_length=40)
    message: str = Field(..., min_length=3, max_length=4000)
    attributes: Dict[str, Any] = Field(default_factory=dict)


class BatchEventsIn(BaseModel):
    events: List[EventIn]


class AskAIRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=1000)
    user_id: str = Field(default="demo-user", max_length=120)
    role: UserRole = Field(default=UserRole.viewer)
    max_context_events: int = Field(default=5, ge=1, le=20)


class AIAnswer(BaseModel):
    request_id: str
    question: str
    answer: str
    confidence: str
    retrieved_events: List[Dict[str, Any]]
    created_at: datetime


class IngestResponse(BaseModel):
    status: str
    ingested_count: int
    rejected_count: int = 0
    details: Optional[str] = None


class SummaryReport(BaseModel):
    total_events: int
    events_by_source: Dict[str, int]
    events_by_severity: Dict[str, int]
    latest_events: List[Dict[str, Any]]
