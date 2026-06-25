def clean_message(message: str) -> str:
    return " ".join(message.strip().split())


def normalize_severity(severity: str) -> str:
    normalized = severity.strip().lower()
    allowed = {"debug", "info", "warning", "error", "critical"}
    return normalized if normalized in allowed else "info"
