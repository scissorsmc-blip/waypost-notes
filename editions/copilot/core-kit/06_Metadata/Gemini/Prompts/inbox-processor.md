# Inbox Processor (`/inbox-processor`)

Keep `00_Inbox/` clear without losing ideas or tasks.

## Execution Sequence

1. **Scan `00_Inbox/` Root**:
   * List loose notes and attachments in `00_Inbox/` (do NOT move `Daily Notes/`, `Meetings/`, or `Granola/`).
2. **Extract Action Items & Errands**:
   * Pull any tasks, follow-ups, or errands into today's Daily Note (`00_Inbox/Daily Notes/YYYY-MM-DD.md`) as `- [ ] **Task** 📅 YYYY-MM-DD #tag`.
3. **Clean & Normalize**:
   * Add clean YAML frontmatter (`title`, `created`, `tags`).
   * Format messy raw text with clear headings and bullet points.
   * Enforce cloud-safe filenames (`YYYY-MM-DD - Descriptive Title.md`, no leading/trailing spaces or illegal characters).
4. **File Into PARA**:
   * Active goal with deadline -> `01_Projects/`
   * Ongoing responsibility -> `02_Areas/`
   * Reference material -> `03_Resources/`
   * Historical/inactive -> `04_Archive/`
5. **Report Summary**:
   * Show a short table of what was filed, where it moved, and any tasks added to today's Daily Note.

---
*Follow `AGENTS.md` and `06_Metadata/Gemini/System-Prompts/Waypost Operating Rules.md`. Include `[[WikiLinks]]` to referenced notes and keep `06_Metadata/Gemini/` updated.*
