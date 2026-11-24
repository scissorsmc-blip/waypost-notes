#!/data/data/com.termux/files/usr/bin/bash
PY="$HOME/.gemini/tools/.venv/bin/python"
[ -x "$PY" ] || PY="python3"
SCRIPTS="$HOME/vault/03_Resources/Automation & Scripts"
echo "=== Syncing Brain, Calendar, Granola & Tasks ==="
"$PY" "$SCRIPTS/brain_sync.py"
"$PY" "$SCRIPTS/calendar_sync.py" --with-granola
"$PY" "$SCRIPTS/gtasks_sync.py" || true
read -rp "Press Enter to close..."
