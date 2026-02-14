# ai

AI services for GraphLearn:
- graph extraction from text (LLM)
- normalization/dedup heuristics
- QA over graph + sources
- question generation and answer grading
- embeddings-based scoring (optional in MVP)

Shared prompts live in `../agents/` and can be extended here.

## Minimal service (stub)

Endpoint:
- POST /extract

Request body:
```json
{
  "text": "Your text here",
  "source_id": "optional-doc-id",
  "locator": "optional-location"
}
```

## Run locally

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

## Run with docker compose

```bash
docker compose --env-file infra/.env -f infra/docker-compose.yml up -d ai
```
