#!/data/data/com.termux/files/usr/bin/bash
# install_termux_pack.sh - One-Command Termux Setup for Android Tablet & Phone
# Deploys Python venv, Android Share Sheet capture hooks, Termux:Widget shortcuts,
# Calm Slate dark palette, and runs cross-platform brain_sync.py.

set -e

VAULT_DIR="${VAULT_DIR:-$HOME/vault}"
SCRIPTS_DIR="$VAULT_DIR/03_Resources/Automation & Scripts"
TERMUX_PACK="$SCRIPTS_DIR/termux"
VENV_DIR="$HOME/.gemini/tools/.venv"

echo "=== Waypost Notes Termux Starter Pack Installer ==="

if [ ! -d "$VAULT_DIR/06_Metadata/Gemini" ]; then
  echo "ERROR: Vault not found at $VAULT_DIR."
  echo "Link your synced vault first, for example:"
  echo "  termux-setup-storage && ln -s ~/storage/shared/Obsidian/WaypostNotes ~/vault"
  exit 1
fi

# 1. Ensure Python & prebuilt cryptography are installed
if command -v pkg >/dev/null 2>&1; then
  echo "[1/5] Ensuring Termux python & python-cryptography packages..."
  pkg install -y python python-cryptography
elif ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Please install Python 3."
  exit 1
else
  echo "[1/5] Python already installed: $(python3 --version)"
fi

# 2. Build/update shared Termux Python venv
echo "[2/5] Configuring Python venv at $VENV_DIR..."
mkdir -p "$HOME/.gemini/tools"
if [ -d "$VENV_DIR" ] && ! grep -q "include-system-site-packages = true" "$VENV_DIR/pyvenv.cfg" 2>/dev/null; then
  rm -rf "$VENV_DIR"
fi
if [ ! -x "$VENV_DIR/bin/python" ]; then
  python3 -m venv --system-site-packages "$VENV_DIR"
fi
"$VENV_DIR/bin/pip" install --quiet --upgrade pip
"$VENV_DIR/bin/pip" install --quiet -r "$SCRIPTS_DIR/requirements.txt"

# 3. Deploy Android Share Sheet hooks
echo "[3/5] Installing Android Share Sheet hooks in ~/bin/..."
mkdir -p "$HOME/bin"

cat > "$HOME/bin/termux-url-opener" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
PY="$HOME/.gemini/tools/.venv/bin/python"
[ -x "$PY" ] || PY="python3"
"$PY" "$HOME/vault/03_Resources/Automation & Scripts/termux/mobile_capture.py" url "$1"
echo ""
read -rp "Press Enter to close..."
EOF

cat > "$HOME/bin/termux-file-editor" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
PY="$HOME/.gemini/tools/.venv/bin/python"
[ -x "$PY" ] || PY="python3"
"$PY" "$HOME/vault/03_Resources/Automation & Scripts/termux/mobile_capture.py" file "$1"
echo ""
read -rp "Press Enter to close..."
EOF

chmod +x "$HOME/bin/termux-url-opener" "$HOME/bin/termux-file-editor"

# 4. Deploy Termux:Widget shortcuts to ~/.shortcuts/
echo "[4/5] Deploying Termux:Widget shortcuts to ~/.shortcuts/..."
mkdir -p "$HOME/.shortcuts"
for script in \
  01_Init_Daily_Note.sh \
  02_Log_Vitals.sh \
  03_Log_Expense.sh \
  04_Sync_All.sh; do
  if [ -f "$TERMUX_PACK/$script" ]; then
    cp "$TERMUX_PACK/$script" "$HOME/.shortcuts/$script"
    chmod +x "$HOME/.shortcuts/$script"
  fi
done

# 5. Apply Calm Slate & Warm Ink Termux dark theme
if [ -f "$TERMUX_PACK/colors.properties" ]; then
  mkdir -p "$HOME/.termux"
  cp "$TERMUX_PACK/colors.properties" "$HOME/.termux/colors.properties"
  command -v termux-reload-settings >/dev/null 2>&1 && termux-reload-settings || true
  echo "[+] Applied Calm Slate dark theme to ~/.termux/colors.properties."
fi

# 6. Run cross-platform Brain Sync
echo "[5/5] Running cross-platform brain_sync.py..."
"$VENV_DIR/bin/python" "$SCRIPTS_DIR/brain_sync.py"

echo ""
echo "=== Setup Complete ==="
echo "Next steps:"
echo "  1. Disable Android battery optimization for Termux & Termux:Widget (Unrestricted)."
echo "  2. Add the Termux:Widget 4x2 widget to your home screen."
echo "  3. Optional: Configure calendar sync via:"
echo "     $VENV_DIR/bin/python \"$SCRIPTS_DIR/calendar_sync.py\" --setup"
