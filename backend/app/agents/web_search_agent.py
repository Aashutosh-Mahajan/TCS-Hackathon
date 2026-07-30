"""Public-web fallback for questions absent from the internal RAG dataset.

Web snippets are deliberately never considered verified internal evidence.
"""

import html
import re
import time
from urllib.parse import parse_qs, unquote, urlparse

import httpx

from app.agents.state import PipelineState
from app.config import get_settings


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", value))).strip()


def _extract_results(page: str, limit: int) -> list[dict]:
    """Extract only displayed title/URL/snippet; do not scrape page content."""
    results: list[dict] = []
    anchors = re.findall(r'<a rel="nofollow" class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', page, re.S)
    snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</(?:a|div)>', page, re.S)
    for index, (href, title) in enumerate(anchors):
        parsed = urlparse(html.unescape(href))
        if parsed.netloc.endswith("duckduckgo.com"):
            href = parse_qs(parsed.query).get("uddg", [""])[0]
        href = unquote(href)
        title = _clean(title)
        snippet = _clean(snippets[index]) if index < len(snippets) else ""
        if href.startswith(("http://", "https://")) and title and snippet:
            results.append({"title": title[:200], "url": href, "snippet": snippet[:700]})
        if len(results) >= limit:
            break
    return results


def web_search_agent(state: PipelineState) -> dict:
    """Search only after a strict internal-dataset evidence gate rejects a query."""
    start = time.perf_counter()
    settings = get_settings()
    existing_trace = state.get("agent_trace", [])
    if state.get("dataset_match"):
        return {
            "web_searched": False, "web_search_status": "not_needed", "verification_required": False,
            "agent_trace": existing_trace + [{"agent": "Web Search Agent", "input_summary": "Internal dataset match found", "output_summary": "Skipped public web search", "duration_ms": 0.0}],
        }

    results: list[dict] = []
    status = "no_results"
    if settings.enable_web_search:
        try:
            response = httpx.get(
                "https://html.duckduckgo.com/html/", params={"q": state["query"]},
                headers={"User-Agent": "Mozilla/5.0 (compatible; ResponsibleRAG/1.0)"},
                timeout=settings.web_search_timeout_seconds, follow_redirects=True,
            )
            response.raise_for_status()
            results = _extract_results(response.text, settings.web_search_results)
            status = "results_found" if results else "no_results"
        except httpx.HTTPError:
            status = "unavailable"
    else:
        status = "disabled"

    web_snippets = [{
        "text": item["snippet"], "score": 0.0, "source": f"Web search: {item['title']}",
        "url": item["url"], "language": state.get("detected_language", "en"),
        "category": "web_search", "section": "Public web search result",
    } for item in results]
    duration_ms = (time.perf_counter() - start) * 1000
    return {
        "retrieved_snippets": web_snippets, "web_searched": True, "web_search_status": status,
        "verification_required": True,
        "agent_trace": existing_trace + [{
            "agent": "Web Search Agent", "input_summary": "No internal dataset match; public-web fallback requested",
            "output_summary": f"Status: {status} | Results: {len(results)} | Verification required",
            "duration_ms": round(duration_ms, 2),
        }],
    }
