---
name: daily-review
description: Evening shutdown routine, task reconciliation, rollover to tomorrow, and vault hygiene. Use when the user says "/daily-review", "good night", or "wrap up my day".
---

# Daily Review (`/daily-review`)

Close out the day cleanly so nothing slips through the cracks and tomorrow starts organized.

## Execution Sequence

1. **Triage Quick Captures**:
   * Check `00_Inbox/` root for loose notes and offer to file them into PARA (keep `Daily Notes/` and `Meetings/`/`Granola/` in place).
2. **Harvest Today's Meeting Action Items**:
   * Check meeting notes dated today in `00_Inbox/Meetings/` (and `00_Inbox/Granola/` if present) for unlogged commitments.
3. **Reconcile Today's Tasks**:
   * Review `00_Inbox/Daily Notes/YYYY-MM-DD.md` and notes modified today.
   * Mark clearly completed tasks as `- [x]`. If uncertain about any item, ask briefly before checking it off.
4. **Roll Over Unfinished Tasks**:
   * Create tomorrow's Daily Note (`00_Inbox/Daily Notes/YYYY-MM-DD.md`) if it does not exist yet.
   * Copy remaining open tasks (`- [ ]`) to tomorrow and mark them as rolled over (`- [>]`) in today's note.
5. **Optional Full-Kit Sync**:
   * If configured, run `gtasks_sync.py` and `brain_sync.py`.
6. **Automated Hygiene**:
   * Archive Daily Notes older than 7 days to `04_Archive/Daily Log/YYYY/MM/`.
   * Prune backup snapshots in `06_Metadata/Gemini/Backups/` and raw logs in `06_Metadata/Gemini/Debug-Logs/` older than 30 days. Never delete `Plans/`, `Walkthroughs/`, or `Artifacts/`.
7. **Concise Wrap-Up**:
   * Report what got done today, what moved to tomorrow, and confirm the vault is clean.
