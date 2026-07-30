from pydantic import BaseModel, Field


# --- Request Models ---

class QueryRequest(BaseModel):
    """Incoming query from the frontend."""
    query: str = Field(..., min_length=1, max_length=2000, description="User question in any supported language")


# --- Response Models ---

class SnippetResponse(BaseModel):
    """A single retrieved source snippet."""
    text: str
    score: float = Field(..., ge=0.0, le=1.0)
    source: str
    language: str
    category: str = ""


class AgentTraceEntry(BaseModel):
    """Execution trace for a single agent in the pipeline."""
    agent: str
    input_summary: str
    output_summary: str
    duration_ms: float


class ScoringFactors(BaseModel):
    """Breakdown of all factors that went into the confidence score."""
    retrieval_score: float = Field(..., ge=0.0, le=1.0, description="Best retrieval similarity score")
    grounding_label: str = Field(..., description="supported / partial / contradicted / no_evidence")
    grounding_details: str = Field(..., description="Reasoning behind grounding label")
    retrieval_weight: float = Field(default=0.4, description="Weight given to retrieval score")
    grounding_weight: float = Field(default=0.6, description="Weight given to grounding")
    grounding_multiplier: float = Field(..., ge=0.0, le=1.0, description="Numeric grounding factor")
    formula: str = Field(..., description="Human-readable formula used")


class QueryResponse(BaseModel):
    """Full pipeline response returned to the frontend."""
    query: str
    detected_language: str
    answer: str
    confidence_tag: str = Field(..., description="Certain / Uncertain / Needs Verification")
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    explanation: str
    warning: str | None = None
    retrieved_snippets: list[SnippetResponse]
    scoring_factors: ScoringFactors
    agent_trace: list[AgentTraceEntry]
