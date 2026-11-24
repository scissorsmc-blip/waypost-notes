#!/usr/bin/env bash
# Calm Slate - Guided macOS Installer (Core Kit & Full Kit + Auto-Sync)
#
# Installs Obsidian, Google Antigravity, and Granola, sets up automatic cross-device
# sync (Apple iCloud Drive for iPhone/iPad OR Syncthing for Android/Windows),
# creates your PARA + AI Memory vault (06_Metadata/Gemini/), and links rules & skills.

set -euo pipefail

KIT="${KIT:-}"
SYNC_MODE="${SYNC_MODE:-}"
VAULT_PATH="${VAULT_PATH:-}"
REPO_OWNER="${REPO_OWNER:-scissorsmc-blip}"
REPO_NAME="${REPO_NAME:-calm-slate}"
BRANCH="${BRANCH:-main}"
SKIP_APP_INSTALL="${SKIP_APP_INSTALL:-0}"

header() {
  echo ""
  echo "============================================================"
  echo "  $1"
  echo "============================================================"
  echo ""
}

copy_folder_safe() {
  local src="$1"
  local dst="$2"
  [ -d "$src" ] || return 0
  mkdir -p "$dst"
  (
    cd "$src"
    find . -mindepth 1 | while IFS= read -r rel; do
      rel="${rel#./}"
      [ "$(basename "$rel")" = ".gitkeep" ] && continue
      if [ -d "$src/$rel" ]; then
        mkdir -p "$dst/$rel"
      elif [ ! -e "$dst/$rel" ]; then
        mkdir -p "$(dirname "$dst/$rel")"
        cp "$src/$rel" "$dst/$rel"
      fi
    done
  )
}

header "Calm Slate - macOS Setup"
echo "This installer sets up Obsidian + Google Antigravity + Granola with a"
echo "ready-to-use vault, persistent AI memory (06_Metadata/Gemini), and easy sync."
echo ""

# 1. Choose Core Kit vs Full Kit
if [ -z "$KIT" ]; then
  echo "Choose which kit to install:"
  echo "  [1] Core Kit (Recommended for Beginners)"
  echo "      - Obsidian + Google Antigravity + Granola sync script + PARA vault"
  echo "      - AI memory + 12 everyday skills + Calm Slate dark theme."
  echo ""
  echo "  [2] Full Kit (Power-Up Bundle)"
  echo "      - Everything in Core Kit PLUS 12 extended skills, 5 Calm Slate wallpapers,"
  echo "        Android theme guide, and optional Calendar/Google Tasks/YNAB sync."
  echo ""
  read -rp "Enter 1 for Core Kit or 2 for Full Kit [Default: 1]: " choice
  if [ "$choice" = "2" ]; then KIT="full"; else KIT="core"; fi
fi
echo "[+] Selected: $(echo "$KIT" | tr '[:lower:]' '[:upper:]') KIT"

# 2. Choose Cross-Device Sync Mode (Simple & TBI-Friendly)
if [ -z "$SYNC_MODE" ]; then
  echo ""
  echo "How will you sync Calm Slate with other devices?"
  echo "  [1] Mac + iPhone / iPad (Recommended for Apple - Free built-in iCloud Drive)"
  echo "  [2] Mac + Android or Windows (Recommended for Android - Free Syncthing, 1 QR scan)"
  echo "  [3] Mac Only (Local Documents folder - no sync)"
  echo ""
  read -rp "Enter 1, 2, or 3 [Default: 1]: " sync_choice
  case "$sync_choice" in
    2) SYNC_MODE="syncthing" ;;
    3) SYNC_MODE="local" ;;
    *) SYNC_MODE="icloud" ;;
  esac
fi
echo "[+] Sync mode: $SYNC_MODE"

# 3. Pick Vault Folder based on chosen Sync Mode
if [ -z "$VAULT_PATH" ]; then
  OBSIDIAN_ICLOUD="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents"
  GENERIC_ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs"
  if [ "$SYNC_MODE" = "icloud" ]; then
    if [ -d "$OBSIDIAN_ICLOUD" ] || [ -d "$GENERIC_ICLOUD" ]; then
      DEFAULT_VAULT="$OBSIDIAN_ICLOUD/CalmSlate"
    else
      echo "[i] iCloud Drive folder not detected on this Mac yet; falling back to Documents."
      DEFAULT_VAULT="$HOME/Documents/CalmSlate"
    fi
  else
    DEFAULT_VAULT="$HOME/Documents/CalmSlate"
  fi
  echo ""
  echo "Where should your Calm Slate vault folder be created?"
  echo "  Recommended: $DEFAULT_VAULT"
  read -rp "Press Enter to accept recommended location, or paste another path: " custom_path
  if [ -n "$custom_path" ]; then
    VAULT_PATH="${custom_path/#\~/$HOME}"
  else
    VAULT_PATH="$DEFAULT_VAULT"
  fi
