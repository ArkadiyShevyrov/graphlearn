# infra

Local dev stack and deployment notes.

Includes:
- docker compose for Neo4j
- environment examples
- runbooks for developers

## Local stack

From repo root:
```bash
cp infra/.env.example infra/.env
docker compose --env-file infra/.env -f infra/docker-compose.yml up -d
```

Services:
- Neo4j: http://localhost:7474
- Backend API: http://localhost:8000
- AI service: http://localhost:8001
