from typing import List, Tuple
from ..database import add_audit_log
from ..models import EventIn
from .storage import save_event


def ingest_event(event: EventIn) -> dict:
    saved = save_event(event)
    add_audit_log("INGEST_EVENT", f"{saved['source_type']}:{saved['event_id']}")
    return saved


def ingest_events(events: List[EventIn]) -> Tuple[int, int]:
    ingested = 0
    rejected = 0

    for event in events:
        try:
            ingest_event(event)
            ingested += 1
        except Exception:
            rejected += 1

    return ingested, rejected
