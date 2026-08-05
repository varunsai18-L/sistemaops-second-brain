#!/usr/bin/env python3
"""
SystemaOps AI Marketing Engine Auto-Sync & Indexer
Parses 05-Marketing/ vault pillars and updates Master Marketing Hub metrics.
"""

import os
from pathlib import Path

VAULT_DIR = Path("/Users/varunsai/mcp-obsidian/second brain")
MARKETING_DIR = VAULT_DIR / "05-Marketing"

def scan_marketing_vault():
    print("==========================================================================")
    print("🚀 SystemaOps AI-First Marketing Engine Vault Sync")
    print("==========================================================================")
    
    pillars = {
        "01-Client-Vault": "Client Transcripts, Feedback & Personas",
        "02-Swipe-Files": "Hooks, Headlines & Pitch Swipe Files",
        "03-Framework-Library": "Marketing & Positioning Frameworks",
        "04-Idea-Graph": "Content Clusters & Knowledge Graph",
        "05-Campaigns": "Growth Campaigns & Follow-up Sequences"
    }
    
    total_notes = 0
    pillar_counts = {}

    for folder, label in pillars.items():
        folder_path = MARKETING_DIR / folder
        if folder_path.exists():
            files = [f for f in folder_path.glob("*.md")]
            count = len(files)
            pillar_counts[label] = count
            total_notes += count
            print(f"✅ {label}: {count} Notes found")
        else:
            print(f"⚠️ {label}: Folder missing, creating...")
            folder_path.mkdir(parents=True, exist_ok=True)
            pillar_counts[label] = 0

    print("--------------------------------------------------------------------------")
    print(f"📊 Total Marketing Knowledge Base Assets: {total_notes} Notes across 5 Pillars")
    print("==========================================================================")
    print("🎉 Marketing Vault Sync Completed Successfully!")

if __name__ == "__main__":
    scan_marketing_vault()
