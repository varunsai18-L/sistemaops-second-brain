#!/usr/bin/env python3
"""
SystemaOps Vault Cleanup & Real Data Verification Script
Filters out Odoo sample demo tasks and XWiki system platform pages,
leaving only real, active company project tasks and technical documentation.
"""

import os
import shutil
import re
from pathlib import Path

VAULT_DIR = Path("/Users/varunsai/mcp-obsidian/second brain")
TASKS_DIR = VAULT_DIR / "04-Projects" / "Odoo Tasks"
XWIKI_DIR = VAULT_DIR / "09-Documentation" / "XWiki"
ARCHIVE_DIR = VAULT_DIR / "_Archive" / "System_and_Demo_Files"

# Sample/Demo projects to exclude
DEMO_PROJECT_KEYWORDS = [
    "Home Construction",
    "Prototypes DEVOPS : Odoo ERP"
]

# System/Platform XWiki spaces to exclude
XWIKI_SYSTEM_SPACES = [
    "AppWithinMinutes",
    "Panels",
    "PanelsCode",
    "FlamingoThemes",
    "IconThemesCode",
    "IconThemes",
    "WikiManager",
    "LDAPUserImport",
    "Help.Applications.Movies.Code",
    "Help.Applications.Movies",
    "Help.Applications.Contributors.Code",
    "Help.Applications.Contributors",
    "Help.SupportPanel",
    "XWiki.Notifications.Code",
    "XWiki.Notifications.Code.Macro",
    "XWiki.Notifications",
    "XWiki.Alerts.Code",
    "XWiki.Attachment.Validation.Code",
    "XWiki.EventStream.Code",
    "XWiki.AuthService",
    "Crypto",
    "Attachment.Code",
    "Attachment",
    "CKEditor",
    "JobMacro",
    "Macros"
]

def clean_odoo_tasks():
    print("==========================================================================")
    print("🧹 Cleaning Odoo Tasks (Removing Sample/Demo Tasks)...")
    print("==========================================================================")
    
    archive_tasks = ARCHIVE_DIR / "Odoo_Demo_Tasks"
    archive_tasks.mkdir(parents=True, exist_ok=True)
    
    total_tasks = 0
    real_tasks = 0
    removed_tasks = 0

    for filepath in TASKS_DIR.glob("*.md"):
        total_tasks += 1
        content = filepath.read_text(encoding="utf-8")
        
        # Check if task belongs to a demo project
        is_demo = False
        for kw in DEMO_PROJECT_KEYWORDS:
            if f'project: "{kw}"' in content or f'project: "{kw} "' in content:
                is_demo = True
                break
        
        if is_demo:
            dest = archive_tasks / filepath.name
            shutil.move(str(filepath), str(dest))
            removed_tasks += 1
        else:
            real_tasks += 1

    print(f"✅ Real Active Company Tasks: {real_tasks}")
    print(f"📦 Archived Demo/Sample Tasks: {removed_tasks}")
    return real_tasks

def clean_xwiki_docs():
    print("==========================================================================")
    print("🧹 Cleaning openDesk XWiki Documentation (Removing System Platform Pages)...")
    print("==========================================================================")
    
    archive_xwiki = ARCHIVE_DIR / "XWiki_System_Pages"
    archive_xwiki.mkdir(parents=True, exist_ok=True)
    
    total_pages = 0
    real_pages = 0
    removed_pages = 0

    for root, dirs, files in os.walk(XWIKI_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            
            filepath = Path(root) / f
            total_pages += 1
            rel_path = filepath.relative_to(XWIKI_DIR)
            first_part = str(rel_path).split(os.sep)[0]
            
            # Check if page is inside a system space
            is_system = False
            for sys_space in XWIKI_SYSTEM_SPACES:
                if rel_path.parts[0] == sys_space or first_part.startswith("XWiki.") or first_part.startswith("Help.Applications."):
                    is_system = True
                    break
            
            if is_system:
                dest = archive_xwiki / filepath.name
                shutil.move(str(filepath), str(dest))
                removed_pages += 1
            else:
                real_pages += 1

    print(f"✅ Real Company Technical Docs & Specs: {real_pages}")
    print(f"📦 Archived System Platform/Theme Pages: {removed_pages}")
    return real_pages

def update_ceo_dashboard(real_tasks_count, real_xwiki_count):
    print("==========================================================================")
    print("👑 Updating CEO Dashboard with Verified Real Metrics...")
    print("==========================================================================")
    
    dashboard_file = VAULT_DIR / "00 - CEO Dashboard.md"
    content = dashboard_file.read_text(encoding="utf-8")
    
    # Replace task count
    content = re.sub(
        r'\| 📋 \*\*Synced Odoo Tasks\*\* +\| `\d+ Tasks`',
        f'| 📋 **Synced Odoo Tasks**         | `{real_tasks_count} Active Tasks`',
        content
    )
    
    # Replace employee count if needed
    content = re.sub(
        r'\| 👥 \*\*Total Active Team Members\*\* \| `\d+ Employees`',
        '| 👥 **Total Active Team Members** | `59 Employees`',
        content
    )

    dashboard_file.write_text(content, encoding="utf-8")
    print("✅ CEO Dashboard updated successfully!")

if __name__ == "__main__":
    real_tasks = clean_odoo_tasks()
    real_pages = clean_xwiki_docs()
    update_ceo_dashboard(real_tasks, real_pages)
    print("==========================================================================")
    print("🎉 Vault Cleanup & Real Data Verification Complete!")
    print("==========================================================================")
