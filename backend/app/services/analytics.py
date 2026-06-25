from collections import Counter
from ..models import SummaryReport
from .storage import read_all_events


def build_summary_report() -> SummaryReport:
    events = read_all_events()
    by_source = Counter(event.get("source_type", "unknown") for event in events)
    by_severity = Counter(event.get("severity", "unknown") for event in events)

    return SummaryReport(
        total_events=len(events),
        events_by_source=dict(by_source),
        events_by_severity=dict(by_severity),
        latest_events=events[:5],
    )
