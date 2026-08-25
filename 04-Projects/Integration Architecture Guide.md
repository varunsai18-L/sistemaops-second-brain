---
type: Integration Architecture Doc
title: "Second Brain x RFQ Engine — Full Integration Guide"
tags:
  - documentation
  - architecture
  - integration
  - rfq
  - second-brain
sync_date: 2026-08-19
---

# 🔗 Second Brain x RFQ Engine

## Full Integration Architecture Guide

> *How the Obsidian Second Brain connects bi-directionally with the PVMS RFQ Engine — end-to-end, step by step.*

---

## 1. Architecture Overview

```
                          ┌─────────────────────────────┐
                          │   OBSIDIAN SECOND BRAIN     │
                          │   (Single Source of Truth)  │
                          │                             │
                          │  07-Employees/    (55)      │
                          │  09-Documentation/ (359)    │
                          │  04-Projects/      (22)     │
                          │  04-Projects/Odoo Tasks (115)│
                          │  06-Clients/       (47)     │
                          │  04-Projects/RFQ Evaluations │
                          └──────────┬──────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              ▼                      ▼                      ▼
   ┌────────────────┐    ┌──────────────────┐    ┌──────────────────┐
   │  sync_odoo.py   │    │  sync_xwiki.py   │    │ sync_marketing.py │
   │  (Odoo ERP)     │    │ (OpenDesk/XWiki) │    │ (Marketing vault) │
   └────────────────┘    └──────────────────┘    └──────────────────┘
              │                      │                      │
              └──────────┬───────────┘                      │
                         ▼                                  │
              ┌─────────────────────────┐                   │
              │  auto_sync.sh (vault)   │                   │
              │  runs all syncs + git   │                   │
              └──────────┬──────────────┘                   │
                         ▼                                  │
              ┌─────────────────────────┐                   │
              │  PVMS RFQ ENGINE        │◄──────────────────┘
              │  /launch.sh:            │
              │   1. sync_second_brain_ │
              │      to_pvms.py (pull)  │
              │   2. backfill_cloud_rag │
              │      .py (index)        │
              │   3. streamlit app      │
              └─────────────────────────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
      ┌────────────┐ ┌──────────┐ ┌────────────────┐
      │ Local RAG  │ │ Knowledge │ │ RFQ Evaluations│
      │ API :8100  │ │ Graph    │ │ auto-written   │
      │ (persistent)│ │ (nodes)  │ │ back to vault  │
      └────────────┘ └──────────┘ └────────────────┘
```

**Direction of data flow:**
- **Pull (Obsidian → RFQ):** Employees, docs, projects, tasks feed the engine's database, capacity, and knowledge graph
- **Push (RFQ → Obsidian):** Every evaluation result auto-writes a note back into the vault

---

## 2. Components

| # | Component | Role | Location |
|---|---|---|---|
| 1 | Obsidian Second Brain | Single source of truth — markdown vault | `/Users/varunsai/mcp-obsidian/second brain/` |
| 2 | Odoo ERP | Source of employees, partners, tasks, projects | `odoo.systemaops.com` |
| 3 | OpenDesk/XWiki | Source of technical documentation | `wiki.systemaops.in` |
| 4 | PVMS RFQ Engine | AI evaluation engine (Streamlit app) | `/Users/varunsai/Downloads/project-viability-management-system-main/` |
| 5 | Local RAG API | Embedding store + query endpoint (FastAPI) | `http://127.0.0.1:8100` |
| 6 | Ollama | Local LLM + embeddings | `http://127.0.0.1:11434` |

---

## 3. Sync Step-by-Step

### 3.1 Vault Auto-Sync (`15-Automation/auto_sync.sh`)

Runs on demand or scheduled, keeps the vault current with live systems:

| Step | Script | What it does | Writes to |
|---|---|---|---|
| 1 | `sync_odoo.py` | Pulls employees, partners, tasks, projects from Odoo REST API | `07-Employees/`, `06-Clients/`, `04-Projects/` |
| 2 | `sync_xwiki.py` | SSO auth → catalogs 599 pages → dedupes to 360 → downloads | `09-Documentation/XWiki/` |
| 3 | `sync_marketing.py` | Pulls marketing knowledge (personas, frameworks, campaigns) | Marketing pillars |
| 4 | `git commit + push` | Version-controls the whole vault | GitLab + GitHub |

