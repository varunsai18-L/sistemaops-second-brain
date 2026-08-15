---
id: odoo-task-459
type: Project Task
project: "odysseus"
stage: "Brainstorm"
assignees: "Neha Sharma"
last_updated: 2026-06-13 07:02:22
sync_date: 2026-08-15 21:08:36
tags:
  - odoo/task
  - project/odysseus
  - status/brainstorm
---
# Task: set up the environment for the Odysseus while downloading the dependencies

- **Project:** [[odysseus]]
- **Odoo Stage:** Brainstorm
- **Assignees:** Neha Sharma
- **Last Sync:** 2026-08-15 21:08:36

## Description
Step 1 -- Create & activate virtual environment run these commands in GitBash one by one 1.python -m venv venv2.venv\Scripts\activateWhat it does: Creates an isolated Python environment so packages don't clash with your system Python. You'll see (venv) in your terminal when it's active.Step 2 --Installing dependencies3. pip install -r requirements.txtWhat it does: Installs all Python packages Odysseus needs.Step 3 — Run first-time setup4. python setup.pyWhat it does: Creates the database, generates the admin password, seeds initial config. Run this only once.Step 4 — Set up .env5. copy.env.example .env 6. notepad .envAdd/edit these two lines in the file:envAPP_HOST=127.0.0.1
APP_PORT=7000Save and close Notepad.Step 5 — Start the app7. python -m uvicorn app:app --host 127.0.0.1 --port 7000What it does: Starts Odysseus at http://127.0.0.1:7000. Open that in your browser.
