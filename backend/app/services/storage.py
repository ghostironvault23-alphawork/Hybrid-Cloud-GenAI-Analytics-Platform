import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List
from ..config import get_settings
from ..models import EventIn
from ..utils.masking import mask_dict
from ..utils.validation import clean_message, normalize_severity


def _event_file_path(source_type: str) -> Path:
    settings = get_settings()
    folder = settings.data_path / "raw" / source_type
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "events.jsonl"


def serialize_event(event: EventIn) -> Dict[str, Any]:
    return {
        "source_type": event.source_type.value,
        "source_name": event.source_name,
        "event_id": event.event_id,
        "timestamp": event.timestamp.isoformat(),
        "severity": normalize_severity(event.severity),
        "message": clean_message(event.message),
        "attributes": mask_dict(event.attributes),
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }


def save_event(event: EventIn) -> Dict[str, Any]:
    payload = serialize_event(event)
    path = _event_file_path(payload["source_type"])
    with path.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return payload


def read_all_events() -> List[Dict[str, Any]]:
    settings = get_settings()
    root = settings.data_path / "raw"
    if not root.exists():
        return []

    events: List[Dict[str, Any]] = []
    for file_path in root.glob("*/events.jsonl"):
        with file_path.open("r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    events.sort(key=lambda item: item.get("timestamp", ""), reverse=True)
    return events


def search_events(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    query_terms = {term.lower() for term in query.split() if len(term) > 2}
    events = read_all_events()
    if not query_terms:
        return events[:limit]

    scored: List[tuple[int, Dict[str, Any]]] = []
    for event in events:
        haystack = " ".join(
            [
                str(event.get("source_type", "")),
                str(event.get("source_name", "")),
                str(event.get("severity", "")),
                str(event.get("message", "")),
                json.dumps(event.get("attributes", {})),
            ]
        ).lower()
        score = sum(1 for term in query_terms if term in haystack)
        if score > 0:
            scored.append((score, event))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [event for _, event in scored[:limit]]