fi
echo "[+] Vault folder: $VAULT_PATH"

# 4. Install Obsidian, Google Antigravity & Granola via Homebrew (or guide direct download)
if [ "$SKIP_APP_INSTALL" != "1" ]; then
  header "Step 1 of 4: Installing Obsidian, Antigravity & Granola"
  if command -v brew >/dev/null 2>&1; then
    echo "[*] Checking/installing Obsidian via Homebrew..."
    brew list --cask obsidian >/dev/null 2>&1 || brew install --cask obsidian
    echo "[+] Obsidian ready."

    echo "[*] Checking/installing Google Antigravity via Homebrew..."
    brew list --cask antigravity >/dev/null 2>&1 || brew install --cask antigravity
    echo "[+] Google Antigravity ready."

    echo "[*] Checking/installing Granola (AI meeting notepad) via Homebrew..."
    if brew list --cask granola >/dev/null 2>&1 || brew install --cask granola; then
      echo "[+] Granola ready."
    else
      echo "[i] Download free Granola from: https://www.granola.ai"
    fi
  else
    echo "[i] Homebrew is not installed on this Mac (totally fine!)."
    echo "    Download and drag these free apps into Applications:"
    echo "      1. Obsidian:           https://obsidian.md"
    echo "      2. Google Antigravity: https://antigravity.google"
    echo "      3. Granola (meetings): https://www.granola.ai"
    read -rp "Press Enter to continue creating your vault now..."
  fi
fi

# 5. Locate local repo files or download from GitHub
header "Step 2 of 4: Preparing Starter Vault Files"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_REPO_ROOT="$(dirname "$SCRIPT_DIR")"
TEMP_ROOT=""

if [ -f "$LOCAL_REPO_ROOT/core-kit/AGENTS.md" ]; then
  SOURCE_ROOT="$LOCAL_REPO_ROOT"
  echo "[+] Using local Calm Slate files from: $SOURCE_ROOT"
else
  TEMP_ROOT="$(mktemp -d)"
  ZIP_URL="https://github.com/$REPO_OWNER/$REPO_NAME/archive/refs/heads/$BRANCH.zip"
  echo "[*] Downloading Calm Slate from $ZIP_URL ..."
  curl -fsSL "$ZIP_URL" -o "$TEMP_ROOT/kit.zip"
  unzip -q "$TEMP_ROOT/kit.zip" -d "$TEMP_ROOT"
  SOURCE_ROOT="$(find "$TEMP_ROOT" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
  echo "[+] Downloaded and unpacked Calm Slate."
fi

# 6. Build Vault (Core Kit + optional Full Kit overlay)
mkdir -p "$VAULT_PATH"
copy_folder_safe "$SOURCE_ROOT/core-kit" "$VAULT_PATH"
echo "[+] Installed Core Kit vault structure, templates, dark theme, Granola sync, and 12 core skills."

if [ "$KIT" = "full" ]; then
  copy_folder_safe "$SOURCE_ROOT/full-kit-addons" "$VAULT_PATH"
  echo "[+] Installed Full Kit add-ons (sync scripts, 5 wallpapers, theme guide, and 12 extended skills)."
fi

# 7. Mirror rules & skills + register vault in Obsidian
header "Step 3 of 4: Linking Vault Rules, Skills, Obsidian & Sync"
GLOBAL_PLUGIN="$HOME/.gemini/config/plugins/user-profile"
mkdir -p "$VAULT_PATH/.agents/rules" "$VAULT_PATH/.agents/skills" "$GLOBAL_PLUGIN/rules" "$GLOBAL_PLUGIN/skills"
cp "$VAULT_PATH/AGENTS.md" "$VAULT_PATH/.agents/rules/AGENTS.md"
cp "$VAULT_PATH/AGENTS.md" "$GLOBAL_PLUGIN/rules/AGENTS.md"
cp -R "$VAULT_PATH/06_Metadata/Gemini/Skills/"* "$VAULT_PATH/.agents/skills/"
cp -R "$VAULT_PATH/06_Metadata/Gemini/Skills/"* "$GLOBAL_PLUGIN/skills/"
echo "[+] Linked AGENTS.md and all skills into workspace and Antigravity."

