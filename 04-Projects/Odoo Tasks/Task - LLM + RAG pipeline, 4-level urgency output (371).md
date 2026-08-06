---
id: odoo-task-371
type: Project Task
project: "AI ML review"
stage: "Prototype Development"
assignees: "Chetana Santhi Manapragada"
last_updated: 2026-06-06 15:16:25
sync_date: 2026-08-06 17:50:21
tags:
  - odoo/task
  - status/prototype-development
---
# Task: LLM + RAG pipeline, 4-level urgency output

- **Project:** [[AI ML review]]
- **Odoo Stage:** Prototype Development
- **Assignees:** Chetana Santhi Manapragada
- **Last Sync:** 2026-08-06 17:50:21

## Description
Completed (Prototype Development)Designed and implemented the full backend pipeline end-to-end:Project structure&nbsp;— modular Python packages:&nbsp;api/,&nbsp;rag/,&nbsp;triage/,&nbsp;knowledge_base/Knowledge base&nbsp;— 10 clinical triage guideline documents covering cardiovascular, respiratory, neurological, GI, sepsis, trauma, allergy, pediatric, and mental health protocolsRAG pipeline&nbsp;—&nbsp;BM25 keyword retriever built from 10 clinical guideline documents; no ML dependencies requiredTriage chain&nbsp;—&nbsp;LangChain retriever injects top-4 relevant guidelines into a structured prompt; NVIDIA Nemotron 3 Nano Omni via OpenRouter returns JSON with urgency level, clinical reasoning, next steps, and red-flag symptomsFastAPI app&nbsp;—&nbsp;POST /triage,&nbsp;GET /health,&nbsp;POST /admin/rebuild-index&nbsp;with Pydantic request/response validation, CORS middleware, and lifespan managementSafety&nbsp;— mandatory disclaimer on every response; conservative escalation rule (in doubt, escalate); admin endpoint protected by API keyOutput: 4-level urgency classification — self_care, doctor_consultation, urgent_care, emergency_referralStack:&nbsp;Python · FastAPI · LangChain · BM25 · NVIDIA Nemotron 3 Nano Omni (OpenRouter)

---
**Project Hub:** [[04-Projects/rfq-knowledge/00 - RFQ Project Knowledge Base Index]]
