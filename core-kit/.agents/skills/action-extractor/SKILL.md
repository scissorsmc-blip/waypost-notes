---
name: action-extractor
description: Commitment and action item harvester. Scans recent meeting notes or transcripts and extracts concrete tasks, owners, and due dates into today's Daily Note.
---

# Action Extractor (`/action-extractor`)

Turn meeting notes into concrete tasks so commitments never get dropped.

## Execution Sequence

1. **Locate Recent Meeting Notes**:
   * Scan `00_Inbox/Meetings/` and `00_Inbox/Granola/` (if present) for notes from the last 48 hours, or inspect the specific note the user referenced.
2. **Separate Owner vs. Waiting-On Items**:
   * **My Action Items**: Tasks the user committed to doing -> format as `- [ ] **Action** (from [[Meeting Note]]) 📅 YYYY-MM-DD #domain`.
   * **Waiting On Others**: Commitments made by other people -> list clearly as `Waiting on [Name]` so the user only tracks follow-up if desired.
3. **Confirm Before Injecting (When Ambiguous)**:
   * Only add the user's own commitments to `00_Inbox/Daily Notes/YYYY-MM-DD.md` under `## Tasks by Domain`.
4. **Link Sources**:
   * Always include a `[[WikiLink]]` back to the original meeting note.