# Auto-register vault in Obsidian's obsidian.json on macOS
if command -v python3 >/dev/null 2>&1; then
  python3 - "$VAULT_PATH" << 'PYEOF'
import json, sys, time, uuid
from pathlib import Path

vault_path = str(Path(sys.argv[1]).expanduser().resolve())
cfg_path = Path.home() / "Library" / "Application Support" / "obsidian" / "obsidian.json"
cfg_path.parent.mkdir(parents=True, exist_ok=True)
if cfg_path.exists():
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception:
        cfg = {"vaults": {}}
else:
    cfg = {"vaults": {}}

vaults = cfg.setdefault("vaults", {})
if not any(v.get("path") == vault_path for v in vaults.values() if isinstance(v, dict)):
    vid = uuid.uuid4().hex[:16]
    vaults[vid] = {"path": vault_path, "ts": int(time.time() * 1000), "open": True}
    cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    print("[+] Registered vault automatically inside Obsidian.")
PYEOF
fi

# Auto-configure Syncthing if user chose Option 2 (Mac + Android / Windows)
if [ "$SYNC_MODE" = "syncthing" ]; then
  if command -v brew >/dev/null 2>&1; then
    echo "[*] Installing and starting Syncthing background service..."
    brew list syncthing >/dev/null 2>&1 || brew install syncthing
    brew services start syncthing >/dev/null 2>&1 || true
    sleep 3
    if command -v syncthing >/dev/null 2>&1; then
      syncthing cli config folders add --id calm-slate --label "Calm Slate" --path "$VAULT_PATH" >/dev/null 2>&1 || true
      echo "[+] Syncthing running in background with Calm Slate folder registered (.stignore active)."
      echo "    Open http://127.0.0.1:8384 -> Actions > Show ID to scan QR code from Android Syncthing-Fork."
      command -v open >/dev/null 2>&1 && open "http://127.0.0.1:8384" >/dev/null 2>&1 || true
    fi
  else
    echo "[i] Install Syncthing from https://syncthing.net (or install Homebrew), then see SYNC_GUIDE.md."
  fi
elif [ "$SYNC_MODE" = "icloud" ]; then
  echo "[+] Vault placed in Apple iCloud Drive Obsidian container for automatic iPhone/iPad sync."
fi

# 8. Optional Python venv for Full Kit
if [ "$KIT" = "full" ]; then
  header "Step 4 of 4: Setting Up Optional Python Tools (Full Kit)"
  if command -v python3 >/dev/null 2>&1; then
    VENV_DIR="$HOME/.gemini/tools/.venv"
    mkdir -p "$HOME/.gemini/tools"
    [ -x "$VENV_DIR/bin/python" ] || python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --quiet --upgrade pip
    "$VENV_DIR/bin/pip" install --quiet -r "$VAULT_PATH/03_Resources/Automation & Scripts/requirements.txt"
    "$VENV_DIR/bin/python" "$VAULT_PATH/03_Resources/Automation & Scripts/brain_sync.py"
    echo "[+] Full Kit Python environment ready."
  else
    echo "[i] Python 3 not found. Install Python 3 later to use Full Kit sync scripts."
  fi
fi

[ -n "$TEMP_ROOT" ] && rm -rf "$TEMP_ROOT"

header "All Done! Calm Slate Is Ready"
echo "Vault Location: $VAULT_PATH"
echo ""
echo "Your Next Steps (5 Minutes):"
echo "  1. Connect free Granola meeting sync (1-time browser sign-in):"
echo "     python3 \"$VAULT_PATH/03_Resources/Automation & Scripts/granola_sync.py\" --auth"
echo "  2. Open Google Antigravity -> Open Folder -> $VAULT_PATH -> type: /onboard"
echo "  3. Open Obsidian anytime to view 00_Start_Here.md and SYNC_GUIDE.md."
if [ "$KIT" = "full" ]; then
  echo "  4. Full Kit Guide: Open FULL_KIT_GUIDE.md whenever you want optional add-ons."
fi
echo ""
