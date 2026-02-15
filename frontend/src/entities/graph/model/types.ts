export type NodeSource = {
  source_id?: string;
  locator?: string;
};

export type GraphNode = {
  id: string;
  title: string;
  type: string;
  aliases?: string[];
  source?: NodeSource;
  metadata?: Record<string, unknown>;
};

export type GraphEdge = {
  from: string;
  target: string;
  relation: string;
  weight?: number;
  source?: NodeSource;
  metadata?: Record<string, unknown>;
};

export type GraphPayload = {
  nodes: GraphNode[];
  edges: GraphEdge[];
};

export type SelectedNode = GraphNode | null;
