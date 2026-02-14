# Workflow: ingest_text → graph

Goal: turn raw educational text into a stored knowledge graph with deduped nodes/edges.

## Steps

1) **Chunk input**
- Keep chunk boundaries stable (e.g., by headings or ~1-2k tokens).
- Assign each chunk a `source_id` and `locator` strategy (page/section/offset).

2) **Extract (per chunk)**
- Call extraction prompt: `agents/prompts/extract_graph.system.md`
- Output must validate against `schemas/graph.schema.json`
- Do not invent facts/relations.

3) **Normalize**
- Canonicalize node titles (trim, normalize whitespace).
- Create alias map for duplicates.
- Prefer stable IDs: `slug(title)+hash(type)` or DB-generated IDs with alias mapping.

4) **Merge**
- Deduplicate nodes by canonical title + type (and alias list).
- Deduplicate edges by (source,target,relation).
- Preserve provenance: keep `source_id` + `locator` for nodes/edges.

5) **Persist**
- Use idempotent operations (MERGE) in graph DB.
- Store raw source documents separately if available.

## Output
- Graph DB updated
- Optional: a merge report (counts, dedup decisions, conflicts)
