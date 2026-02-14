# Architecture (draft)

GraphLearn is a graph-first learning platform.

## Components (high level)

- Frontend: graph visualization + learning UX
- Backend: Graph API + ingestion endpoints + progress tracking
- AI: extraction, QA, question generation, grading (LLM + embeddings)
- Infra: local dev stack, CI, deploy notes

## Data stores

- Graph DB (e.g., Neo4j)
- Source documents store (files, sections, metadata)
- Progress store (events + mastery scores)

## Design principles

- Contracts first (schemas)
- Idempotent ingestion
- Provenance everywhere (edges/nodes linked to sources)
- Human-in-the-loop editing where needed
