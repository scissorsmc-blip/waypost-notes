#!/usr/bin/env python3
"""
daily_note_init.py - Fast Daily Note Generator (Mobile & Desktop)
=================================================================

Creates today's Daily Note in 00_Inbox/Daily Notes/YYYY-MM-DD.md if missing,
using clean PARA domain headings.
"""

import datetime
import os
import sys
from pathlib import Path


def resolve_vault_root() -> Path:
    env_vault = os.environ.get("WAYPOST_VAULT") or os.environ.get("VAULT_DIR")
    if env_vault and (Path(env_vault) / "06_Metadata" / "Gemini").exists():
        return Path(env_vault).resolve()
    script_vault = Path(__file__).resolve().parents[3]
    if (script_vault / "06_Metadata" / "Gemini").exists():
        return script_vault
    home_vault = Path.home() / "vault"
    if (home_vault / "06_Metadata" / "Gemini").exists():
        return home_vault.resolve()
    raise FileNotFoundError("Unable to resolve Obsidian Vault root.")


def main() -> None:
    vault = resolve_vault_root()
    today = datetime.date.today()
    date_str = today.isoformat()
    yesterday = (today - datetime.timedelta(days=1)).isoformat()
    tomorrow = (today + datetime.timedelta(days=1)).isoformat()
    day_name = today.strftime("%A")
    pretty_date = today.strftime("%A, %B %d, %Y").replace(" 0", " ")

    daily_dir = vault / "00_Inbox" / "Daily Notes"
    daily_dir.mkdir(parents=True, exist_ok=True)
    note_path = daily_dir / f"{date_str}.md"

    if note_path.exists():
        print(f"[=] Today's Daily Note already exists: {note_path.name}")
        return

    content = f"""---
type: daily
date: {date_str}
day: {day_name}
tags:
  - daily
  - log
created: {date_str}
updated: {date_str}
---

# {pretty_date}

> [[{yesterday}| Yesterday]] <- **{date_str}** -> [[{tomorrow}| Tomorrow]]

---

## Top 3 Priorities
> *Focus on these before taking on new incoming requests.*
1. 
2. 
3. 

---

## Energy & Health Check
* **Energy Level (1-5)**:: 
* **Focus / Stamina**:: Normal
* **Notes**:: 

---

## Schedule & Meetings
* 

---

## Quick Capture & Scratchpad
* 

---

## Tasks by Domain

### Work & Projects
- [ ] 

### Personal, Home & Admin
- [ ] 

---

## Evening Wrap-Up
1. Check off completed tasks (`- [x]`)
2. Run `/daily-review` to carry unfinished tasks (`- [>]`) to tomorrow
"""
    note_path.write_text(content, encoding="utf-8")
    print(f"[+] Created today's Daily Note: {note_path}")


if __name__ == "__main__":
    main()
