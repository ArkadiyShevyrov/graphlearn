import type { GraphPayload } from "../../entities/graph";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL?.toString() || "http://localhost:8000";

export async function fetchGraph(): Promise<GraphPayload> {
  const response = await fetch(`${API_BASE}/graph`);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return (await response.json()) as GraphPayload;
}
