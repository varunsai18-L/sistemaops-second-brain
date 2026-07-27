# PVMS 2.0 — Implementation Status

This tracks what from `PVMS_2_0_Product_Improvement_and_Commercialization_Roadmap.docx`
has been implemented in this codebase, and what is intentionally left as
infrastructure work you'll need to provision yourself (it can't be
faked into "working" without real servers to deploy it against).

## Shipped in this update

All items below run today, on the existing Streamlit + local-JSON
stack — no new servers, databases, or paid APIs required. Each is a
new module under `src/pvms/`, wired into the pipeline through
`src/pvms/agents/multi_agent_orchestrator.py` and surfaced in the UI
(`app/main.py`).

| Roadmap item | Module | UI surface |
|---|---|---|
| Advanced RFQ Intelligence | `intelligence/compliance_extractor.py` | "Advanced Intelligence" tab |
| AI Risk Engine (5 dimensions) | `scoring/ai_risk_engine.py` | "Advanced Intelligence" tab |
| Smart Cost Estimation | `scoring/smart_cost_estimation.py` | "Team & Smart Costing" tab |
| Historical Project Matching | `matching/historical_matching.py` | "Advanced Intelligence" tab |
| Capacity Planning | `capacity/capacity_planning.py` | "Team & Smart Costing" tab |
| Proposal Generation | `proposal/proposal_generator.py` | "Proposal" tab (Word download) |
| Executive Dashboard | `dashboard/executive_dashboard.py` | Sidebar → "Executive Dashboard" |
| Competitive Intelligence | `intelligence/competitive_intelligence.py` | Sidebar → "Competitive Intelligence" |
| Knowledge Graph | `knowledge/knowledge_graph.py` | Sidebar → "Knowledge Graph" |
| Multi-Agent AI | `agents/multi_agent_orchestrator.py` | Runs every upload (Parser → Technical → Finance → Risk → Proposal → Reviewer) |

Each module degrades gracefully: if a document doesn't contain a given
signal (no evaluation weights, no penalty clauses, no budget, etc.),
that section is simply omitted rather than shown with invented data —
same convention the original codebase already used.

Historical matching and the knowledge graph both improve automatically
as more RFQs are processed, since they read from `data/outputs/`.

## Deliberately not implemented: infrastructure swap

The roadmap's "Recommended Architecture" section calls for replacing
the current stack with:

- **Frontend:** React (current: Streamlit)
- **Backend:** FastAPI
- **Database:** PostgreSQL (relational) + Neo4j (knowledge graph) + pgvector (semantic search)
- **Queue:** Redis + Celery
- **Storage:** MinIO/S3
- **SSO, RBAC, audit logs, on-prem packaging** for commercial tiers

This is a genuine infrastructure migration — it needs servers to
stand up, connection strings to configure, and a hosting environment
to deploy to. None of that exists in "a zip file you run" the way the
current Streamlit app does. Faking it (e.g. shipping FastAPI routes
with no database behind them) would produce something that *looks*
done but doesn't actually run, which fails the "must work" requirement
harder than not touching it at all.

What this update does instead: every *capability* the new architecture
was meant to unlock (semantic historical matching, a queryable
knowledge graph, capacity-aware team planning) is delivered now, on
file-based storage, with a clean seam to swap in Postgres/Neo4j/pgvector
later:

- `matching/historical_matching.py` — swap the TF-IDF scorer for pgvector without touching callers.
- `knowledge/knowledge_graph.py` — swap `build_graph()`'s in-memory adjacency for a Neo4j driver without touching callers.
- `capacity/capacity_planning.py` — swap the JSON employee store for a Postgres table without touching callers.

If/when you provision Postgres, Neo4j, Redis, and a FastAPI/React
stack, migrating is a matter of reimplementing these three modules'
internals — the rest of the pipeline (agents, UI, report generation)
does not need to change.

## Not addressed by this update

- **Commercialization strategy, pricing tiers (Starter/Professional/Enterprise), SSO/RBAC, audit logs** — these are business/product and platform-security decisions, not code that can be "added" to a repo; they need a real auth provider and a decision on target customers/pricing.
- **MongoDB → PostgreSQL migration** — `repositories/mongo.py` is unused by the live Streamlit pipeline today (the app runs entirely on local JSON files), so there was nothing to migrate; a real migration would happen alongside the FastAPI/Postgres work above.
