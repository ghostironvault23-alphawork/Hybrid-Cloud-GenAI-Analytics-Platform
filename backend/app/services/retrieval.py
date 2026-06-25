from typing import Dict, List
from .storage import search_events


def retrieve_context(question: str, max_events: int = 5) -> List[Dict]:
    """Retrieve relevant events for a question.

    This is a local RAG-style implementation using keyword scoring.
    In production, replace it with Bedrock Knowledge Bases, OpenSearch, or Azure AI Search.
    """
    return search_events(question, limit=max_events)
