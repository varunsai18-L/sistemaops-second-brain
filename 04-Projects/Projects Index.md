---
title: Projects Index
date: 2026-07-09
tags: [index, projects]
---

# 🚀 Projects Dashboard

Welcome to the **SystemsOps Projects Dashboard**. This folder manages all our active projects, internal tasks, and initiatives. The data here is synced directly from our Odoo ERP.

## 📊 Live Projects Overview

> This table automatically pulls all active projects synced from Odoo.

```dataview
TABLE length(file.inlinks) AS "Total Tasks", source AS "Source"
FROM "04-Projects/Odoo Projects"
SORT file.name ASC
```

## 🏃‍♂️ Tasks in Progress (Company-Wide)

```dataview
TABLE project AS "Project", assignees AS "Assignees"
FROM "04-Projects/Odoo Tasks"
WHERE stage = "In Progress" OR stage = "Development"
SORT last_updated DESC
```

## 📁 Related Notes
- [[Project Template]]
