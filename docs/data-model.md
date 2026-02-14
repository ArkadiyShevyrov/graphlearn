# Data Model (draft)

## Node types
- concept
- definition
- theorem
- example
- resource
- topic

## Edge relations
- requires (prerequisite)
- defines
- uses
- illustrates
- applies_to
- related_to
- part_of

## Edge fields (MVP contract)
- from (source node id)
- target (target node id)
- relation (enum above)
- source (optional provenance: source_id + locator)

## Provenance
All nodes/edges may include:
- source_id (document/chunk id)
- locator (page/section/span)
