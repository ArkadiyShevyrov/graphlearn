import { useEffect, useMemo, useRef } from "react";
import cytoscape from "cytoscape";
import { useGraphExplorer } from "../model/useGraphExplorer";
import type { GraphNode } from "../../../entities/graph";

export default function GraphExplorer() {
  const { graph, status, selectedNode, setSelectedNode, loadGraph } =
    useGraphExplorer();
  const containerRef = useRef<HTMLDivElement | null>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  const elements = useMemo(() => {
    const nodes = graph.nodes.map((node) => ({
      data: {
        id: node.id,
        label: node.title,
        title: node.title,
        type: node.type,
        aliases: node.aliases ?? [],
        source: node.source ?? null,
        metadata: node.metadata ?? null,
      },
    }));

    const edges = graph.edges.map((edge) => ({
      data: {
        id: `${edge.from}__${edge.relation}__${edge.target}`,
        source: edge.from,
        target: edge.target,
        relation: edge.relation,
        weight: edge.weight ?? null,
        provenance: edge.source ?? null,
        metadata: edge.metadata ?? null,
      },
    }));

    return [...nodes, ...edges];
  }, [graph]);

  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements: [],
      layout: { name: "cose" },
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#1f5b7a",
            label: "data(label)",
            "text-wrap": "wrap",
            "text-max-width": "140px",
            color: "#f2f7f9",
            "font-size": "12px",
            "text-valign": "center",
            "text-halign": "center",
            width: "label",
            height: "label",
            padding: "14px",
            shape: "round-rectangle",
          },
        },
        {
          selector: "edge",
          style: {
            width: 2,
            "line-color": "#6aa1b5",
            "target-arrow-color": "#6aa1b5",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            label: "data(relation)",
            "font-size": "10px",
            color: "#3c5160",
            "text-background-color": "#ffffff",
            "text-background-opacity": 0.7,
            "text-background-padding": "3px",
          },
        },
        {
          selector: ":selected",
          style: {
            "background-color": "#f46b45",
            "line-color": "#f46b45",
            "target-arrow-color": "#f46b45",
          },
        },
      ],
    });

    cy.on("tap", "node", (event) => {
      const data = event.target.data() as GraphNode & {
        aliases?: string[];
        source?: { source_id?: string; locator?: string };
        metadata?: Record<string, unknown>;
      };
      setSelectedNode({
        id: data.id,
        title: data.title,
        type: data.type,
        aliases: data.aliases ?? [],
        source: data.source ?? undefined,
        metadata: data.metadata ?? undefined,
      });
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
      cyRef.current = null;
    };
  }, [setSelectedNode]);

  useEffect(() => {
    if (!cyRef.current) {
      return;
    }
    cyRef.current.json({ elements });
    cyRef.current.layout({ name: "cose", animate: false }).run();
    cyRef.current.fit();
  }, [elements]);

  return (
    <div className="app min-h-screen">
      <section className="panel panel-main">
        <header className="panel-header">
          <div>
            <h1>GraphLearn</h1>
            <p className="subtitle">Graph exploration MVP</p>
          </div>
          <div className="actions">
            <button onClick={loadGraph}>Reload</button>
          </div>
        </header>
        <div className="status">{status}</div>
        <div className="graph-canvas" ref={containerRef} />
      </section>
      <aside className="panel panel-side">
        <h2>Node details</h2>
        {!selectedNode ? (
          <p className="muted">Select a node to see details.</p>
        ) : (
          <div className="details">
            <div className="detail-row">
              <span className="label">ID</span>
              <span>{selectedNode.id}</span>
            </div>
            <div className="detail-row">
              <span className="label">Title</span>
              <span>{selectedNode.title}</span>
            </div>
            <div className="detail-row">
              <span className="label">Type</span>
              <span>{selectedNode.type}</span>
            </div>
            <div className="detail-row">
              <span className="label">Aliases</span>
              <span>
                {selectedNode.aliases && selectedNode.aliases.length > 0
                  ? selectedNode.aliases.join(", ")
                  : "-"}
              </span>
            </div>
            <div className="detail-row">
              <span className="label">Source</span>
              <span>
                {selectedNode.source?.source_id || "-"}
                {selectedNode.source?.locator
                  ? ` (${selectedNode.source.locator})`
                  : ""}
              </span>
            </div>
          </div>
        )}
      </aside>
    </div>
  );
}
