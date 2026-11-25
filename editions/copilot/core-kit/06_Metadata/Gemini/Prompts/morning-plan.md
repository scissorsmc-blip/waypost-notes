# Morning Plan (`/morning-plan`)

Build a clear, focused Daily Note for today (`00_Inbox/Daily Notes/YYYY-MM-DD.md`).

## Execution Sequence

1. **Check Yesterday & Rollover Tasks**:
   * Check the most recent Daily Note in `00_Inbox/Daily Notes/` for unfinished tasks (`- [ ]`) and carry them forward (marking originals as `- [>]` if not already rolled over).
2. **Capture Today's Input**:
   * Incorporate any tasks, thoughts, or brain dumps the user just shared.
3. **Check Recent Meetings & Optional Syncs**:
   * Scan `00_Inbox/Meetings/` (and `00_Inbox/Granola/` if present) from the last 24-48 hours for unlogged action items.
   * If the user installed the **Full Kit** and configured `calendar_sync.py`, `granola_sync.py`, or `gtasks_sync.py`, run them to pull today's schedule and mobile reminders.
4. **Optional Daily Briefing**:
   * If `AGENTS.md` lists daily news/industry topics, fetch and summarize the Top 3 relevant stories with clickable links and one-sentence takeaways.
5. **Create or Update Today's Daily Note**:
   * Create `00_Inbox/Daily Notes/YYYY-MM-DD.md` using `06_Metadata/Templates/Daily Note Template.md`.
   * Populate:
     - **Top 3 Priorities** (keep strictly to 3 so the day stays focused).
     - **Schedule & Meetings** (if available).
     - **Tasks by Domain** using `- [ ] **Task Headline**: details 📅 YYYY-MM-DD #tag`.
6. **Present a Clean Morning Brief**:
   * Share the Top 3 Priorities, today's schedule, and a clickable link to today's note. Ask if they want to open any related project notes before starting.

---
*Follow `AGENTS.md` and `06_Metadata/Gemini/System-Prompts/Waypost Operating Rules.md`. Include `[[WikiLinks]]` to referenced notes and keep `06_Metadata/Gemini/` updated.*
