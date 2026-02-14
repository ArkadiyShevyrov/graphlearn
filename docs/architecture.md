# Architecture (draft)

GraphLearn is a graph-first learning platform.

## Components (high level)

- Frontend: graph visualization + learning UX
- Backend: Graph API + ingestion endpoints + progress tracking
- AI: extraction, QA, question generation, grading (LLM + embeddings)
- Infra: local dev stack, CI, deploy notes

## MVP stack (baseline)

- Frontend: React + TypeScript + Vite + Cytoscape.js
- Backend API: FastAPI (Python)
- AI workers: Python + LLM SDKs (extraction, QA, assessment)
- Jobs/queues: Celery + Redis
- Data: Neo4j (graph), Postgres (progress/metadata), S3/MinIO (sources)
- Infra: docker compose (local), optional K8s later

## Data stores

- Graph DB (e.g., Neo4j)
- Source documents store (files, sections, metadata)
- Progress store (events + mastery scores)

## Design principles

- Contracts first (schemas)
- Idempotent ingestion
- Provenance everywhere (edges/nodes linked to sources)
- Human-in-the-loop editing where needed
