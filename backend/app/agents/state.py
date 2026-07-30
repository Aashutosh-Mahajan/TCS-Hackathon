"""
Pipeline state schema — the shared typed dict that flows through all LangGraph nodes.

Every agent reads from and writes to this state, making the full pipeline
inspectable and auditable (a core requirement for Responsible Enterprise AI).
"""

from typing import TypedDict


class PipelineState(TypedDict, total=False):
    """Shared state that flows through the LangGraph agent pipeline."""

    # Input
    query: str                          # Original user question

    # Language Agent output
    detected_language: str              # en / hi / mr

    # Retriever Agent output
    retrieved_snippets: list[dict]      # [{text, score, source, language, category}]
    retrieval_score: float              # Best retrieval similarity (0–1)

    # Answer Agent output
    answer: str                         # Generated answer
    answer_mode: str                    # model / source fallback / service unavailable

    # Grounding Agent output
    grounding_label: str                # supported / partial / contradicted / no_evidence
    grounding_details: str              # Entailment reasoning

    # Confidence Scorer output
    confidence_score: float             # 0–1 numeric confidence
    confidence_tag: str                 # Certain / Uncertain / Needs Verification
    grounding_multiplier: float         # Numeric grounding factor used in formula

    # Explainer Agent output
    explanation: str                    # Human-readable reason
    warning: str                        # Warning if evidence weak/missing (empty string if none)

    # Pipeline trace
    agent_trace: list[dict]             # [{agent, input_summary, output_summary, duration_ms}]
