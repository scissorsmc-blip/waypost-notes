#!/usr/bin/env python3
"""
brain_sync.py - Waypost Notes (Copilot Edition) Prompt & Skill Synchronizer
===================================================================

Keeps 06_Metadata/Gemini/Skills/ and 06_Metadata/Gemini/Prompts/ aligned so
any custom skill you add is also available as a /command inside Obsidian Copilot.
"""

import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def resolve_vault_root() -> Path:
    env_vault = os.environ.get("WAYPOST_VAULT") or os.environ.get("VAULT_DIR")
    if env_vault and (Path(env_vault) / "06_Metadata" / "Gemini").exists():
        return Path(env_vault).resolve()
    script_vault = Path(__file__).resolve().parents[2]
    if (script_vault / "06_Metadata" / "Gemini").exists():
        return script_vault
    home_vault = Path.home() / "vault"
    if (home_vault / "06_Metadata" / "Gemini").exists():
        return home_vault.resolve()
    raise FileNotFoundError(
        "Unable to resolve Vault root. Run this script from inside your vault or set WAYPOST_VAULT."
    )


def main() -> None:
    vault_root = resolve_vault_root()
    gemini_dir = vault_root / "06_Metadata" / "Gemini"
    skills_dir = gemini_dir / "Skills"
    prompts_dir = gemini_dir / "Prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)

    synced = 0
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                continue
            target_prompt = prompts_dir / f"{skill_dir.name}.md"
            if not target_prompt.exists() or skill_md.stat().st_mtime > target_prompt.stat().st_mtime + 1.0:
                raw = skill_md.read_text(encoding="utf-8")
                body = re.sub(r"^---\n.*?\n---\n+", "", raw, flags=re.S).strip()
                prompt_text = (
                    body
                    + "\n\n---\n"
                    + "*Follow `AGENTS.md` and `06_Metadata/Gemini/System-Prompts/Waypost Operating Rules.md`. "
                    + "Include `[[WikiLinks]]` to referenced notes and keep `06_Metadata/Gemini/` updated.*\n"
                )
                target_prompt.write_text(prompt_text, encoding="utf-8")
                synced += 1

    print(f"[+] Copilot prompt sync complete ({synced} prompt(s) updated in {prompts_dir}).")


if __name__ == "__main__":
    main()
