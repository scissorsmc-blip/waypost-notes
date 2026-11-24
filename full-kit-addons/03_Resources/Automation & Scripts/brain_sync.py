#!/usr/bin/env python3
"""
brain_sync.py - Cross-Platform Antigravity Brain Synchronizer
=============================================================

Synchronizes AGENTS.md, Vault Skills (06_Metadata/Gemini/Skills/), and optional
CLI session logs/sync state across Windows, macOS, Linux, and Android Termux.
"""

import os
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def resolve_vault_root() -> Path:
    env_vault = os.environ.get("CALM_SLATE_VAULT") or os.environ.get("VAULT_DIR")
    if env_vault and (Path(env_vault) / "06_Metadata" / "Gemini").exists():
        return Path(env_vault).resolve()
    script_vault = Path(__file__).resolve().parents[2]
    if (script_vault / "06_Metadata" / "Gemini").exists():
        return script_vault
    home_vault = Path.home() / "vault"
    if (home_vault / "06_Metadata" / "Gemini").exists():
        return home_vault.resolve()
    raise FileNotFoundError(
        "Unable to resolve Vault root. Run this script from inside your vault or set CALM_SLATE_VAULT."
    )


def copy_if_newer(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime + 1.0:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return True
    return False


def main() -> None:
    vault_root = resolve_vault_root()
    vault_brain = vault_root / "06_Metadata" / "Gemini"
    vault_rules = vault_root / "AGENTS.md"
    if not vault_rules.exists():
        vault_rules = vault_brain / "AGENTS.md"

    vault_skills = vault_brain / "Skills"
    vault_debug_logs = vault_brain / "Debug-Logs"
    vault_gtasks = vault_brain / "GoogleTasks"
    workspace_rules_dir = vault_root / ".agents" / "rules"
    workspace_skills_dir = vault_root / ".agents" / "skills"

    home = Path.home()
    global_plugin_dir = home / ".gemini" / "config" / "plugins" / "user-profile"
    global_rules_dir = global_plugin_dir / "rules"
    global_skills_dir = global_plugin_dir / "skills"
    local_brain_root = home / ".gemini" / "antigravity-cli" / "brain"
    local_gtasks_dir = home / ".gemini" / "tools" / "google-tasks"

    for d in (
        workspace_rules_dir,
        workspace_skills_dir,
        global_rules_dir,
        global_skills_dir,
        vault_debug_logs,
        vault_gtasks,
    ):
        d.mkdir(parents=True, exist_ok=True)

    # 1. Mirror canonical AGENTS.md
    if vault_rules.exists():
        for target in (
            workspace_rules_dir / "AGENTS.md",
            global_rules_dir / "AGENTS.md",
            vault_brain / "AGENTS.md",
        ):
            if target.resolve() != vault_rules.resolve():
                shutil.copy2(vault_rules, target)
        print("[+] Synced AGENTS.md across workspace, global plugin, and vault brain.")

    # 2. Mirror canonical Vault Skills to workspace .agents/skills and Global Plugin directory
    skill_count = 0
    if vault_skills.exists():
        for skill_dir in sorted(vault_skills.iterdir()):
            if not skill_dir.is_dir():
                continue
            shutil.copytree(skill_dir, workspace_skills_dir / skill_dir.name, dirs_exist_ok=True)
            shutil.copytree(skill_dir, global_skills_dir / skill_dir.name, dirs_exist_ok=True)
            skill_count += 1
        print(f"[+] Synced {skill_count} skills to workspace and {global_skills_dir}.")

    # 3. Bi-Directional Brain Transcript Sync (Local <-> Vault Debug-Logs)
    pushed = 0
    pulled = 0
    if local_brain_root.exists():
        for conv_dir in local_brain_root.iterdir():
            if not conv_dir.is_dir():
                continue
            log_dir = conv_dir / ".system_generated" / "logs"
            if not log_dir.exists():
                continue
            for jsonl in log_dir.glob("*.jsonl"):
                if copy_if_newer(jsonl, vault_debug_logs / conv_dir.name / jsonl.name):
                    pushed += 1

    if vault_debug_logs.exists():
        local_brain_root.mkdir(parents=True, exist_ok=True)
        for conv_dir in vault_debug_logs.iterdir():
            if not conv_dir.is_dir():
                continue
            for jsonl in conv_dir.glob("*.jsonl"):
                target_local = local_brain_root / conv_dir.name / ".system_generated" / "logs" / jsonl.name
                if copy_if_newer(jsonl, target_local):
                    pulled += 1
    print(f"[+] Brain Transcripts: Pushed {pushed} file(s) to Vault; Pulled {pulled} file(s) to Local Brain.")

    # 4. Bi-Directional Google Tasks Token & State Sync (only if user enabled Google Tasks)
    local_gtasks_dir.mkdir(parents=True, exist_ok=True)
    gtasks_synced = 0
    for fname in ("credentials.json", "token.json", "gtasks_state.json"):
        local_f = local_gtasks_dir / fname
        vault_f = vault_gtasks / fname
        if local_f.exists() and (not vault_f.exists() or local_f.stat().st_mtime > vault_f.stat().st_mtime + 1.0):
            shutil.copy2(local_f, vault_f)
            gtasks_synced += 1
        elif vault_f.exists() and (not local_f.exists() or vault_f.stat().st_mtime > local_f.stat().st_mtime + 1.0):
            shutil.copy2(vault_f, local_f)
            gtasks_synced += 1
    if gtasks_synced:
        print(f"[+] Google Tasks state/token sync complete ({gtasks_synced} file(s) updated).")


if __name__ == "__main__":
    main()
