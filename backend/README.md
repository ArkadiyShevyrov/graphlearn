# backend

Backend API for GraphLearn:
- graph CRUD (courses, nodes, edges)
- ingestion endpoints
- progress events

Baseline stack:
- FastAPI (Python)
- Neo4j driver

Minimal endpoints:
- GET /health
- POST /graph/ingest
- GET /graph

Example ingest payload:
```json
{
  "nodes": [
    { "id": "n1", "title": "Vector", "type": "concept" },
    { "id": "n2", "title": "Vector addition", "type": "concept" }
  ],
  "edges": [
    { "from": "n1", "target": "n2", "relation": "requires" }
  ]
}
```

## Run locally

1) Create venv and install deps:
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Set env (example):
```bash
$env:NEO4J_URI="bolt://localhost:7687"
$env:NEO4J_USER="neo4j"
$env:NEO4J_PASSWORD="password"
```

3) Run the API:
```bash
uvicorn app.main:app --reload --port 8000
```

## Run with docker compose

```bash
docker compose --env-file infra/.env -f infra/docker-compose.yml up -d backend
```
