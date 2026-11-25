# Context Restorer (`/context-restorer`)

Generate an instant, high-clarity resumption briefing when returning to any project, domain, or previous session.

## Execution Sequence

1. **Identify Target**:
   * Locate the requested project (`01_Projects/`), area (`02_Areas/`), or most recent session/Daily Note.
2. **Audit Recent Activity**:
   * Check the most recently modified notes, meeting captures, and open tasks (`- [ ]`) connected to that topic.
3. **Deliver a Structured Anchor**:
   * **Where You Left Off**: Last completed milestone or decision.
   * **Active State & Open Threads**: Drafts in progress, open tasks, or items waiting on someone else.
   * **The Single Next Decision**: The clearest next concrete action to take right now.
4. **Link Essential Files**:
   * Include clickable links and `[[WikiLinks]]` to the 1-3 key notes needed to resume immediately.

---
*Follow `AGENTS.md` and `06_Metadata/Gemini/System-Prompts/Waypost Operating Rules.md`. Include `[[WikiLinks]]` to referenced notes and keep `06_Metadata/Gemini/` updated.*
