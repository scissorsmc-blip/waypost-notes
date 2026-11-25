#!/usr/bin/env bash
# Waypost Notes (Copilot Edition) - macOS Shortcut Launcher
set -euo pipefail
export EDITION="copilot"
TMP_SCRIPT="$(mktemp)"
trap 'rm -f "$TMP_SCRIPT"' EXIT
curl -fsSL "https://raw.githubusercontent.com/${REPO_OWNER:-scissorsmc-blip}/${REPO_NAME:-waypost-notes}/${BRANCH:-main}/installers/install-mac.sh" -o "$TMP_SCRIPT"
bash "$TMP_SCRIPT" "$@"
