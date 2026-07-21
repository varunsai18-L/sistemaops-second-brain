# Obsidian Vault Automation Scripts

This folder contains synchronization tools to bring company data into your Obsidian Vault:
1. **`sync_odoo.py`**: Syncs Odoo CRM Leads and Project Tasks.
   - Saves Leads to: `06-Clients/Odoo Leads/`
   - Saves Tasks to: `04-Projects/Odoo Tasks/`
2. **`sync_xwiki.py`**: Syncs openDesk XWiki documentation pages (`wiki.systemaops.in`).
   - Saves Wiki Pages to: `09-Documentation/XWiki/`

---

## Setup & Running

### 1. Update Credentials in `.env`
Add your XWiki and Odoo credentials to `.env`:
```text
# Odoo
ODOO_URL=https://odoo.systemaops.com
DB_NAME=systemaops
USER_EMAIL=saivarunrath@gmail.com
API_KEY=your_odoo_developer_api_key

# XWiki
XWIKI_URL=https://wiki.systemaops.in
XWIKI_USER=your_xwiki_username
XWIKI_PASS=your_xwiki_password
```

### 2. Run the Scripts
```bash
cd "/Users/varunsai/mcp-obsidian/second brain/15-Automation"

# Sync Odoo data
python3 sync_odoo.py

# Sync XWiki data
python3 sync_xwiki.py
```
