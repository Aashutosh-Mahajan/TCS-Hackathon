"""
Answer Agent — generates an answer grounded in retrieved context using OpenAI.

The system prompt strictly enforces context-grounded answering to minimize
hallucination — the answer should ONLY use information from retrieved snippets.
"""

import time
from openai import OpenAI
from app.agents.state import PipelineState
from app.config import get_settings


SYSTEM_PROMPT = """You are a helpful enterprise AI assistant. Your task is to answer the user's question using ONLY the provided source context snippets.

RULES:
1. Answer ONLY based on the provided context. Do not use any external knowledge.
2. If the context does not contain enough information to answer, say so clearly.
3. Keep your answer concise (2-4 sentences maximum).
4. If the question is in Hindi or Marathi, respond in the same language.
5. Reference the source when possible (e.g., "According to the Employee Handbook...").
6. Do not make up facts, numbers, or policies that are not in the context."""


def answer_agent(state: PipelineState) -> dict:
    """Generate a grounded answer using OpenAI with retrieved context."""
    start = time.perf_counter()
    settings = get_settings()

    query = state["query"]
    snippets = state.get("retrieved_snippets", [])
    language = state.get("detected_language", "en")

    # Build context from retrieved snippets
    context_parts = []
    for i, snippet in enumerate(snippets, 1):
        context_parts.append(
            f"[Source {i}: {snippet['source']} — {snippet.get('section', '')}]\n{snippet['text']}"
        )
    context = "\n\n".join(context_parts) if context_parts else "No relevant sources found."

    user_message = f"""Question: {query}

Retrieved Context:
{context}

Please answer the question based ONLY on the retrieved context above."""

    answer_mode = "model"
    if not settings.use_external_model or not settings.openai_api_key:
        # A deterministic, source-first path keeps the prototype responsive in
        # local/demo environments where an external model is not configured.
        if snippets:
            best = snippets[0]
            answer = f"According to {best['source']}, {best['text']}"
        else:
            answer = "No relevant source evidence was found for this question."
        answer_mode = "source fallback"
    else:
        try:
            client = OpenAI(api_key=settings.openai_api_key)
            response = client.chat.completions.create(
                model=settings.openai_model,
                max_tokens=512,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )
            answer = response.choices[0].message.content or ""
        except Exception:
            if snippets:
                best = snippets[0]
                answer = f"According to {best['source']}, {best['text']}"
            else:
                answer = "No relevant source evidence was found for this question."
            answer_mode = "source fallback"


    duration_ms = (time.perf_counter() - start) * 1000

    trace_entry = {
        "agent": "Answer Agent",
        "input_summary": f"Query + {len(snippets)} snippets | Mode: {answer_mode}",
        "output_summary": f"Generated {len(answer)} char answer",
        "duration_ms": round(duration_ms, 2),
    }

    existing_trace = state.get("agent_trace", [])

    return {
        "answer": answer,
        "answer_mode": answer_mode,
        "agent_trace": existing_trace + [trace_entry],
    }
