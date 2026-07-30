"""
Language Agent — detects the language of the user's query.

Uses langdetect for lightweight detection (no API call needed).
Maps detected language to en/hi/mr, defaulting to 'en' for unknowns.
"""

import time
from langdetect import detect, LangDetectException
from app.agents.state import PipelineState


SUPPORTED_LANGUAGES = {"en", "hi", "mr"}


def language_agent(state: PipelineState) -> dict:
    """Detect the language of the query and add to state."""
    start = time.perf_counter()
    query = state["query"]

    try:
        detected = detect(query)
        # langdetect returns ISO 639-1 codes; Marathi is 'mr', Hindi is 'hi'
        if detected not in SUPPORTED_LANGUAGES:
            detected = "en"
    except LangDetectException:
        detected = "en"

    duration_ms = (time.perf_counter() - start) * 1000

    trace_entry = {
        "agent": "Language Agent",
        "input_summary": f"Query: '{query[:80]}...'",
        "output_summary": f"Detected language: {detected}",
        "duration_ms": round(duration_ms, 2),
    }

    existing_trace = state.get("agent_trace", [])

    return {
        "detected_language": detected,
        "agent_trace": existing_trace + [trace_entry],
    }
