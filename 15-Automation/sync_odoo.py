import os
import re
import json
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
    invalid_chars = '<>:"/\\|?*'
    clean_name = ''.join(c for c in name if c not in invalid_chars)
    return clean_name.strip()

def strip_html(text):
    if not text:
        return "No description provided."
    clean = re.sub(r'<[^>]+>', '', text)
    clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>') \
                 .replace('&nbsp;', ' ').replace('&quot;', '"').replace('&#39;', "'")
    clean = re.sub(r'\n{3,}', '\n\n', clean.strip())
    return clean or "No description provided."

def sync_crm_leads(models, uid):
    print("Syncing CRM Leads from Odoo...")
    leads_folder = os.path.join(VAULT_PATH, "06-Clients", "Odoo Leads")
    os.makedirs(leads_folder, exist_ok=True)
    
    domain = [('type', '=', 'opportunity'), ('active', '=', True)]
    fields = ['name', 'partner_id', 'description', 'stage_id', 'write_date']
    
    try:
        leads = models.execute_kw(
            DB_NAME, uid, API_KEY, 
            'crm.lead', 'search_read', 
            [domain], {'fields': fields}
        )
    except xmlrpc.client.Fault as e:
        if "You are not allowed to access" in str(e):
            print(f"⚠️  No access to crm.lead ({e.faultString[:60]}...). Falling back to res.partner.")
            return sync_partners(models, uid)
        print(f"Failed to fetch CRM leads: {e}")
        return
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
        
    cleanup_stale_files(leads_folder, [f"Lead - {safe_filename(l['name'])} ({l['id']}).md" for l in leads])
    print(f"Synced {synced_count} CRM Leads to 06-Clients/Odoo Leads/")
    return synced_count


