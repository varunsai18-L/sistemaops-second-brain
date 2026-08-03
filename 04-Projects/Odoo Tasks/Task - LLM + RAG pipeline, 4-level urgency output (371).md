---
id: odoo-task-371
type: Project Task
project: "AI ML review"
stage: "Prototype Development"
assignees: "65"
last_updated: 2026-06-06 15:16:25
sync_date: 2026-08-03 21:49:02
tags:
  - odoo/task
  - project/ai-ml-review
  - status/prototype-development
---
# Task: LLM + RAG pipeline, 4-level urgency output

- **Project:** [[AI ML review]]
- **Odoo Stage:** Prototype Development
- **Assignees:** 65
- **Last Sync:** 2026-08-03 21:49:02

## Description
Completed (Prototype Development)Designed and implemented the full backend pipeline end-to-end:Project structure — modular Python packages: api/, rag/, triage/, knowledge_base/Knowledge base — 10 clinical triage guideline documents covering cardiovascular, respiratory, neurological, GI, sepsis, trauma, allergy, pediatric, and mental health protocolsRAG pipeline — BM25 keyword retriever built from 10 clinical guideline documents; no ML dependencies requiredTriage chain — LangChain retriever injects top-4 relevant guidelines into a structured prompt; NVIDIA Nemotron 3 Nano Omni via OpenRouter returns JSON with urgency level, clinical reasoning, next steps, and red-flag symptomsFastAPI app — POST /triage, GET /health, POST /admin/rebuild-index with Pydantic request/response validation, CORS middleware, and lifespan managementSafety — mandatory disclaimer on every response; conservative escalation rule (in doubt, escalate); admin endpoint protected by API keyOutput: 4-level urgency classification — self_care, doctor_consultation, urgent_care, emergency_referralStack: Python · FastAPI · LangChain · BM25 · NVIDIA Nemotron 3 Nano Omni (OpenRouter)
