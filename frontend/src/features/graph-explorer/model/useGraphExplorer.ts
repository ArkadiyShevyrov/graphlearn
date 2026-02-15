import { useCallback, useEffect, useState } from "react";
import type { GraphPayload, SelectedNode } from "../../../entities/graph";
import { emptyGraph } from "../../../entities/graph";
import { fetchGraph } from "../../../shared/api/graphApi";

export function useGraphExplorer() {
  const [graph, setGraph] = useState<GraphPayload>(emptyGraph);
  const [status, setStatus] = useState<string>("Idle");
  const [selectedNode, setSelectedNode] = useState<SelectedNode>(null);

  const loadGraph = useCallback(async () => {
    setStatus("Loading graph...");
    try {
      const data = await fetchGraph();
      setGraph(data);
      setStatus(`Loaded ${data.nodes.length} nodes / ${data.edges.length} edges.`);
    } catch (error) {
      setStatus("Failed to load graph.");
      setGraph(emptyGraph);
    }
  }, []);

  useEffect(() => {
    loadGraph();
  }, [loadGraph]);

  return {
    graph,
    status,
    selectedNode,
    setSelectedNode,
    loadGraph,
  };
}
