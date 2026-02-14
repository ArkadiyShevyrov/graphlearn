# frontend

UI for GraphLearn:
- graph visualization
- browsing nodes/edges
- learning flows (questions, answers, progress)

Baseline stack:
- React + TypeScript + Vite + Tailwind CSS + Cytoscape.js

Architecture:
- Feature-Sliced Design (FSD)
- Layers: app, pages, widgets, features, entities, shared

Current MVP screen:
- load graph from backend
- visualize nodes/edges
- click node to view details

See also: `../AGENTS.md`

## Run locally

```bash
npm install
npm run dev
```

Env (optional):
```bash
$env:VITE_API_BASE_URL="http://localhost:8000"
```
