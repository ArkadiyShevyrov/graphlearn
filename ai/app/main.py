from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from jsonschema import Draft202012Validator
from pydantic import BaseModel

APP_TITLE = "GraphLearn AI"
SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "graph.schema.json"


def load_schema() -> Dict[str, Any]:
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_validator() -> Draft202012Validator:
    return Draft202012Validator(load_schema())


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug


schema_validator = build_validator()
app = FastAPI(title=APP_TITLE)


class ExtractRequest(BaseModel):
    text: str
    source_id: Optional[str] = None
    locator: Optional[str] = None


@app.post("/extract")
def extract_graph(payload: ExtractRequest = Body(...)) -> JSONResponse:
    raw_text = payload.text.strip()
    digest = hashlib.sha1(raw_text.encode("utf-8")).hexdigest()[:10]
    title_seed = raw_text.splitlines()[0] if raw_text else "Untitled"
    title = title_seed[:80]
    base_slug = slugify(title)
    node_id = f"concept-{base_slug or 'text'}-{digest}"

    node: Dict[str, Any] = {
        "id": node_id,
        "title": title,
        "type": "concept",
        "metadata": {"stub": True},
    }

    source = {}
    if payload.source_id:
        source["source_id"] = payload.source_id
    if payload.locator:
        source["locator"] = payload.locator
    if source:
        node["source"] = source

    graph = {"nodes": [node], "edges": []}
    errors = sorted(schema_validator.iter_errors(graph), key=lambda err: err.path)
    if errors:
        return JSONResponse(
            status_code=500,
            content={"detail": "Stub output failed schema validation."},
        )

    return JSONResponse(status_code=200, content=graph)
