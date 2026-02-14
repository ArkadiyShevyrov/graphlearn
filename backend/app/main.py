from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jsonschema import Draft202012Validator
from neo4j import GraphDatabase

APP_TITLE = "GraphLearn API"

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "graph.schema.json"


def load_schema() -> Dict[str, Any]:
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_validator() -> Draft202012Validator:
    return Draft202012Validator(load_schema())


def parse_origins(raw: str | None) -> List[str]:
    if not raw:
        return ["*"]
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


schema_validator = build_validator()

app = FastAPI(title=APP_TITLE)

app.add_middleware(
    CORSMiddleware,
    allow_origins=parse_origins(os.getenv("CORS_ALLOW_ORIGINS")),
    allow_methods=["*"],
    allow_headers=["*"],
)


class Neo4jClient:
    def __init__(self) -> None:
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self._driver.close()

    def upsert_graph(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> None:
        with self._driver.session() as session:
            session.execute_write(self._upsert_nodes, nodes)
            session.execute_write(self._upsert_edges, edges)

    def fetch_graph(self) -> Dict[str, Any]:
        with self._driver.session() as session:
            nodes = session.execute_read(self._fetch_nodes)
            edges = session.execute_read(self._fetch_edges)
        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def _upsert_nodes(tx, nodes: List[Dict[str, Any]]) -> None:
        tx.run(
            """
            UNWIND $nodes AS node
            MERGE (n:Node {id: node.id})
            SET n.title = node.title,
                n.type = node.type,
                n.aliases = coalesce(node.aliases, []),
                n.metadata = coalesce(node.metadata, {}),
                n.source = coalesce(node.source, {})
            """,
            nodes=nodes,
        )

    @staticmethod
    def _upsert_edges(tx, edges: List[Dict[str, Any]]) -> None:
        prepared = []
        for edge in edges:
            prepared.append({**edge, "from_id": edge.get("from")})

        tx.run(
            """
            UNWIND $edges AS edge
            MATCH (a:Node {id: edge.from_id})
            MATCH (b:Node {id: edge.target})
            MERGE (a)-[r:REL {relation: edge.relation}]->(b)
            SET r.weight = edge.weight,
                r.metadata = coalesce(edge.metadata, {}),
                r.source = coalesce(edge.source, {})
            """,
            edges=prepared,
        )

    @staticmethod
    def _fetch_nodes(tx) -> List[Dict[str, Any]]:
        result = tx.run(
            """
            MATCH (n:Node)
            RETURN n.id AS id,
                   n.title AS title,
                   n.type AS type,
                   n.aliases AS aliases,
                   n.source AS source,
                   n.metadata AS metadata
            ORDER BY n.title
            """
        )
        return [dict(record) for record in result]

    @staticmethod
    def _fetch_edges(tx) -> List[Dict[str, Any]]:
        result = tx.run(
            """
            MATCH (a:Node)-[r:REL]->(b:Node)
            RETURN a.id AS from,
                   b.id AS target,
                   r.relation AS relation,
                   r.weight AS weight,
                   r.source AS source,
                   r.metadata AS metadata
            """
        )
        return [dict(record) for record in result]


neo4j_client = Neo4jClient()


@app.on_event("shutdown")
def shutdown() -> None:
    neo4j_client.close()


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/graph")
def get_graph() -> Dict[str, Any]:
    return neo4j_client.fetch_graph()


@app.post("/graph/ingest")
def ingest_graph(payload: Dict[str, Any] = Body(...)) -> JSONResponse:
    errors = sorted(schema_validator.iter_errors(payload), key=lambda err: err.path)
    if errors:
        details = [
            {
                "path": "/" + "/".join([str(part) for part in err.path]),
                "message": err.message,
            }
            for err in errors
        ]
        return JSONResponse(status_code=422, content={"detail": details})

    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])
    neo4j_client.upsert_graph(nodes, edges)
    return JSONResponse(
        status_code=200,
        content={"status": "ok", "nodes": len(nodes), "edges": len(edges)},
    )
