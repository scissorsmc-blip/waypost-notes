---
name: switching-machines
description: Cross-device state synchronizer and clean session hand-off. Use when switching computers or moving between desktop and mobile/tablet.
---

# Switching Machines (`/switching-machines`)

Ensure all progress, rules, skills, and open threads transfer smoothly to your next device.

## Execution Sequence
1. Run `python "03_Resources/Automation & Scripts/brain_sync.py"` if available to sync `AGENTS.md`, skills, and session transcripts.
2. Create a concise hand-off note in `06_Metadata/Gemini/Agent-Sessions/YYYY-MM-DD - Session Hand-Off.md` summarizing:
   * What was completed this session.
   * Exact stopping point and active files.
   * Next 1-3 actions on the new device.
3. Confirm cloud sync (OneDrive / iCloud / Dropbox) has no filename conflicts before closing.
