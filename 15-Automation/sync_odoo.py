import os
import re
import xmlrpc.client
from datetime import datetime
from dotenv import load_dotenv

# Get the vault root directory (one level up from this script in 15-Automation)
VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load configuration from a .env file located in the same directory as the script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

ODOO_URL = os.getenv("ODOO_URL")
DB_NAME = os.getenv("DB_NAME")
USER_EMAIL = os.getenv("USER_EMAIL")
API_KEY = os.getenv("API_KEY")

# Allow override in .env, otherwise default to the detected vault root
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH", VAULT_ROOT)

def validate_config():
    missing = []
    for var, val in [
        ("ODOO_URL", ODOO_URL),
        ("DB_NAME", DB_NAME),
        ("USER_EMAIL", USER_EMAIL),
        ("API_KEY", API_KEY)
    ]:
        if not val:
            missing.append(var)
    if missing:
        print(f"Error: Missing environment variables in .env: {', '.join(missing)}")
        print("Please configure them in the .env file in the 15-Automation folder.")
        return False
    return True

def safe_filename(name):
    # Strip characters that are invalid in filenames
    invalid_chars = '<>:"/\\|?*'
    clean_name = ''.join(c for c in name if c not in invalid_chars)
    return clean_name.strip()

def strip_html(text):
    """Remove HTML tags and decode basic entities for clean Obsidian markdown."""
    if not text:
        return "No description provided."
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>') \
                 .replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'")
    # Collapse excessive whitespace/newlines
    clean = re.sub(r'\n{3,}', '\n\n', clean.strip())
    return clean or "No description provided."

def sync_crm_leads(models, uid):
    print("Syncing CRM Leads from Odoo...")
    # Place Odoo leads in the 06-Clients folder
    leads_folder = os.path.join(VAULT_PATH, "06-Clients", "Odoo Leads")
    os.makedirs(leads_folder, exist_ok=True)
    
    # Filter active leads (opportunities)
    domain = [('type', '=', 'opportunity'), ('active', '=', True)]
    fields = ['name', 'partner_id', 'description', 'stage_id', 'write_date']
    
    try:
        leads = models.execute_kw(
            DB_NAME, uid, API_KEY, 
            'crm.lead', 'search_read', 
            [domain], {'fields': fields}
        )
    except Exception as e:
        print(f"Failed to fetch CRM leads: {e}")
        return

    synced_count = 0
    for lead in leads:
        lead_id = lead['id']
        title = safe_filename(lead['name'])
        stage = lead['stage_id'][1] if lead['stage_id'] else "None"
        customer = lead['partner_id'][1] if lead['partner_id'] else "Unknown"
        description = strip_html(lead['description'])
        last_updated = lead['write_date']

        # Format as clean Obsidian Markdown with frontmatter tags
        md_content = f"""---
id: odoo-lead-{lead_id}
type: CRM Lead
customer: "{customer}"
stage: "{stage}"
last_updated: {last_updated}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - odoo/lead
  - status/{stage.lower().replace(" ", "-")}
---
# Lead: {title}

- **Customer:** [[{customer}]]
- **Odoo Stage:** {stage}
- **Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Details
{description}
"""
        filename = f"Lead - {title} ({lead_id}).md"
        file_path = os.path.join(leads_folder, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        synced_count += 1
        
    print(f"Synced {synced_count} CRM Leads to 06-Clients/Odoo Leads/")

def sync_project_tasks(models, uid):
    print("Syncing Project Tasks from Odoo...")
    # Place Odoo tasks in the 04-Projects folder
    tasks_folder = os.path.join(VAULT_PATH, "04-Projects", "Odoo Tasks")
    os.makedirs(tasks_folder, exist_ok=True)
    
    # Filter active tasks
    domain = [('active', '=', True)]
    fields = ['name', 'project_id', 'description', 'stage_id', 'write_date', 'user_ids']
    
    try:
        tasks = models.execute_kw(
            DB_NAME, uid, API_KEY, 
            'project.task', 'search_read', 
            [domain], {'fields': fields}
        )
    except Exception as e:
        print(f"Failed to fetch Project Tasks: {e}")
        return

    synced_count = 0
    for task in tasks:
        task_id = task['id']
        title = safe_filename(task['name'])
        project = task['project_id'][1] if task['project_id'] else "No Project"
        stage = task['stage_id'][1] if task['stage_id'] else "None"
        # user_ids is a list of integer record IDs — convert to strings before joining
        assignees = ", ".join(str(uid_) for uid_ in task['user_ids']) if task.get('user_ids') else "Unassigned"
        description = strip_html(task['description'])
        last_updated = task['write_date']

        # Format as clean Obsidian Markdown
        md_content = f"""---
id: odoo-task-{task_id}
type: Project Task
project: "{project}"
stage: "{stage}"
assignees: "{assignees}"
last_updated: {last_updated}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - odoo/task
  - project/{project.lower().replace(" ", "-")}
  - status/{stage.lower().replace(" ", "-")}
---
# Task: {title}

- **Project:** [[{project}]]
- **Odoo Stage:** {stage}
- **Assignees:** {assignees}
- **Last Sync:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Description
{description}
"""
        filename = f"Task - {title} ({task_id}).md"
        file_path = os.path.join(tasks_folder, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        synced_count += 1
        
    print(f"Synced {synced_count} Project Tasks to 04-Projects/Odoo Tasks/")

def main():
    if not validate_config():
        return

    print("Connecting to Odoo...")
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        
        # Try to get server version first (doesn't need DB name)
        try:
            version = common.version()
            print(f"Odoo server reachable: {version.get('server_version', 'unknown')}")
        except Exception:
            pass
        
        uid = common.authenticate(DB_NAME, USER_EMAIL, API_KEY, {})
        if not uid:
            print("\n❌ Authentication failed!")
            print("Possible causes:")
            print("  1. Wrong DB_NAME in .env — check with your Odoo admin for the exact database name")
            print("  2. Wrong USER_EMAIL or API_KEY")
            print(f"  Current DB_NAME = '{DB_NAME}'")
            return
        
        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        print(f"✅ Authenticated successfully as UID: {uid}")
        
        sync_crm_leads(models, uid)
        sync_project_tasks(models, uid)
        print("\n✅ Sync complete!")
        
    except Exception as e:
        err = str(e)
        if "does not exist" in err or "Database not found" in err or "AccessError" in err:
            print(f"\n❌ Database '{DB_NAME}' not found on the Odoo server.")
            print("Fix: Update DB_NAME in .env with the correct database name.")
            print("Tip: Ask your Odoo admin or check the Odoo server config for the DB name.")
        else:
            print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
