"""
Confidence Scorer Agent — rule-based fusion of retrieval and grounding signals.

Deliberately chosen over a black-box ML classifier: transparent, auditable,
and defensible — directly aligned with "Responsible Enterprise AI" theme.

Formula: confidence = w1 * retrieval_score + w2 * grounding_multiplier
Weights: w1=0.4, w2=0.6 (grounding matters more than retrieval similarity)
"""

import time
from app.agents.state import PipelineState


# Grounding label → numeric multiplier
GROUNDING_MULTIPLIERS = {
    "supported": 1.0,
    "partial": 0.5,
    "contradicted": 0.1,
    "no_evidence": 0.15,
}

# Weights — grounding is weighted higher because a well-grounded answer
# from a lower-similarity source is more trustworthy than a high-similarity
# source with a contradicted answer
W_RETRIEVAL = 0.4
W_GROUNDING = 0.6

# Tag thresholds
CERTAIN_THRESHOLD = 0.7
UNCERTAIN_THRESHOLD = 0.4


def confidence_agent(state: PipelineState) -> dict:
    """Compute confidence score and tag using rule-based fusion."""
    start = time.perf_counter()

    retrieval_score = state.get("retrieval_score", 0.0)
    grounding_label = state.get("grounding_label", "no_evidence")

    # Get grounding multiplier
    grounding_mult = GROUNDING_MULTIPLIERS.get(grounding_label, 0.15)

    # Compute weighted confidence score
    confidence_score = W_RETRIEVAL * retrieval_score + W_GROUNDING * grounding_mult

    # Clamp to [0, 1]
    confidence_score = max(0.0, min(1.0, confidence_score))

    # Map to tag
    if confidence_score >= CERTAIN_THRESHOLD:
        confidence_tag = "Certain"
    elif confidence_score >= UNCERTAIN_THRESHOLD:
        confidence_tag = "Uncertain"
    else:
        confidence_tag = "Needs Verification"

    # No evidence and contradictions are both explicitly unsafe to act on.
    if grounding_label in {"contradicted", "no_evidence"}:
        confidence_tag = "Needs Verification"
        confidence_score = min(confidence_score, 0.3)

    duration_ms = (time.perf_counter() - start) * 1000

    trace_entry = {
        "agent": "Confidence Scorer",
        "input_summary": f"Retrieval: {retrieval_score:.3f} | Grounding: {grounding_label}",
        "output_summary": f"Score: {confidence_score:.3f} → {confidence_tag}",
        "duration_ms": round(duration_ms, 2),
    }

    existing_trace = state.get("agent_trace", [])

    return {
        "confidence_score": round(confidence_score, 4),
        "confidence_tag": confidence_tag,
        "grounding_multiplier": grounding_mult,
        "agent_trace": existing_trace + [trace_entry],
    }