def sync_partners(models, uid):
    """Sync companies from res.partner (accessible to this user)."""
    print("Syncing Client Partners (res.partner) from Odoo...")
    partners_folder = os.path.join(VAULT_PATH, "06-Clients", "Odoo Partners")
    os.makedirs(partners_folder, exist_ok=True)
    
    domain = [('is_company', '=', True), ('active', '=', True)]
    fields = ['name', 'email', 'phone', 'website', 'write_date']
    
    try:
        partners = models.execute_kw(
            DB_NAME, uid, API_KEY,
            'res.partner', 'search_read',
            [domain], {'fields': fields}
        )
    except Exception as e:
        print(f"Failed to fetch partners: {e}")
        return 0

    synced_count = 0
    for partner in partners:
        pid = partner['id']
        name = safe_filename(partner['name'])
        email = partner.get('email') or "N/A"
        phone = partner.get('phone') or "N/A"
        website = partner.get('website') or ""
        last_updated = partner.get('write_date') or "N/A"

        md_content = f"""---
id: odoo-partner-{pid}
type: Client Partner
name: "{name}"
email: "{email}"
phone: "{phone}"
last_updated: {last_updated}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - client/partner
---
# 🏢 Client Partner: {name}

- **Company Name:** {name}
- **Email:** [{email}](mailto:{email})
- **Phone:** {phone}
- **Website:** {website}
- **Notes:** No description provided.

---
## 📋 Associated Projects & Opportunities (Dataview)

```dataview
TABLE manager AS "Project Manager", task_count AS "Tasks"
FROM "04-Projects/Odoo Projects"
WHERE client = "{name}"
```
"""
        filename = f"Partner - {name} ({pid}).md"
        file_path = os.path.join(partners_folder, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        synced_count += 1

    cleanup_stale_files(partners_folder, [f"Partner - {safe_filename(p['name'])} ({p['id']}).md" for p in partners])
    print(f"Synced {synced_count} Client Partners to 06-Clients/Odoo Partners/")
    return synced_count

def sync_project_tasks(models, uid):
    print("Syncing Project Tasks from Odoo...")
    tasks_folder = os.path.join(VAULT_PATH, "04-Projects", "Odoo Tasks")
    os.makedirs(tasks_folder, exist_ok=True)
    
    # Build User ID -> Name Mapping
    user_map = {}
    try:
        users = models.execute_kw(
            DB_NAME, uid, API_KEY,
            'res.users', 'search_read',
            [[]], {'fields': ['id', 'name']}
        )
        user_map = {u['id']: u['name'] for u in users}
    except Exception as e:
        print(f"User mapping warning: {e}")

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
        assignees = ", ".join(user_map.get(uid_, str(uid_)) for uid_ in task['user_ids']) if task.get('user_ids') else "Unassigned"
        description = strip_html(task['description'])
        last_updated = task['write_date']

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
        
    cleanup_stale_files(tasks_folder, [f"Task - {safe_filename(t['name'])} ({t['id']}).md" for t in tasks])
    print(f"Synced {synced_count} Project Tasks to 04-Projects/Odoo Tasks/")

def read_existing_employee_data(emp_folder, name):
    """Read capacity/cert data from an existing vault file so values aren't
    lost when the Odoo DB no longer exposes the custom fields."""
    cap = None
    certs = None
    file_path = os.path.join(emp_folder, f"Employee - {name}.md")
    if not os.path.exists(file_path):
        return None, None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        m = re.search(r'capacity_utilization:\s*([0-9.]+)', content)
        if m:
            cap = float(m.group(1))
        m = re.search(r'##\s*🎯?\s*Certifications\s*\n(.*?)(?:\n##\s*|\n---|\Z)', content, re.DOTALL)
        if m:
            certs = [c.strip().lstrip('- ').strip() for c in m.group(1).splitlines() if c.strip()]
            certs = [c for c in certs if c and c.lower() != 'no certifications listed']
    except Exception:
        pass
    return cap, certs


def sync_employees(models, uid):
    print("Syncing Employee Directory from Odoo...")
    emp_folder = os.path.join(VAULT_PATH, "07-Employees")
    os.makedirs(emp_folder, exist_ok=True)
    
    # Discover which fields actually exist on hr.employee in this DB
    try:
        existing_fields = models.execute_kw(
            DB_NAME, uid, API_KEY,
            'hr.employee', 'fields_get', [],
            {'attributes': ['type']}
        )
    except Exception as e:
        print(f"Failed to introspect hr.employee fields: {e}")
        return {"emp_id_mapping": {}, "employee_count": 0}

    def pick(*names):
        return [f for f in names if f in existing_fields]

    domain = [('active', '=', True)]
    fields = pick('name', 'work_email', 'work_phone', 'mobile_phone', 'job_title',
                  'department_id', 'parent_id', 'work_location_id', 'write_date',
                  'capacity_percentage', 'cert_ids', 'skill_ids', 'employee_skill_ids')
    
    try:
        employees = models.execute_kw(
            DB_NAME, uid, API_KEY, 
            'hr.employee', 'search_read', 
            [domain], {'fields': fields}
        )
    except Exception as e:
        print(f"Failed to fetch Employees: {e}")
        return {"emp_id_mapping": {}, "employee_count": 0}

    synced_count = 0
    emp_list = []
    emp_id_mapping = {}  # Odoo employee ID -> internal mapping
    
    for emp in employees:
        emp_id = emp['id']
        odoo_id = str(emp_id)  # Original Odoo ID
        name = safe_filename(emp['name'])
        job_title = emp['job_title'] or "Team Member"
        department = emp['department_id'][1] if emp.get('department_id') else "General"
        manager = emp['parent_id'][1] if emp.get('parent_id') else "None"
        email = emp.get('work_email') or "N/A"
        phone = emp.get('work_phone') or emp.get('mobile_phone') or "N/A"
        location = emp['work_location_id'][1] if emp.get('work_location_id') else "Office"
        capacity_utilization = emp.get('capacity_percentage') or 0
        last_updated = emp.get('write_date', 'N/A')

        # Employee ID Mapping: Odoo ID -> Internal Mapping
        emp_id_mapping[odoo_id] = {
            "odoo_id": odoo_id,
            "internal_id": f"internal_{emp_id}",
            "name": name
        }
        
        # Extract certifications from available relationship fields
        certifications = []
        if 'cert_ids' in emp and emp.get('cert_ids'):
            for cert_ref in emp['cert_ids']:
                if isinstance(cert_ref, (list, tuple)):
                    cert_name = cert_ref[1] if len(cert_ref) > 1 else str(cert_ref[0])
                else:
                    cert_name = str(cert_ref)
                certifications.append(cert_name)
        elif 'skill_ids' in emp and emp.get('skill_ids'):
            for skill_ref in emp['skill_ids']:
                if isinstance(skill_ref, (list, tuple)):
                    skill_name = skill_ref[1] if len(skill_ref) > 1 else str(skill_ref[0])
                else:
                    skill_name = str(skill_ref)
                certifications.append(skill_name)

        # If the Odoo DB no longer provides capacity/cert fields, preserve the
        # last known values from the existing vault file instead of wiping them.
        if not capacity_utilization and not certifications:
            saved_cap, saved_certs = read_existing_employee_data(emp_folder, name)
            if saved_cap is not None:
                capacity_utilization = saved_cap
            if saved_certs:
                certifications = saved_certs
        
        emp_list.append({
            "odoo_id": odoo_id,
            "internal_id": f"internal_{emp_id}",
            "name": name,
            "job_title": job_title,
            "department": department,
            "email": email,
            "phone": phone,
            "capacity_utilization": float(capacity_utilization or 0),
            "certifications": certifications
        })

        md_content = f"""---
id: odoo-emp-{emp_id}
type: Employee Profile
name: "{name}"
job_title: "{job_title}"
department: "{department}"
manager: "{manager}"
email: "{email}"
phone: "{phone}"
location: "{location}"
capacity_utilization: {capacity_utilization or 0}
last_updated: {last_updated}
sync_date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
tags:
  - employee
  - department/{department.lower().replace(" ", "-")}
  - capacity/{str(float(capacity_utilization or 0)).replace(".", "-")}
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
- **Capacity Utilization:** {capacity_utilization or 0}%

---
## 🎯 Certifications
{', '.join(certifications) if certifications else 'No certifications listed'}

## 🎯 Assigned Tasks & Projects
- Search assigned tasks in Obsidian: `assignees:"{name}"` or `[[{name}]]`

---
*Synced from Odoo HR Module on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        filename = f"Employee - {name}.md"
        file_path = os.path.join(emp_folder, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        synced_count += 1

    cleanup_stale_files(emp_folder, [f"Employee - {safe_filename(e['name'])}.md" for e in employees])

    # Create Master Index for 1-click access with capacity and cert info
    index_md = f"""---
tags:
  - employee/index
  - directory
type: Master Directory
---

# 📁 Master Employee Directory Index (A to Z)

Click any employee below to view their complete A to Z details:

| Employee Name | Job Title | Department | Capacity | Certifications | Email | Profile Link |
|---|---|---|---|---|---|---|
"""
    for e in sorted(emp_list, key=lambda x: x['name']):
        cert_display = ', '.join(e['certifications'][:3]) + ("..." if len(e['certifications']) > 3 else "")
        index_md += f"| {e['name']} | {e['job_title']} | {e['department']} | {e['capacity_utilization']}% | {cert_display} | {e['email']} | [[Employee - {e['name']}]]|\n"

    index_md += f"\n---\n*Total Active Employees: {synced_count} | Last Synced: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    with open(os.path.join(emp_folder, "00 - Master Employee Directory Index.md"), "w", encoding="utf-8") as f:
        f.write(index_md)

    # Return the ID mapping for use by other modules
    return {"emp_id_mapping": emp_id_mapping, "employee_count": synced_count}

def cleanup_stale_files(folder, current_filenames):
    """Remove generated .md files in folder that are no longer present in Odoo."""
    if not os.path.isdir(folder):
        return
    keep = set(current_filenames)
    removed = 0
    for fname in os.listdir(folder):
        if not fname.endswith(".md"):
            continue
        if fname in keep:
            continue
        path = os.path.join(folder, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                head = f.read(200)
        except Exception:
            continue
        # Only delete files that carry the sync frontmatter marker
        if "id: odoo-" in head:
            os.remove(path)
            removed += 1
    if removed:
        print(f"  Cleaned up {removed} stale file(s) in {os.path.basename(folder)}")

def main():
    if not validate_config():
        return

    print("Connecting to Odoo...")
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        
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
        emp_result = sync_employees(models, uid)
        print("\n✅ Odoo Sync Completed. Review counts above for any warnings.")
        
        # Return the employee ID mapping for API gateway use
        if emp_result and "emp_id_mapping" in emp_result:
            print(f"📋 Employee ID Mapping: {len(emp_result['emp_id_mapping'])} employees mapped")
        
    except Exception as e:
        err = str(e)
        if "does not exist" in err or "Database not found" in err or "AccessError" in err:
            print(f"\n❌ Database '{DB_NAME}' not found on the Odoo server.")
            print("Fix: Update DB_NAME in .env with the correct database name.")
        else:
            print(f"\n❌ An error occurred: {e}")

def get_employee_capacity_cert_data() -> dict:
    """Extract employee capacity and certification data from the synced Obsidian vault.
    
    This function reads the synced employee markdown files and returns structured data
    for the Integrated API Gateway's employee mapping and capacity/certification features.
    
    Returns:
        Dictionary with employee capacity utilization and certifications list.
    """
    emp_folder = os.path.join(VAULT_ROOT, "07-Employees")
    capacity_cert_data = []
    
    if not os.path.exists(emp_folder):
        return {"employees": [], "total": 0}
    
    # Read all employee files and extract capacity/cert info
    for root, _, files in os.walk(emp_folder):
        for file in sorted(files):
            if file.startswith("Employee") and file.endswith(".md"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Extract capacity utilization from frontmatter or A to Z details
                    cap_match = re.search(r'capacity_utilization:\s*([0-9.]+)', content)
                    if not cap_match:
                        cap_match = re.search(r'Capacity Utilization:\s*([0-9.]+)%', content)
                    capacity = float(cap_match.group(1)) if cap_match else 0.0
                    
                    # Extract certifications (emoji or plain header)
                    certs_section = re.search(r'##\s*🎯?\s*Certifications\s*(.*?)(?:\n---\n|\n##\s*|$)', content, re.DOTALL)
                    certs_text = certs_section.group(1).strip() if certs_section else ""
                    certs = [c.strip().lstrip('- ') for c in certs_text.split('\n') if c.strip()]
                    certs = [c for c in certs if c and c.lower() != 'no certifications listed']
                    
                    # Extract employee name: from YAML frontmatter name, then # 👤 Employee Profile: header
                    name = ""
                    fm_match = re.search(r'^name:\s*"([^"]+)"', content, re.MULTILINE)
                    if fm_match:
                        name = fm_match.group(1).strip()
                    if not name:
                        name_match = re.search(r'^#\s*👤?\s*Employee Profile:\s*(.+?)$', content, re.MULTILINE)
                        name = name_match.group(1).strip() if name_match else "Unknown"
                    
                    # Extract job title and department from frontmatter
                    job_title = "Team Member"
                    jt_match = re.search(r'^job_title:\s*"([^"]+)"', content, re.MULTILINE)
                    if jt_match:
                        job_title = jt_match.group(1).strip()
                    department = "General"
                    dept_match = re.search(r'^department:\s*"([^"]+)"', content, re.MULTILINE)
                    if dept_match:
                        department = dept_match.group(1).strip()
                    
                    capacity_cert_data.append({
                        "name": name,
                        "job_title": job_title,
                        "department": department,
                        "capacity_utilization": capacity,
                        "certifications": certs
                    })
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
    
    return {
        "employees": capacity_cert_data,
        "total": len(capacity_cert_data)
    }


def get_employee_id_mapping() -> dict:
    """Return the Odoo employee ID to internal ID mapping from the last sync.
    
    Returns:
        Dictionary mapping Odoo employee IDs to internal mappings.
    """
    mapping_path = os.path.join(VAULT_ROOT, ".last_emp_mapping.json")
    
    if os.path.exists(mapping_path):
        try:
            with open(mapping_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    
    # Fallback: rebuild from the most recent employee files
    return {"employees": [], "total": 0}


def save_employee_id_mapping(mapping: dict):
    """Save the employee ID mapping to disk for future API gateway access."""
    mapping_path = os.path.join(VAULT_ROOT, ".last_emp_mapping.json")
    try:
        with open(mapping_path, "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=2)
        print(f"💾 Employee ID mapping saved to {mapping_path}")
    except Exception as e:
        print(f"Error saving employee mapping: {e}")


if __name__ == "__main__":
    main()
