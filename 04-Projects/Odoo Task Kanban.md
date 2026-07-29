---
tags:
  - kanban
  - project-tasks
  - odoo
type: Task Board
---

# 📌 Odoo Task Kanban Board

> **Interactive Task Flow:** Live Dataview columns tracking all Odoo tasks across execution stages.

---

## 🏃‍♂️ In Progress

```dataview
TABLE project AS "Project", assignees AS "Assignees", last_updated AS "Last Updated"
FROM "04-Projects/Odoo Tasks"
WHERE stage = "In Progress" OR stage = "In progress"
SORT last_updated DESC
```

---

## 📥 Backlog

```dataview
TABLE project AS "Project", assignees AS "Assignees", last_updated AS "Last Updated"
FROM "04-Projects/Odoo Tasks"
WHERE stage = "Backlog" or stage = "New"
SORT project ASC
```

---

## 🔍 Under Review & Testing

```dataview
TABLE project AS "Project", assignees AS "Assignees", last_updated AS "Last Updated"
FROM "04-Projects/Odoo Tasks"
WHERE stage = "Review" OR stage = "Testing"
SORT last_updated DESC
```

---

## ✅ Done / Completed

```dataview
TABLE project AS "Project", assignees AS "Assignees", last_updated AS "Completed Date"
FROM "04-Projects/Odoo Tasks"
WHERE stage = "Done" OR stage = "Completed"
SORT last_updated DESC
```
