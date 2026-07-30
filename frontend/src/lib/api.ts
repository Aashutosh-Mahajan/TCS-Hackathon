import { QueryRequest, QueryResponse } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Submit a query to the backend pipeline.
 */
export async function submitQuery(query: string): Promise<QueryResponse> {
  const payload: QueryRequest = { query };

  const response = await fetch(`${API_BASE}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail || `API error: ${response.status}`);
  }

  return response.json();
}

/**
 * Health check for the backend.
 */
export async function getHealth(): Promise<{ status: string; dataset_size: number; model: string }> {
  const response = await fetch(`${API_BASE}/api/health`);
  if (!response.ok) {
    throw new Error("Backend is not available");
  }
  return response.json();
}
