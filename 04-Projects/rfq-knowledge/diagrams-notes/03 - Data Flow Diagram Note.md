---
tags:
  - rfq-project
  - diagram
  - dataflow
  - pvms
project: RFQ Viability Management System
type: Diagram Note
---

# 🔄 Data Flow Diagram Note

## Diagram View
![[dataflow_diagram.png]]

## Description & Pipeline
Illustrates end-to-end data progression from initial RFQ intake through automated assessment to final report export.

### Pipeline Stages:
1. **Ingestion & Parsing:** Extracts text, tables, and metadata from incoming RFQ files.
2. **Module Processing:** Sequential analysis across Technical, Financial, Risk, and Resource feasibility modules.
3. **Synthesis & Storage:** Aggregates module scores into unified project viability metrics.
4. **Export & Handoff:** Formats final outputs into downloadable PDF/Markdown executive summaries.

---
**Related Notes:**
- [[integration_mapping]]
- [[rfq_data_schema]]
- [[report_structure]]
