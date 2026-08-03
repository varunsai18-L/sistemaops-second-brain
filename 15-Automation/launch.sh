#!/bin/bash
# Cross-Platform Launcher for PVMS 2.0 RFQ Intelligence System (Mac & Linux)
echo "=========================================================================="
echo "🚀 Launching PVMS 2.0 RFQ Intelligence System for Team & Executive Review"
echo "=========================================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f "venv/bin/python" ]; then
    PYTHON_BIN="venv/bin/python"
elif [ -f "../.venv/bin/python" ]; then
    PYTHON_BIN="../.venv/bin/python"
else
    PYTHON_BIN="python3"
fi

echo "1. Running Odoo & openDesk Auto-Sync..."
python3 sync_odoo.py

echo "2. Running Second Brain -> PVMS Ingestion..."
cd "/Users/varunsai/.gemini/antigravity/scratch/project-viability-management-system" 2>/dev/null || cd "../.."
"$PYTHON_BIN" scripts/sync_second_brain_to_pvms.py

echo "3. Opening browser at http://localhost:8501..."
if command -v open >/dev/null; then
    open "http://localhost:8501"
elif command -v xdg-open >/dev/null; then
    xdg-open "http://localhost:8501"
fi

IP_ADDR=$(ifconfig 2>/dev/null | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

echo "=========================================================================="
echo "🎉 System running!"
echo "   - Local URL:   http://localhost:8501"
if [ -n "$IP_ADDR" ]; then
    echo "   - Network URL: http://$IP_ADDR:8501 (Share with team members on network)"
fi
echo "=========================================================================="
