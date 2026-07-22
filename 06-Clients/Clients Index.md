---
title: Clients Index
created: 2026-07-09
tags: [index, clients]
---

# 👥 Clients Dashboard

Welcome to the **SystemsOps Clients Dashboard**. This folder is the central hub for managing client relationships, CRM leads, and prospect information synced directly from Odoo.

## 🎯 Active CRM Leads

> This table automatically lists all active CRM leads imported from Odoo.

```dataview
TABLE customer AS "Customer", stage AS "Stage", last_updated AS "Last Updated"
FROM "06-Clients/Odoo Leads"
SORT last_updated DESC
```

## 📁 Related Notes
- [[Client Template]]
