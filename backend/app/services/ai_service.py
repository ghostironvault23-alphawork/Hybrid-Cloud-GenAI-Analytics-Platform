import json
from typing import Dict, List, Tuple
from ..config import get_settings


def _format_events(events: List[Dict]) -> str:
    if not events:
        return "No matching enterprise context found."

    lines = []
    for idx, event in enumerate(events, start=1):
        lines.append(
            f"{idx}. [{event.get('severity')}] {event.get('source_name')} "
            f"at {event.get('timestamp')}: {event.get('message')}"
        )
    return "\n".join(lines)


def build_prompt(question: str, context_events: List[Dict]) -> str:
    context = _format_events(context_events)
    return f"""
You are an enterprise AI analyst.
Use only the provided context.
Do not guess if data is missing.

Question:
{question}

Context:
{context}

Return:
1. Summary
2. Root Cause or Key Finding
3. Business Impact
4. Recommended Fix
5. Prevention Steps
""".strip()


def mock_ai_answer(question: str, context_events: List[Dict]) -> Tuple[str, str]:
    """Deterministic local AI-style answer for safe demo."""
    if not context_events:
        return (
            "Summary: I could not find enough matching enterprise context for this question.\n\n"
            "Root Cause or Key Finding: Not enough relevant data was available in the local data lake.\n\n"
            "Business Impact: The issue cannot be confirmed without logs, tickets, metrics, or telemetry.\n\n"
            "Recommended Fix: Ingest more relevant cloud logs, IoT events, or on-prem tickets and retry the analysis.\n\n"
            "Prevention Steps: Add structured ingestion, source tagging, timestamps, and severity levels for every event.",
            "low",
        )

    critical_or_error = [
        event for event in context_events
        if event.get("severity") in {"critical", "error"}
    ]
    main_event = critical_or_error[0] if critical_or_error else context_events[0]

    summary = main_event.get("message", "Relevant event found.")
    source = main_event.get("source_name", "unknown source")
    severity = main_event.get("severity", "info")

    answer = (
        f"Summary: The most relevant event came from {source} with severity '{severity}'. "
        f"The event states: {summary}\n\n"
        "Root Cause or Key Finding: Based on the retrieved context, the issue is linked to the highest-severity "
        "event and related operational signals in the platform data lake.\n\n"
        "Business Impact: This can affect service reliability, reporting accuracy, user experience, or operational response time depending on the impacted system.\n\n"
        "Recommended Fix: Validate the impacted service, review recent deployments or configuration changes, check resource metrics, and apply the corrective action shown in the logs or ticket.\n\n"
        "Prevention Steps: Add proactive monitoring, alert thresholds, deployment checks, automated rollback rules, and periodic data quality validation."
    )

    confidence = "high" if len(context_events) >= 3 else "medium"
    return answer, confidence


def bedrock_answer(question: str, context_events: List[Dict]) -> Tuple[str, str]:
    """Optional Bedrock integration.

    Requires AWS credentials, Bedrock model access, and USE_BEDROCK=true.
    """
    settings = get_settings()
    prompt = build_prompt(question, context_events)

    try:
        import boto3

        client = boto3.client("bedrock-runtime", region_name=settings.aws_region)
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 800,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = client.invoke_model(
            modelId=settings.bedrock_model_id,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json",
        )
        payload = json.loads(response["body"].read())
        text = payload["content"][0]["text"]
        return text, "medium"
    except Exception as exc:
        fallback, _ = mock_ai_answer(question, context_events)
        return (
            fallback
            + f"\n\nNote: Bedrock call failed and local mock response was used. Reason: {str(exc)}",
            "medium",
        )


def generate_answer(question: str, context_events: List[Dict]) -> Tuple[str, str]:
    settings = get_settings()
    if settings.use_bedrock:
        return bedrock_answer(question, context_events)
    return mock_ai_answer(question, context_events)
