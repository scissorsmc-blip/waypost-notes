#!/data/data/com.termux/files/usr/bin/bash
PY="$HOME/.gemini/tools/.venv/bin/python"
[ -x "$PY" ] || PY="python3"
"$PY" "$HOME/vault/03_Resources/Automation & Scripts/termux/log_vitals.py"
read -rp "Press Enter to close..."
