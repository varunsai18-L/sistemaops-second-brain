#!/bin/zsh

# Auto Sync Script for Systemaops Second Brain (Odoo + OpenDesk -> Obsidian -> GitLab & GitHub)
VAULT_DIR="/Users/varunsai/mcp-obsidian/second brain"
AUTO_DIR="$VAULT_DIR/15-Automation"

echo "=== Starting Systemaops Second Brain Auto-Sync: $(date) ==="

# Navigate to 15-Automation directory
cd "$AUTO_DIR" || exit 1

# Activate virtualenv if available
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run Odoo Sync
echo "1. Running Odoo Sync..."
python3 sync_odoo.py

# Run OpenDesk / XWiki Sync
echo "2. Running OpenDesk / XWiki Sync..."
if [ -f "sync_xwiki.py" ]; then
    python3 sync_xwiki.py
fi

# Run Marketing Engine Sync
echo "3. Running AI Marketing Vault Sync..."
if [ -f "sync_marketing.py" ]; then
    python3 sync_marketing.py
fi

# Git Commit and Push to GitLab & GitHub
cd "$VAULT_DIR" || exit 1
echo "4. Committing and Pushing to GitLab & GitHub..."

git add -A
git commit -m "Auto-Sync: $(date '+%Y-%m-%d %H:%M') - Odoo & OpenDesk updates"
git push origin main
git push github main

echo "=== Auto-Sync Finished Successfully: $(date) ==="
