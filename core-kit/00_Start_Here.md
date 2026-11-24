---
type: welcome
title: Start Here - Welcome to Calm Slate
tags:
  - start-here
  - onboarding
---

# Welcome to Calm Slate

You have everything installed and linked together. Your notes live locally in **Obsidian**, and your AI assistant (**Google Antigravity**) reads your rules, remembers your context in `06_Metadata/Gemini/`, and helps you run your day without losing track of tasks or ideas.

---

## Your First 2 Steps (5 Minutes)

### Step 1: Connect Free Granola Meeting Sync (1 Minute)
[Granola](https://www.granola.ai) captures clean meeting summaries (free plan supported, zero meeting bots joining your calls) so Obsidian (`00_Inbox/Granola/`) stays your single source of truth:
1. Install **Granola** (if not installed already) and sign in.
2. **Desktop Obsidian Plugin (Automatic every 15 mins)**: Open Obsidian **Settings > Community Plugins** -> **Turn on community plugins** -> confirm **Granola Meetings Simple Sync** is **ON** -> open its settings and click **Connect / Sign In with Granola**.
3. **Cross-Platform / CLI / Mobile Backup (`granola_sync.py`, zero extra packages)**: Also included right in `03_Resources/Automation & Scripts/granola_sync.py`. Run `python "03_Resources/Automation & Scripts/granola_sync.py" --auth` once, then sync and link into today's Daily Note anytime with `--link-daily`.

### Step 2: Run Your 5-Minute Setup Interview
1. Open **Google Antigravity** and make sure this vault folder is selected as your workspace.
2. Type this message into the chat box and press Enter:

> **`/onboard`** *(or just type: **"Start my setup interview"**)*

Antigravity will ask you 6-8 plain-English questions about your work, personal life areas, preferred communication style, and optional accessibility settings (like structured checklists or energy tracking). It will then customize [[AGENTS]] and create your personal folders automatically.

---

## How Your Vault Is Organized (PARA)

| Folder | What Goes Inside |
| :--- | :--- |
| **`00_Inbox/`** | Daily Notes (`Daily Notes/`), quick captures, and meeting notes (`Meetings/`). |
| **`01_Projects/`** | Active initiatives with a clear finish line or deadline. |
| **`02_Areas/`** | Ongoing life and work responsibilities (Work, Home, Health, Finance, Volunteering). |
| **`03_Resources/`** | Reference guides, recipes, research, templates, and saved articles. |
| **`04_Archive/`** | Completed projects and old daily notes (moved automatically). |
| **`05_Attachments/`** | Images, PDFs, and screenshots linked into notes. |
| **`06_Metadata/Gemini/`** | Your AI assistant's persistent memory (`Plans/`, `Walkthroughs/`, `Artifacts/`, `Backups/`, `Skills/`, and [[Brain_Cockpit]]). |

---

## Everyday Commands You Can Try Right Away

Just type any of these in Google Antigravity:

* **`/morning-plan`** (or say *"good morning"*) - Build today's agenda, pull open tasks, and set your Top 3 Priorities.
* **`/daily-review`** (or say *"good night"*) - Wrap up the day, mark completed tasks, and roll unfinished items to tomorrow.
* **`/inbox-processor`** - Sort messy inbox notes into the right folders automatically.
* **`/task-breakdown`** - Turn a big, overwhelming project into tiny 10-minute steps.
* **`/context-restorer`** - Instant recap of where you left off on any project.
* **`/thinking-partner`** - Brainstorm an idea before you start writing.
* **`/de-aiify`** - Rewrite stiff or robotic drafts into your natural human voice.

---

## Optional Dark Comfort Theme

A low-glare dark theme (**Calm Slate & Warm Ink**) is already included to reduce eye strain and harsh glare:
* Open Obsidian **Settings > Appearance > CSS snippets** and toggle **`calm-slate-dark`** ON or OFF anytime.
