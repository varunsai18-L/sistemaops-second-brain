#!/usr/bin/env python3
"""
Remove Footer Master Links from Individual Notes
Strips added master links from Employee and XWiki notes so green nodes float cleanly around central hubs.
"""

import os
from pathlib import Path

VAULT_DIR = Path("/Users/varunsai/mcp-obsidian/second brain")
EMP_DIR = VAULT_DIR / "07-Employees"
XWIKI_DIR = VAULT_DIR / "09-Documentation" / "XWiki"
TASKS_DIR = VAULT_DIR / "04-Projects" / "Odoo Tasks"

def strip_footer_links(directory, targets):
    if not directory.exists():
        return 0
    cleaned = 0
    for filepath in directory.rglob("*.md"):
        content = filepath.read_text(encoding="utf-8")
        modified = False
        for target in targets:
            if target in content:
                content = content.replace(target, "")
                modified = True
        if modified:
            filepath.write_text(content.strip() + "\n", encoding="utf-8")
            cleaned += 1
    return cleaned

if __name__ == "__main__":
    targets = [
        "\n---\n**Master Directory:** [[00 - Master Employee Directory Index]]\n",
        "**Master Directory:** [[00 - Master Employee Directory Index]]",
        "\n---\n**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]\n",
        "**Knowledge Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]",
        "\n---\n**Project Hub:** [[04-Projects/rfq-knowledge/00 - RFQ Project Knowledge Base Index]]\n",
        "**Project Hub:** [[04-Projects/rfq-knowledge/00 - RFQ Project Knowledge Base Index]]",
        "### 🕸️ Knowledge Graph Connections",
        "- **CEO Command Center:** [[00 - CEO Dashboard]]",
        "- **Master Directory:** [[00 - Master Employee Directory Index]]",
        "- **AI Marketing Engine:** [[05-Marketing/00 - Master Marketing Hub]]",
        "- **RFQ Project Hub:** [[04-Projects/rfq-knowledge/00 - RFQ Project Knowledge Base Index]]",
        "- **openDesk XWiki Index:** [[09-Documentation/XWiki/00 - openDesk XWiki Master Index]]",
        "- **RFQ Tech Specs:** [[04-Projects/rfq-knowledge/00 - RFQ Project Knowledge Base Index]]"
    ]
    
    print("Stripping footer links from Employee, Task, and XWiki notes...")
    c1 = strip_footer_links(EMP_DIR, targets)
    c2 = strip_footer_links(TASKS_DIR, targets)
    c3 = strip_footer_links(XWIKI_DIR, targets)
    print(f"✅ Cleaned {c1} Employee notes, {c2} Task notes, {c3} XWiki notes.")
    print("🎉 Green nodes are now clean & floating freely in Graph View!")
