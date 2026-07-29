---
tags:
  - crm
  - leads
  - pipeline
  - sales
type: Client Pipeline
---

# 🤝 CRM & Client Lead Pipeline Tracker

> **Live Sales Pipeline:** Dataview live tracking of all customer opportunities synced from Odoo CRM.

---

## 📊 Pipeline Overview by Stage (Dataview)

```dataview
TABLE customer AS "Customer", stage AS "Stage", last_updated AS "Last Updated"
FROM "06-Clients/Odoo Leads"
WHERE type = "CRM Lead"
SORT stage ASC, last_updated DESC
```

---

## 🎯 Lead Quick Links

- [[06-Clients/Odoo Leads/|All Odoo CRM Lead Files]]
- [[06-Clients/Client Template|Client Note Template]]
