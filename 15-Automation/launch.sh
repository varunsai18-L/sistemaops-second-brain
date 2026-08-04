#!/bin/bash
# Cross-Platform Robust Launcher for PVMS 2.0 RFQ Intelligence System (Mac & Linux)
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
python3 sync_odoo.py 2>/dev/null || true

echo "2. Running Second Brain -> PVMS Ingestion..."
RFQP_DIR="/Users/varunsai/.gemini/antigravity/scratch/project-viability-management-system"
if [ -d "$RFQP_DIR" ]; then
    cd "$RFQP_DIR"
    STREAMLIT_BIN="$RFQP_DIR/.venv/bin/streamlit"
    "$RFQP_DIR/.venv/bin/python" scripts/sync_second_brain_to_pvms.py
else
    STREAMLIT_BIN="streamlit"
    python3 scripts/sync_second_brain_to_pvms.py 2>/dev/null || true
fi

# Check if Streamlit is already running on port 8501
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "✅ Streamlit server is already running on port 8501!"
else
    echo "3. Starting PVMS 2.0 Web Application server..."
    nohup "$STREAMLIT_BIN" run app/main.py --server.headless false > /tmp/streamlit_pvms.log 2>&1 &
    sleep 3
fi

echo "4. Opening browser at http://localhost:8501..."
if command -v open >/dev/null 2>&1; then
    open "http://localhost:8501"
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:8501"
fi

IP_ADDR=$(ifconfig 2>/dev/null | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)

echo "=========================================================================="
echo "🎉 PVMS 2.0 Web App is running live!"
echo "   - Local URL:   http://localhost:8501"
if [ -n "$IP_ADDR" ]; then
    echo "   - Network URL: http://$IP_ADDR:8501 (Share this URL with team members on the same network)"
fi
echo "=========================================================================="
