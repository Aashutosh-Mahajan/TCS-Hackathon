// TypeScript types mirroring backend Pydantic models

export interface SnippetResponse {
  text: string;
  score: number;
  source: string;
  language: string;
  category: string;
  url?: string | null;
}

export interface AgentTraceEntry {
  agent: string;
  input_summary: string;
  output_summary: string;
  duration_ms: number;
}

export interface ScoringFactors {
  retrieval_score: number;
  grounding_label: string;
  grounding_details: string;
  retrieval_weight: number;
  grounding_weight: number;
  grounding_multiplier: number;
  formula: string;
}

export type ConfidenceTag = "Certain" | "Uncertain" | "Needs Verification";

export interface QueryResponse {
  query: string;
  detected_language: string;
  answer: string;
  confidence_tag: ConfidenceTag;
  confidence_score: number;
  explanation: string;
  warning: string | null;
  dataset_status: "in_dataset" | "not_in_dataset";
  web_searched: boolean;
  web_search_status: string;
  verification_required: boolean;
  retrieved_snippets: SnippetResponse[];
  scoring_factors: ScoringFactors;
  agent_trace: AgentTraceEntry[];
}

export interface QueryRequest {
  query: string;
}

// Confidence tag color mapping
export const TAG_COLORS: Record<ConfidenceTag, { bg: string; text: string; glow: string; border: string }> = {
  Certain: {
    bg: "rgba(34, 197, 94, 0.15)",
    text: "#22c55e",
    glow: "0 0 20px rgba(34, 197, 94, 0.3)",
    border: "rgba(34, 197, 94, 0.3)",
  },
  Uncertain: {
    bg: "rgba(245, 158, 11, 0.15)",
    text: "#f59e0b",
    glow: "0 0 20px rgba(245, 158, 11, 0.3)",
    border: "rgba(245, 158, 11, 0.3)",
  },
  "Needs Verification": {
    bg: "rgba(239, 68, 68, 0.15)",
    text: "#ef4444",
    glow: "0 0 20px rgba(239, 68, 68, 0.3)",
    border: "rgba(239, 68, 68, 0.3)",
  },
};

// Language display mapping
export const LANGUAGE_LABELS: Record<string, string> = {
  en: "English",
  hi: "हिंदी",
  mr: "मराठी",
};
