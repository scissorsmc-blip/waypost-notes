---
type: guide
title: Full Kit Power-Up Guide (Waypost Notes (Copilot Edition))
tags:
  - full-kit
  - copilot
  - automation
  - guide
Updated: 2026-11-24
---

# Full Kit Power-Up Guide (Waypost Notes (Copilot Edition))

Your **Full Kit** includes everything in the Core Kit (Obsidian + pre-configured Copilot plugin + Gemini setup + 12 everyday slash commands + Calm Slate dark theme) **plus**:

* **12 Extended Copilot Slash Commands & Skills** (24 total in `/` menu)
* **5 Matching Calm Slate Wallpapers** + **Android & Samsung System Theme Guide**
* **Optional Python Sync Scripts** (Calendar ICS, Granola Meetings, Google Tasks, YNAB)

**You do NOT need to set all of these up at once.** Turn on only the integrations you actually use, whenever you are ready.

---

## Included Optional Integrations

### 1. Calendar Sync (Outlook, Microsoft 365, Google Calendar, or Apple iCloud)
Pulls your daily schedule (including Zoom/Teams/Meet links) via read-only private ICS feeds.
* **Setup (2 minutes)**:
  1. In New Outlook / M365: **Settings > Calendar > Shared calendars > Publish a calendar** -> copy the `.ics` link. *(In Google Calendar: **Settings > Integrate calendar > Secret address in iCal format**.)*
  2. Run:
     ```bash
     python "03_Resources/Automation & Scripts/calendar_sync.py" --setup
     ```

### 2. Granola Meeting Notes Sync *(Already Included in Core Kit!)*
The zero-dependency `03_Resources/Automation & Scripts/granola_sync.py` script is included right in the Core Kit so `00_Inbox/Granola/` stays your single source of truth across every platform (no Granola Obsidian plugin needed).
* **CLI / Mobile Auth (1 minute)**:
  ```bash
  python "03_Resources/Automation & Scripts/granola_sync.py" --auth
  ```
* **Sync & Link to Today's Daily Note**:
  ```bash
  python "03_Resources/Automation & Scripts/granola_sync.py" --link-daily
  ```

### 3. Google Tasks Two-Way Sync (Phone Reminders <-> Obsidian)
Pulls phone reminders into your Daily Note and pushes scheduled Obsidian tasks back to Google Tasks.
* Save your Google Cloud Desktop `credentials.json` to `~/.gemini/tools/google-tasks/credentials.json` and run:
  ```bash
  python "03_Resources/Automation & Scripts/gtasks_sync.py"
  ```

### 4. YNAB Personal Budget Sync
Fetches your YNAB account balances and category status into `02_Areas/Finance & Admin/YNAB Budget Dashboard.md` so Copilot can run `/ynab-sync` and `/financial-diagnostic`.
* Save `YNAB_API_KEY=your_personal_access_token` in `~/.gemini/tools/ynab-sync/.env` and run `ynab_sync.py`.

### 5. Calm Slate Wallpapers & Android/Samsung System Theme Guide
* See [[Calm Slate - Android & Samsung System Theme Guide]] and the 5 matching low-glare wallpapers (Dark Misty Smoky Mountains + minimalist matte variants) in `05_Attachments/Themes/CalmSlate/`.
* Optional Android Termux automation scripts are in `03_Resources/Automation & Scripts/termux/` (see [[Termux_Mobile_Setup_Guide]]).

---

## 12 Additional Copilot `/` Commands Included in Full Kit

Type **`/`** inside the Obsidian Copilot chat panel anytime to run:
* `/outlook-calendar` - Summarize your synced calendar schedule
* `/ynab-sync` - Review YNAB budget balances and categories
* `/switching-machines` - Clean hand-off summary when switching devices
* `/premortem-evaluator` - Stress-test big decisions before committing
* `/deck-architect` - Turn notes or plans into structured slide outlines
* `/financial-diagnostic` - Cash flow and subscription creep audit
* `/privacy-scrubber` - Audit exposed personal info and draft removal requests
* `/oss-pipeline` - Find open-source alternatives to paid subscriptions
* `/study-coach` - Active recall and study coaching for exams or new topics
* `/travel-navigator` - Trip itineraries, packing lists, and flight strategy
* `/career-strategist` - Resume, LinkedIn, and behavioral interview prep
* `/create-command` - Build your own custom Copilot `/commands` in `06_Metadata/Gemini/Prompts/`
