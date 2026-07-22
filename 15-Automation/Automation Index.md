---
name: Automation Index
description: Main index for all automation workflows and processes
date: 2026-07-10
type: index
tags: [automation, workflow, index]
---

# ⚡ Automation Dashboard

Welcome to the **SystemsOps Automation Hub**. This folder contains scripts and workflows designed to automate repetitive tasks and sync our data across tools.

## 🔄 Sync Scripts

We have two primary Python scripts in this folder that sync our company data directly into this Obsidian Second Brain.

### 1. Odoo Sync (`sync_odoo.py`)
Pulls **Project Tasks** and **CRM Leads** directly from our Odoo ERP.
- **How to run:** Open a terminal in the `15-Automation` folder, activate the `venv`, and run `python sync_odoo.py`.
- **Note:** Ensure your API key is correctly set in the `.env` file.

### 2. XWiki Sync (`sync_xwiki.py`)
Pulls pages from our **openDesk (XWiki)** environment into the `09-Documentation/XWiki/` folder.
- **How to run:** Open a terminal in the `15-Automation` folder, activate the `venv`, and run `python sync_xwiki.py`.

## 📋 Standard Workflows

- [[Workflow Library]]
- [[Daily Workflow]]
- [[Weekly Workflow]]
- [[Monthly Workflow]]
- [[Onboarding Workflow]]
- [[Offboarding Workflow]]
- [[Automation Ideas]]
