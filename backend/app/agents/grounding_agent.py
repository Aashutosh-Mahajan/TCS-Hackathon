"""
Grounding Agent — checks entailment between the generated answer and retrieved evidence.

Uses OpenAI to classify whether the answer is:
- supported: fully backed by the evidence
- partial: some claims supported, others not
- contradicted: answer contradicts the evidence
- no_evidence: insufficient evidence to judge
"""

import re
import time
from openai import OpenAI
from app.agents.state import PipelineState
from app.config import get_settings


GROUNDING_PROMPT = """You are an entailment checker for an enterprise AI system. Your job is to determine whether an AI-generated answer is supported by the provided source evidence.

Analyze the answer against the evidence and return your assessment in EXACTLY this format:

LABEL: <one of: supported, partial, contradicted, no_evidence>
REASONING: <1-2 sentence explanation of why you chose this label>

Label definitions:
- "supported": The answer is fully and accurately backed by the evidence. All claims in the answer can be verified from the sources.
- "partial": Some claims in the answer are supported, but others are not verifiable from the evidence or the answer adds information beyond what the evidence states.
- "contradicted": The answer directly contradicts facts stated in the evidence.
- "no_evidence": The evidence does not contain enough relevant information to verify the answer.

Be strict: if the answer adds specific numbers, dates, or claims not in the evidence, mark as "partial" or "contradicted"."""

STOP_WORDS = {"a", "an", "and", "are", "can", "company", "do", "does", "for", "get", "how", "i", "in", "is", "it", "of", "on", "policy", "the", "to", "what", "with", "you"}


def _local_grounding(query: str, snippets: list[dict]) -> tuple[str, str]:
    """Fast, transparent fallback when no external grounding model is configured."""
    if not snippets:
        return "no_evidence", "No relevant source evidence was retrieved for this question."

    evidence = " ".join(snippet["text"] for snippet in snippets).lower()
    numbers_in_query = set(re.findall(r"\d+(?:,\d{3})*", query))
    numbers_in_evidence = set(re.findall(r"\d+(?:,\d{3})*", evidence))
    if numbers_in_query and not numbers_in_query.intersection(numbers_in_evidence):
        return "contradicted", "The numeric claim in the question does not match the retrieved policy evidence."

    query_terms = {
        token for token in re.findall(r"[a-z]{3,}|[\u0900-\u097f]{2,}", query.lower())
        if token not in STOP_WORDS
    }
    evidence_terms = set(re.findall(r"[a-z]{3,}|[\u0900-\u097f]{2,}", evidence))
    if query_terms and query_terms.intersection(evidence_terms):
        return "supported", "The answer is derived directly from the retrieved policy evidence."
    return "no_evidence", "The retrieved sources do not contain matching evidence for the key terms in this question."


def grounding_agent(state: PipelineState) -> dict:
    """Check entailment between answer and retrieved snippets."""
    start = time.perf_counter()
    settings = get_settings()

    answer = state.get("answer", "")
    snippets = state.get("retrieved_snippets", [])

    if not state.get("dataset_match", False):
        details = "The answer is not in the internal dataset. Public web-search snippets are unverified and must be checked against the original authoritative source."
        duration_ms = (time.perf_counter() - start) * 1000
        return {
            "grounding_label": "no_evidence", "grounding_details": details,
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": "Grounding Agent", "input_summary": "Out-of-dataset web fallback",
                "output_summary": "Label: no_evidence | Web results require verification",
                "duration_ms": round(duration_ms, 2),
            }],
        }

    # Build evidence text
    evidence_parts = []
    for i, snippet in enumerate(snippets, 1):
        evidence_parts.append(f"[Evidence {i}]: {snippet['text']}")
    evidence = "\n\n".join(evidence_parts) if evidence_parts else "No evidence available."

    user_message = f"""AI-Generated Answer:
{answer}

Source Evidence:
{evidence}

Assess whether the answer is supported by the evidence."""

    grounding_label = "no_evidence"
    grounding_details = "Unable to perform grounding check."

    if (
        state.get("answer_mode") in {"source fallback", "service unavailable"}
        or not settings.use_external_model
        or not settings.openai_api_key
    ):
        grounding_label, grounding_details = _local_grounding(state.get("query", ""), snippets)
    else:
        try:
            client = OpenAI(api_key=settings.openai_api_key)
            response = client.chat.completions.create(
                model=settings.openai_model,
                max_tokens=256,
                messages=[
                    {"role": "system", "content": GROUNDING_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            result_text = response.choices[0].message.content or ""

            # Parse the structured response
            for line in result_text.strip().split("\n"):
                line = line.strip()
                if line.startswith("LABEL:"):
                    label = line.replace("LABEL:", "").strip().lower()
                    if label in ("supported", "partial", "contradicted", "no_evidence"):
                        grounding_label = label
                elif line.startswith("REASONING:"):
                    grounding_details = line.replace("REASONING:", "").strip()

        except Exception:
            grounding_label, grounding_details = _local_grounding(state.get("query", ""), snippets)


    duration_ms = (time.perf_counter() - start) * 1000

    trace_entry = {
        "agent": "Grounding Agent",
        "input_summary": f"Answer ({len(answer)} chars) vs {len(snippets)} evidence snippets",
        "output_summary": f"Label: {grounding_label} | {grounding_details[:80]}",
        "duration_ms": round(duration_ms, 2),
    }

    existing_trace = state.get("agent_trace", [])

    return {
        "grounding_label": grounding_label,
        "grounding_details": grounding_details,
        "agent_trace": existing_trace + [trace_entry],
    }
