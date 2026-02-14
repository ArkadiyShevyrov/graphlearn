# Agent Context (GraphLearn)

This document is a **global contract** for any LLM/agent working in this repository.

## Mission

Build GraphLearn: a system that turns learning materials into a **knowledge graph** and uses the graph to support:
- explanations grounded in nodes/edges,
- assessment and gap detection,
- learning path recommendations.

## What is “truth” here

The **knowledge graph** is the central artifact.
All AI outputs must either:
- update the graph via strict contracts, or
- answer questions using the graph + referenced sources.

## Strict rules for extraction agents

### Output format
Extraction output must be **only JSON**, no markdown, no prose.

See: `schemas/graph.schema.json`

### Grounding
Do not invent nodes or edges.
Only extract what is supported by the provided text chunk.

### Chunking
If input is too large:
- chunk it,
- run extraction per chunk,
- merge with stable IDs and dedup rules (see `agents/workflows/ingest_text.md`).

### Normalization
After extraction:
- normalize node titles (trim, unify casing rules),
- merge duplicates (alias mapping),
- keep provenance if available (source_id + span/page/line).

## Rules for QA/explanations agents

- Prefer graph-based answers (prerequisites, neighbor nodes, edge reasons).
- If confidence is low or the graph lacks data, say so explicitly and ask for missing context.
- Never “fill gaps” with plausible-looking but unsupported statements.

## Developer ergonomics

When you modify any contract:
- update schemas,
- update docs,
- update affected prompts/workflows under `agents/`.

## Where agent artifacts live

- Root/shared: `agents/`
- Per-module: `<module>/agents/`

Agent artifacts are framework-agnostic:
store prompts, workflows, tool contracts, and runbooks — then wire them into your preferred orchestrator (LangGraph / Agents SDK / etc.).
