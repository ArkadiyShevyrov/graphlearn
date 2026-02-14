# ADR 0001: Tech stack for MVP

## Status

Accepted

## Decision

We choose the following baseline stack for the MVP:

- Frontend: React + TypeScript + Vite + Tailwind CSS + Cytoscape.js (FSD)
- Backend API: FastAPI (Python)
- AI workers: Python + LLM SDKs (extraction, QA, assessment)
- Jobs/queues: Celery + Redis
- Data: Neo4j (graph), Postgres (progress/metadata), S3/MinIO (sources)
- Infra: docker compose (local), optional K8s later

## Why this stack

- Single-language backend/AI (Python) simplifies integration and iteration speed.
- Cytoscape.js provides maximum graph interactivity and editor-like control.
- Tailwind CSS keeps UI iteration fast and consistent across the FSD layers.
- Neo4j fits the graph-first data model and supports graph traversal for learning paths.
- Celery + Redis enables async ingestion and long-running AI tasks without blocking the API.
- Postgres and object storage keep non-graph data and raw sources cleanly separated.
- docker compose keeps local setup simple while staying close to production topology.

## Alternatives considered (rejected)

- Frontend: Next.js or React + CRA
  - Rejected for MVP: Vite is faster for iteration and keeps UI bundling minimal.
- Graph UI: Sigma.js + Graphology
  - Rejected for MVP: faster rendering, but less convenient for rich editing interactions.
- Backend: Node/NestJS or Spring Boot
  - Rejected for MVP: split language from AI pipelines and slower iteration for AI-heavy work.
- Graph DB: Memgraph or Postgres (adjacency tables)
  - Rejected for MVP: Neo4j is more mature for graph traversal and tooling.
