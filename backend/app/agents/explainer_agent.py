"""
Explainer Agent — generates human-readable explanation and warnings.

Template-based for speed (no LLM call needed). Produces 1-2 sentence
explanations that enterprise users can understand and act on.
"""

import time
from app.agents.state import PipelineState


def explainer_agent(state: PipelineState) -> dict:
    """Generate human-readable explanation and warning based on confidence assessment."""
    start = time.perf_counter()

    confidence_tag = state.get("confidence_tag", "Needs Verification")
    confidence_score = state.get("confidence_score", 0.0)
    grounding_label = state.get("grounding_label", "no_evidence")
    grounding_details = state.get("grounding_details", "")
    retrieval_score = state.get("retrieval_score", 0.0)
    snippets = state.get("retrieved_snippets", [])
    dataset_status = state.get("dataset_status", "not_in_dataset")
    web_searched = state.get("web_searched", False)

    # Get the best source name
    best_source = snippets[0]["source"] if snippets else "unknown source"
    score_pct = round(confidence_score * 100)

    # Generate explanation based on tag
    if confidence_tag == "Certain":
        explanation = (
            f"This answer is well-supported by {best_source} with a confidence score of {score_pct}%. "
            f"The retrieved evidence directly confirms the response."
        )
        warning = ""

    elif confidence_tag == "Uncertain":
        explanation = (
            f"This answer is partially supported (confidence: {score_pct}%). "
            f"{grounding_details} Consider verifying with additional sources before acting on this information."
        )
        warning = "⚠️ Partial evidence — some claims may not be fully verified by available sources."

    else:  # Needs Verification
        if dataset_status == "not_in_dataset":
            search_note = "A public web search was performed" if web_searched else "No public web search was performed"
            explanation = f"This query is not covered by the internal dataset (confidence: {score_pct}%). {search_note}; any displayed web result is unverified and must be checked at its original authoritative source."
            warning = "Verification required: this answer is not in the internal dataset and any web-search content is not verified."
        elif grounding_label == "contradicted":
            explanation = (
                f"This answer may contradict available evidence (confidence: {score_pct}%). "
                f"{grounding_details}"
            )
            warning = "🚨 Warning: The answer appears to contradict the available source evidence. Do not rely on this response without independent verification."
        elif grounding_label == "no_evidence":
            explanation = (
                f"No relevant source evidence was found for this query (confidence: {score_pct}%). "
                f"The answer may not be grounded in verified company documents."
            )
            warning = "🚨 Warning: No supporting evidence found in the knowledge base. This answer should be independently verified."
        else:
            explanation = (
                f"This answer has low confidence ({score_pct}%) based on weak retrieval and grounding signals. "
                f"{grounding_details}"
            )
            warning = "⚠️ Low confidence — please verify this information with authoritative sources."

    duration_ms = (time.perf_counter() - start) * 1000

    trace_entry = {
        "agent": "Explainer Agent",
        "input_summary": f"Tag: {confidence_tag} | Score: {score_pct}%",
        "output_summary": f"Explanation: {explanation[:80]}...",
        "duration_ms": round(duration_ms, 2),
    }

    existing_trace = state.get("agent_trace", [])

    return {
        "explanation": explanation,
        "warning": warning,
        "agent_trace": existing_trace + [trace_entry],
    }
