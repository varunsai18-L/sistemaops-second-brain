#!/usr/bin/env python3
"""
Connect Obsidian Graph View Nodes
Adds central hub wikilinks to Employee, Task, and XWiki notes so all nodes connect in Graph View.
"""

import os
from pathlib import Path

VAULT_DIR = Path("/Users/varunsai/mcp-obsidian/second brain")
EMP_DIR = VAULT_DIR / "07-Employees"
TASKS_DIR = VAULT_DIR / "04-Projects" / "Odoo Tasks"
XWIKI_DIR = VAULT_DIR / "09-Documentation" / "XWiki"

def link_employee_notes():
    if not EMP_DIR.exists():
        return
    master_link = "\n---\n**Master Directory:** [[00 - Master Employee Directory Index]]\n"
    count = 0
    for f in EMP_DIR.glob("*.md"):
        if f.name == "00 - Master Employee Directory Index.md":
            continue
        content = f.read_text(encoding="utf-8")
        if "[[00 - Master Employee Directory Index]]" not in content:
            f.write_text(content + master_link, encoding="utf-8")
            count += 1
    print(f"✅ Linked {count} Employee notes to Master Employee Directory Index")

def link_task_notes():
    if not TASKS_DIR.exists():
        return
    master_link = "\n---\n**Project Hub:** [[04-Projects/rfq-knowledge/00 - RFQ Project Knowledge Base Index]]\n"
    count = 0
    for f in TASKS_DIR.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if "00 - RFQ Project Knowledge Base Index" not in content:
            f.write_text(content + master_link, encoding="utf-8")
            count += 1
    print(f"✅ Linked {count} Odoo Task notes to RFQ Project Knowledge Base Index")

def link_xwiki_notes():
    if not XWIKI_DIR.exists():
        return
    master_link = "\n---\n**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]\n"
    count = 0
    for f in XWIKI_DIR.rglob("*.md"):
        if f.name == "00 - openDesk XWiki Master Index.md":
            continue
        content = f.read_text(encoding="utf-8")
        if "00 - openDesk XWiki Master Index" not in content:
            f.write_text(content + master_link, encoding="utf-8")
            count += 1
    print(f"✅ Linked {count} openDesk XWiki technical documentation notes")

if __name__ == "__main__":
    print("Connecting Obsidian Graph View nodes...")
    link_employee_notes()
    link_task_notes()
    link_xwiki_notes()
    print("🎉 All graph nodes linked successfully!")
