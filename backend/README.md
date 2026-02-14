# backend

Backend API for GraphLearn:
- graph CRUD (courses, nodes, edges)
- ingestion endpoints
- progress events

Initial target:
- REST (FastAPI / Node / Spring) + Neo4j driver
- idempotent upserts for nodes/edges