### 3.2 RFQ Engine Startup (`launch.sh`)

Runs automatically every time the app starts:

| Step | Script | What it does |
|---|---|---|
| 1 | `second_brain_api/launch.sh` | Starts local RAG API on port 8100 (persistent JSON storage) |
| 2 | `sync_second_brain_to_pvms.py` | Reads vault: 55 employees → `employee_database.json` + `employee_capacity.json`; 359 XWiki pages → `second_brain_knowledge_index.json`; purges stale employees |
| 3 | `backfill_cloud_rag.py` | Upserts all vault notes into the RAG index (skips existing, idempotent) |
| 4 | `streamlit run app/main.py` | Launches the web app at `http://localhost:8501` |

### 3.3 RFQ Evaluation Flow (in the app)

When a user uploads an RFQ and clicks **Run Viability Analysis**:

| Step | Action | Where |
|---|---|---|
| 1 | Parse the document (PDF/DOCX/TXT) | Parser factory |
| 2 | Multi-agent pipeline (parser, technical, finance, risk, proposal, diagram, reviewer) | `MultiAgentOrchestrator` |
| 3 | Save structured result to `data/outputs/` | `save_rfq_output` |
| 4 | **Auto-write evaluation to vault** | `save_vault_evaluation` → `04-Projects/RFQ Evaluations/RFQ - <Title> (timestamp).md` |
| 5 | Show confirmation in UI: "📝 Saved to Obsidian Second Brain" | Streamlit session state |

### 3.4 Querying Knowledge (Second Brain tab)

| Step | Action | Where |
|---|---|---|
| 1 | User asks a question in plain English | Second Brain tab |
| 2 | Query sent to local RAG API | `POST /api/query` |
| 3 | Embedding similarity search (Ollama nomic-embed-text) | `second_brain_api` |
| 4 | Synthesis generated by local LLM (qwen2.5:3b) | `second_brain_api` |
| 5 | Top matches + answer shown in UI | Streamlit |

---

## 4. Data Mappings

| Vault Location | RFQ Engine Destination | Count |
|---|---|---|
| `07-Employees/Employee - *.md` | `src/pvms/skills/employee_database.json` | 55 |
| `07-Employees/` (capacity frontmatter) | `src/pvms/capacity/employee_capacity.json` | 55 |
| `04-Projects/Odoo Tasks/*.md` | Capacity task-count computation | 115 |
| `09-Documentation/XWiki/*.md` | `data/second_brain_knowledge_index.json` | 359 |
| Knowledge index JSON | Knowledge Graph (Documentation + WikiSpace nodes) | 368+ nodes |
| All of the above | Local RAG API notes store | 558 notes |
| `04-Projects/RFQ Evaluations/` (output) | ← written by `save_vault_evaluation` | 7 |

---

## 5. Key Files

| File | Purpose |
|---|---|
| `15-Automation/auto_sync.sh` | Orchestrates vault syncs + git push |
| `15-Automation/sync_odoo.py` | Odoo → vault pull |
| `15-Automation/sync_xwiki.py` | OpenDesk/XWiki → vault pull |
| `scripts/sync_second_brain_to_pvms.py` | Vault → RFQ engine pull |
| `scripts/backfill_cloud_rag.py` | Vault → RAG index |
| `second_brain_api/app/main.py` | Local RAG API (FastAPI) |
| `src/pvms/repositories/vault_evaluation.py` | RFQ → vault write |
| `src/pvms/knowledge/knowledge_graph.py` | Knowledge graph with doc nodes |
| `src/pvms/knowledge/second_brain_client.py` | App ↔ RAG API client |
| `app/main.py` | Streamlit UI + integration hooks |

---

## 6. Value Summary

1. **Single source of truth** — all company knowledge lives in one searchable vault
2. **Bi-directional** — RFQ results feed back into the knowledge base
3. **Live capacity** — team recommendations use real Odoo task load
4. **Every evaluation is reusable** — past decisions are queryable knowledge
5. **Resilient** — local API with persistent storage, no cloud dependency
6. **Versioned** — the entire vault is backed up to GitLab + GitHub

---

*Documentation generated 2026-08-19 from the live integration implementation.*