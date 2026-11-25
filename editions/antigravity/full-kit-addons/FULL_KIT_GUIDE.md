---
type: guide
title: Full Kit Power-Up Guide
tags:
  - full-kit
  - automation
  - guide
---

# Full Kit Power-Up Guide

Your **Full Kit** includes everything in the Core Kit plus optional sync scripts, an Android mobile pack, and 12 additional AI skills.

**You do NOT need to set all of these up at once.** Turn on only the integrations you actually use, whenever you are ready.

---

## Included Optional Integrations

### 1. Calendar Sync (Outlook, Microsoft 365, Google Calendar, or Apple iCloud)
Pulls your daily schedule (including Zoom/Teams/Meet links) into `/morning-plan` using a read-only private ICS feed. Works on Windows, Mac, Linux, and Android.

* **Setup (2 minutes)**:
  1. In **New Outlook / M365**: Go to **Settings > Calendar > Shared calendars > Publish a calendar** -> copy the `.ics` link. *(In Google Calendar: **Settings > Integrate calendar > Secret address in iCal format**.)*
  2. Run:
     ```bash
     python "03_Resources/Automation & Scripts/calendar_sync.py" --setup
     ```
  3. Test with:
     ```bash
     python "03_Resources/Automation & Scripts/calendar_sync.py"
     ```

### 2. Granola Meeting Notes Sync *(Already Included in Core Kit!)*
The zero-dependency `03_Resources/Automation & Scripts/granola_sync.py` script is included right in the Core Kit so `00_Inbox/Granola/` is always your single source of truth across every platform (no Obsidian plugin needed).
* **CLI / Mobile Auth (1 minute)**:
  ```bash
  python "03_Resources/Automation & Scripts/granola_sync.py" --auth
  ```
* **Sync & Link to Today's Daily Note**:
  ```bash
  python "03_Resources/Automation & Scripts/granola_sync.py" --link-daily
  ```

### 3. Google Tasks Two-Way Sync (Phone Reminders <-> Obsidian)
Pulls quick reminders captured on your phone into your Daily Note and pushes scheduled Obsidian tasks back to Google Tasks.

* **Setup**:
  1. Download your Google OAuth Desktop `credentials.json` from Google Cloud Console (enable the **Google Tasks API**).
  2. Place `credentials.json` in `~/.gemini/tools/google-tasks/credentials.json`.
  3. Run:
     ```bash
     python "03_Resources/Automation & Scripts/gtasks_sync.py"
     ```

### 4. YNAB Personal Budget Sync
Fetches your current YNAB account balances and category status into your vault for `/ynab-sync` and `/financial-diagnostic`.

* **Setup**:
  1. Create a Personal Access Token in YNAB (**Account Settings > Developer Settings**).
  2. Save `YNAB_ACCESS_TOKEN=your_token_here` in `~/.gemini/tools/ynab-sync/.env`.
  3. Ask Antigravity to run **`/ynab-sync`**.

### 5. Cross-Device Brain Sync (`brain_sync.py`)
Keeps `AGENTS.md`, skills, and synced transcripts aligned across multiple computers and Android Termux.
```bash
python "03_Resources/Automation & Scripts/brain_sync.py"
```

### 6. Android Tablet & Phone Pack (`termux/`) + Calm Slate Wallpapers
* **Mobile Automation**: See [[Termux_Mobile_Setup_Guide]] for setting up one-tap Android home-screen widgets, Share Sheet web/PDF capture, and the Calm Slate dark palette on Android via Termux.
* **System-Wide Theme & Wallpapers**: See [[Calm Slate - Android & Samsung System Theme Guide]] and the 5 matching low-glare wallpapers (Dark Misty Smoky Mountains + minimalist matte variants for tablet and phone) bundled in `05_Attachments/Themes/CalmSlate/`.

---

## 12 Additional Skills Included in Full Kit

Ask Antigravity to use any of these anytime:
* `/outlook-calendar` - Read your daily calendar schedule
* `/ynab-sync` - Check YNAB budget balances and categories
* `/switching-machines` - Clean hand-off summary when switching computers
* `/premortem-evaluator` - Stress-test big decisions before committing
* `/deck-architect` - Turn notes or plans into structured slide outlines
* `/financial-diagnostic` - Cash flow and subscription creep audit
* `/privacy-scrubber` - Audit exposed personal info and draft removal requests
* `/oss-pipeline` - Find open-source alternatives to paid subscriptions
* `/study-coach` - Active recall and study coaching for exams or new skills
* `/travel-navigator` - Trip itineraries, packing lists, and flight strategy
* `/career-strategist` - Resume, LinkedIn, and behavioral interview prep
* `/create-command` - Build your own custom `/commands` and skills
