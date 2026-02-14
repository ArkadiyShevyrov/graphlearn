# GraphLearn (graphlearn)

GraphLearn is an educational platform where learning content is represented as a **knowledge graph** (concepts + relationships).
AI features are built **on top of** this graph to help learners:

- navigate prerequisites (“what must I know first?”),
- get explanations tied to graph nodes/edges,
- test understanding and find knowledge gaps,
- build personalized learning paths.

This repository is designed as a **monorepo** with separate modules (frontend, backend, ai, infra), while keeping shared contracts (schemas) and agent/orchestration artifacts consistent across modules.

---

## Core idea

1) **Knowledge graph as the source of truth**
- Nodes: concepts / definitions / theorems / examples / resources
- Edges: relations like `requires`, `defines`, `uses`, `illustrates`, `applies_to`

2) **AI as an assistant over the graph**
- extraction of nodes/edges from text into a strict JSON contract,
- QA and explanations grounded in the graph + referenced sources,
- assessment (semantic grading) and gap analysis,
- recommendations based on prerequisite chains.

---

## MVP scope (first milestone)

- Upload / paste educational text → extract nodes/edges (strict JSON) → normalize/deduplicate → store in graph DB
- Visualize the graph and allow user to explore it
- “Check understanding” flow:
  - generate questions per node/topic,
  - accept free-form answers,
  - grade semantically + point to prerequisite nodes.

---

## Repository layout

```
graphlearn/
  README.md
  AGENTS.md                       # global agent context / rules
  agents/                         # shared prompts & workflows (framework-agnostic)
  schemas/                        # JSON schemas for contracts
  docs/                           # architecture, data model, roadmap
  frontend/                       # UI (graph visualization + learning flows)
  backend/                        # API (graph CRUD, ingestion, progress)
  ai/                             # LLM/embedding services, extraction pipelines
  infra/                          # docker compose, deployment notes
```

---

## Tech stack (baseline)

- Frontend: React + TypeScript + Vite + Cytoscape.js
- Backend API: FastAPI (Python)
- AI workers: Python + LLM SDKs (extraction, QA, assessment)
- Jobs/queues: Celery + Redis
- Data: Neo4j (graph), Postgres (progress/metadata), S3/MinIO (sources)
- Infra: docker compose (local), optional K8s later

---

## Quick start (dev)

This repo ships with a minimal dev stack for local work (Neo4j + placeholders).

1) Copy env example and edit as needed:
```bash
cp infra/.env.example infra/.env
```

2) Start services:
```bash
cd infra
docker compose up -d
```

3) Open Neo4j Browser:
- http://localhost:7474

---

## Contracts (important)

All LLM extraction must output **only** valid JSON that follows:
- `schemas/graph.schema.json`

If the text is large, extraction may chunk input but must merge results deterministically and idempotently.

---

## License

Choose a license before publishing publicly (MIT/Apache-2.0/etc.).
