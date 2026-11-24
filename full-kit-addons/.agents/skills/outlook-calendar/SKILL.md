---
name: outlook-calendar
description: Cross-platform calendar integration for New Outlook, Microsoft 365, Google Calendar, or iCloud via private ICS feeds using calendar_sync.py.
---

# Calendar Sync (`/outlook-calendar`)

Fetch today's (or any target date's) calendar events using `03_Resources/Automation & Scripts/calendar_sync.py`.

## Usage
1. Run `python "03_Resources/Automation & Scripts/calendar_sync.py"` (or `--date YYYY-MM-DD`).
2. Add `--with-granola` to also pull recent Granola meeting notes.
3. If no ICS feeds are configured yet, guide the user to run `calendar_sync.py --setup` and paste their private read-only ICS URL from Outlook or Google Calendar.
4. Inject formatted events into the `## Schedule & Meetings` section of today's Daily Note.
