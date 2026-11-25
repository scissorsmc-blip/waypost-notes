# YNAB Sync (`/ynab-sync`)

Pull current YNAB balances and budget status using `03_Resources/Automation & Scripts/ynab-sync/ynab_sync.py`.

## Execution Sequence
1. Check if `~/.gemini/tools/ynab-sync/.env` contains `YNAB_ACCESS_TOKEN`. If missing, show the 2-step token instructions in `FULL_KIT_GUIDE.md`.
2. Run `ynab_sync.py` to refresh the budget summary note.
3. Present a concise snapshot: Ready to Assign, top overspent/tight categories, and any unapproved transactions needing review.

---
*Follow `AGENTS.md` and `06_Metadata/Gemini/System-Prompts/Waypost Operating Rules.md`. Include `[[WikiLinks]]` to referenced notes and keep `06_Metadata/Gemini/` updated.*
