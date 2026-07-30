"""
FastAPI application — main entry point for the AI Hallucination Confidence Labeler.

Startup sequence:
1. Load embedding model (multilingual-e5-small)
2. Load and index the RAG dataset (dense + sparse)
3. Compile LangGraph pipeline
"""

import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import QueryRequest, QueryResponse, SnippetResponse, AgentTraceEntry, ScoringFactors
from app.rag.embeddings import encode_passages, preload_model
from app.rag.bm25_index import BM25Index
from app.rag.vector_store import VectorStore
from app.agents.retriever_agent import init_retriever
from app.agents.graph import run_pipeline


# Global stores
_dataset: list[dict] = []


def _load_dataset() -> list[dict]:
    """Load the RAG dataset from JSON."""
    data_path = Path(__file__).parent / "data" / "rag_dataset.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: load models, build indices. Shutdown: cleanup."""
    global _dataset

    print("[START] Starting AI Hallucination Confidence Labeler...")

    # 1. Load dataset
    print("[DATA] Loading RAG dataset...")
    _dataset = _load_dataset()
    passages = [entry["passage"] for entry in _dataset]
    print(f"   Loaded {len(_dataset)} entries")

    # 2. Load embedding model and encode passages
    print("[MODEL] Loading multilingual-e5-small model...")
    preload_model()
    print("[EMBED] Encoding passages...")
    passage_embeddings = encode_passages(passages)

    # 3. Build vector store
    vector_store = VectorStore()
    metadata = [
        {
            "text": entry["passage"],
            "source": entry["metadata"]["source"],
            "language": entry["language"],
            "category": entry["category"],
        }
        for entry in _dataset
    ]
    vector_store.add(passage_embeddings, metadata)
    print(f"   Vector store: {vector_store.size} vectors indexed")

    # 4. Build BM25 index
    print("[BM25] Building BM25 index...")
    bm25_index = BM25Index()
    bm25_index.build(passages)

    # 5. Initialize retriever with indices
    init_retriever(vector_store, bm25_index, _dataset)

    print("[READY] System ready!")
    yield

    print("[STOP] Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="AI Hallucination Confidence Labeler",
    description="Multi-agent RAG system that labels AI answers with confidence and reliability tags",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for Next.js frontend
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- API Endpoints ---

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "dataset_size": len(_dataset),
        "model": "multilingual-e5-small",
    }


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a user query through the full agent pipeline.

    Returns the answer with confidence tag, score, explanation,
    source snippets, scoring factors breakdown, and agent trace.
    """
    try:
        # Run the LangGraph pipeline
        result = await run_pipeline(request.query)

        # Build response
        snippets = [
            SnippetResponse(
                text=s["text"],
                score=s["score"],
                source=s["source"],
                language=s["language"],
                category=s.get("category", ""),
                url=s.get("url"),
            )
            for s in result.get("retrieved_snippets", [])
        ]

        agent_trace = [
            AgentTraceEntry(**t)
            for t in result.get("agent_trace", [])
        ]

        scoring_factors = ScoringFactors(
            retrieval_score=result.get("retrieval_score", 0.0),
            grounding_label=result.get("grounding_label", "no_evidence"),
            grounding_details=result.get("grounding_details", ""),
            retrieval_weight=0.4,
            grounding_weight=0.6,
            grounding_multiplier=result.get("grounding_multiplier", 0.0),
            formula=f"confidence = 0.4 × retrieval({result.get('retrieval_score', 0):.3f}) + 0.6 × grounding({result.get('grounding_multiplier', 0):.2f}) = {result.get('confidence_score', 0):.3f}",
        )

        return QueryResponse(
            query=result.get("query", request.query),
            detected_language=result.get("detected_language", "en"),
            answer=result.get("answer", ""),
            confidence_tag=result.get("confidence_tag", "Needs Verification"),
            confidence_score=result.get("confidence_score", 0.0),
            explanation=result.get("explanation", ""),
            warning=result.get("warning", None) or None,
            dataset_status=result.get("dataset_status", "not_in_dataset"),
            web_searched=result.get("web_searched", False),
            web_search_status=result.get("web_search_status", "not_needed"),
            verification_required=result.get("verification_required", False),
            retrieved_snippets=snippets,
            scoring_factors=scoring_factors,
            agent_trace=agent_trace,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")


@app.get("/api/dataset")
async def get_dataset():
    """Return the full dataset for frontend demo/test mode."""
    return {"entries": _dataset, "count": len(_dataset)}
