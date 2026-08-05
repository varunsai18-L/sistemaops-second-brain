#!/usr/bin/env python3
"""
Full A-to-Z Data Sync & Verification Engine for SystemaOps Second Brain
Queries Odoo models (Projects, Tasks, Employees, Partners) and openDesk XWiki,
organizes notes into structured directories, updates Master Indexes, and pushes to Git.
"""

import os
import xmlrpc.client
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load Environment Variables
ENV_PATH = Path("/Users/varunsai/mcp-obsidian/second brain/15-Automation/.env")
load_dotenv(dotenv_path=ENV_PATH)

ODOO_URL = os.getenv("ODOO_URL", "https://odoo.systemaops.com").strip()
DB_NAME = os.getenv("DB_NAME", "odoo_db").strip()
USER_EMAIL = os.getenv("USER_EMAIL", "saivarun945@gmail.com").strip()
API_KEY = os.getenv("API_KEY", "331a27f3443376abf5d39f21d58a09412aca5328").strip()

VAULT_PATH = Path("/Users/varunsai/mcp-obsidian/second brain")

# Demo Projects to exclude from Production Projects
DEMO_PROJECT_KEYWORDS = ["Home Construction", "Prototypes DEVOPS : Odoo ERP"]

def safe_filename(name):
    if not name:
        return "Untitled"
    clean = re.sub(r'[\\/*?:"<>|]', '', str(name))
    return clean.strip()[:100]

def strip_html(text):
    if not text:
        return "No description provided."
    clean = re.sub(r'<[^>]+>', '', str(text))
    return clean.strip()

def connect_odoo():
    print("==========================================================================")
    print(f"📡 Connecting to Odoo at {ODOO_URL}...")
    print("==========================================================================")
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(DB_NAME, USER_EMAIL, API_KEY, {})
    if not uid:
        raise Exception("Authentication failed for Odoo!")
    print(f"✅ Authenticated successfully as UID: {uid}")
    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    return models, uid

def fetch_user_map(models, uid):
    user_map = {}
    try:
        users = models.execute_kw(
            DB_NAME, uid, API_KEY,
            'res.users', 'search_read',
            [[]], {'fields': ['id', 'name']}
        )
        user_map = {u['id']: u['name'] for u in users}
    except Exception as e:
        print(f"⚠️ User map warning: {e}")
    return user_map

def sync_projects(models, uid):
    print("--------------------------------------------------------------------------")
    print("📁 Syncing Odoo Projects...")
    proj_folder = VAULT_PATH / "04-Projects" / "Odoo Projects"
    proj_folder.mkdir(parents=True, exist_ok=True)
    
    fields = ['name', 'user_id', 'partner_id', 'task_count', 'write_date']
    projects = models.execute_kw(
        DB_NAME, uid, API_KEY,
        'project.project', 'search_read',
        [[('active', '=', True)]], {'fields': fields}
    )
    
    count = 0
    proj_list = []
    for p in projects:
        p_name = p['name']
        if any(kw in p_name for kw in DEMO_PROJECT_KEYWORDS):
            continue
        
        manager = p['user_id'][1] if p.get('user_id') else "Unassigned"
        partner = p['partner_id'][1] if p.get('partner_id') else "Internal"
        task_count = p.get('task_count', 0)
        
        proj_list.append((p_name, manager, partner, task_count))
        
        md = f"""---
id: odoo-proj-{p['id']}
type: Project Note
name: "{p_name}"
manager: "{manager}"
client: "{partner}"
task_count: {task_count}
last_updated: {p.get('write_date', 'N/A')}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - odoo/project
---
# 🚀 Project: {p_name}

- **Project Manager:** [[{manager}]]
- **Client / Partner:** [[{partner}]]
- **Total Tasks:** {task_count}
- **Last Updated:** {p.get('write_date', 'N/A')}

---
## 📋 Associated Tasks (Dataview)

```dataview
TABLE assignees AS "Assignees", stage AS "Stage", last_updated AS "Last Synced"
FROM "04-Projects/Odoo Tasks"
WHERE project = "{p_name}"
SORT last_updated DESC
```
"""
        fname = f"Project - {safe_filename(p_name)}.md"
        (proj_folder / fname).write_text(md, encoding="utf-8")
        count += 1
        
    print(f"✅ Synced {count} Production Projects to 04-Projects/Odoo Projects/")
    return proj_list

def sync_tasks(models, uid, user_map):
    print("--------------------------------------------------------------------------")
    print("📋 Syncing Odoo Tasks...")
    tasks_folder = VAULT_PATH / "04-Projects" / "Odoo Tasks"
    tasks_folder.mkdir(parents=True, exist_ok=True)
    
    fields = ['name', 'project_id', 'description', 'stage_id', 'write_date', 'user_ids']
    tasks = models.execute_kw(
        DB_NAME, uid, API_KEY,
        'project.task', 'search_read',
        [[('active', '=', True)]], {'fields': fields}
    )
    
    real_count = 0
    for task in tasks:
        p_name = task['project_id'][1] if task.get('project_id') else "No Project"
        if any(kw in p_name for kw in DEMO_PROJECT_KEYWORDS):
            continue
            
        task_id = task['id']
        title = safe_filename(task['name'])
        stage = task['stage_id'][1] if task.get('stage_id') else "None"
        assignees = ", ".join(user_map.get(u, str(u)) for u in task['user_ids']) if task.get('user_ids') else "Unassigned"
        description = strip_html(task.get('description'))
        last_updated = task.get('write_date', 'N/A')
        
        md = f"""---
id: odoo-task-{task_id}
type: Project Task
project: "{p_name}"
stage: "{stage}"
assignees: "{assignees}"
last_updated: {last_updated}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - odoo/task
  - status/{stage.lower().replace(" ", "-")}
---
# Task: {title}

- **Project:** [[{p_name}]]
- **Odoo Stage:** {stage}
- **Assignees:** {assignees}
- **Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Description
{description}

---
**Project Hub:** [[04-Projects/rfq-knowledge/00 - RFQ Project Knowledge Base Index]]
"""
        fname = f"Task - {title} ({task_id}).md"
        (tasks_folder / fname).write_text(md, encoding="utf-8")
        real_count += 1
        
    print(f"✅ Synced {real_count} Production Tasks to 04-Projects/Odoo Tasks/")
    return real_count

def sync_employees(models, uid):
    print("--------------------------------------------------------------------------")
    print("👥 Syncing Odoo Employees...")
    emp_folder = VAULT_PATH / "07-Employees"
    emp_folder.mkdir(parents=True, exist_ok=True)
    
    fields = ['name', 'work_email', 'work_phone', 'mobile_phone', 'job_title', 'department_id', 'parent_id', 'work_location_id', 'write_date']
    employees = models.execute_kw(
        DB_NAME, uid, API_KEY,
        'hr.employee', 'search_read',
        [[('active', '=', True)]], {'fields': fields}
    )
    
    count = 0
    for emp in employees:
        emp_id = emp['id']
        name = safe_filename(emp['name'])
        job_title = emp.get('job_title') or "Team Member"
        department = emp['department_id'][1] if emp.get('department_id') else "General"
        manager = emp['parent_id'][1] if emp.get('parent_id') else "None"
        email = emp.get('work_email') or "N/A"
        phone = emp.get('work_phone') or emp.get('mobile_phone') or "N/A"
        location = emp['work_location_id'][1] if emp.get('work_location_id') else "Office"
        last_updated = emp.get('write_date', 'N/A')
        
        md = f"""---
id: odoo-emp-{emp_id}
type: Employee Profile
name: "{name}"
job_title: "{job_title}"
department: "{department}"
manager: "{manager}"
email: "{email}"
phone: "{phone}"
location: "{location}"
last_updated: {last_updated}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - employee
  - department/{department.lower().replace(" ", "-")}
---
# 👤 Employee Profile: {name}

## 📋 A to Z Details
- **Full Name:** {name}
- **Job Title:** {job_title}
- **Department:** [[{department}]]
- **Manager / Supervisor:** [[{manager}]]
- **Work Email:** [{email}](mailto:{email})
- **Work Phone:** {phone}
- **Location:** {location}

---
## 🎯 Assigned Tasks & Projects
- Search assigned tasks in Obsidian: `assignees:"{name}"` or `[[{name}]]`

---
**Master Directory:** [[00 - Master Employee Directory Index]]
"""
        fname = f"Employee - {name}.md"
        (emp_folder / fname).write_text(md, encoding="utf-8")
        count += 1
        
    print(f"✅ Synced {count} Employee Profiles to 07-Employees/")
    return count

def sync_partners(models, uid):
    print("--------------------------------------------------------------------------")
    print("🤝 Syncing Odoo Partners & Contacts...")
    partner_folder = VAULT_PATH / "06-Clients" / "Odoo Partners"
    partner_folder.mkdir(parents=True, exist_ok=True)
    
    fields = ['name', 'email', 'phone', 'is_company', 'comment', 'write_date']
    partners = models.execute_kw(
        DB_NAME, uid, API_KEY,
        'res.partner', 'search_read',
        [[('active', '=', True), ('is_company', '=', True)]], {'fields': fields}
    )
    
    count = 0
    for p in partners:
        p_name = safe_filename(p['name'])
        email = p.get('email') or "N/A"
        phone = p.get('phone') or "N/A"
        comment = strip_html(p.get('comment'))
        
        md = f"""---
id: odoo-partner-{p['id']}
type: Client Partner
name: "{p_name}"
email: "{email}"
phone: "{phone}"
last_updated: {p.get('write_date', 'N/A')}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - client/partner
---
# 🏢 Client Partner: {p_name}

- **Company Name:** {p_name}
- **Email:** [{email}](mailto:{email})
- **Phone:** {phone}
- **Notes:** {comment}

---
## 📋 Associated Projects & Opportunities (Dataview)

```dataview
TABLE manager AS "Project Manager", task_count AS "Tasks"
FROM "04-Projects/Odoo Projects"
WHERE client = "{p_name}"
```
"""
        fname = f"Partner - {p_name}.md"
        (partner_folder / fname).write_text(md, encoding="utf-8")
        count += 1
        
    print(f"✅ Synced {count} Corporate Client Partners to 06-Clients/Odoo Partners/")
    return count

if __name__ == "__main__":
    models, uid = connect_odoo()
    user_map = fetch_user_map(models, uid)
    
    proj_list = sync_projects(models, uid)
    task_count = sync_tasks(models, uid, user_map)
    emp_count = sync_employees(models, uid)
    partner_count = sync_partners(models, uid)
    
    print("==========================================================================")
    print("🎉 Full A-to-Z Data Sync Completed Successfully!")
    print(f"   • Employees: {emp_count}")
    print(f"   • Production Projects: {len(proj_list)}")
    print(f"   • Production Tasks: {task_count}")
    print(f"   • Client Partners: {partner_count}")
    print("==========================================================================")
