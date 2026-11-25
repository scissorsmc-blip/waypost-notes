---
type: welcome
title: Start Here - Welcome to Waypost Notes (Copilot Edition)
tags:
  - start-here
  - onboarding
  - copilot
---

# Welcome to Waypost Notes (Copilot Edition)

Everything runs inside **one single app: Obsidian**, using the **Obsidian Copilot** community plugin powered by **Google Gemini**. It works on Windows, Mac, Linux, iPhone, iPad, and Android.

Your AI assistant reads your rules in [[AGENTS]], runs slash-command workflows from `06_Metadata/Gemini/Prompts/` and `Skills/`, and keeps persistent memory inside `06_Metadata/Gemini/`.

---

## Your First 3 Steps (6 Minutes Total)

### Step 1: Connect Your AI Provider (Free Google Gemini Default, or Any Copilot-Compatible AI)
1. Open **[Google AI Studio](https://aistudio.google.com/apikey)** in your browser, sign in with your Google account, and click **Create API Key** (free tier works great for personal vaults).
2. In Obsidian, open **Settings (gear icon) > Community Plugins**:
   * Click **Turn on community plugins** if prompted, and verify **Copilot** is toggled **ON**.
3. Go to **Settings > Copilot > Providers > Google Gemini**, paste your Gemini API key, and choose a Gemini model (for example, `gemini-2.5-flash` or `gemini-2.5-pro`).
   * *Note*: You can also use **any other AI provider supported by the [Obsidian Copilot community plugin](https://github.com/logancyang/obsidian-copilot)** ([obsidiancopilot.com](https://www.obsidiancopilot.com)) - such as OpenAI, Claude, Groq, OpenRouter, or local offline models like Ollama.

### Step 2: Connect Free Granola Meeting Sync (1 Minute)
[Granola](https://www.granola.ai) captures clean meeting summaries (free plan supported, zero meeting bots joining your calls) so Obsidian (`00_Inbox/Granola/`) stays your single source of truth across Windows, Mac, Linux, and Android:
1. Install **Granola** (if not installed already) and sign in.
2. Run the zero-dependency sync script included in your vault once to sign in:
   ```bash
   python "03_Resources/Automation & Scripts/granola_sync.py" --auth
   ```
3. Sync and link meetings into today's Daily Note anytime with `--link-daily` so every meeting lives in `00_Inbox/Granola/` for Copilot to search and extract tasks. No Granola Obsidian plugin required.

### Step 3: Run Your 5-Minute Setup Interview
1. Click the **Copilot** icon in the left ribbon to open the AI chat sidebar.
2. Type **`/onboard`** (or **"Start my setup interview"**) and press Enter.

Copilot will ask 6-8 plain-English questions about your work, life areas, preferred communication style, and optional cognitive/accessibility settings, then personalize [[AGENTS]] and build your `02_Areas/` folders automatically.

---

## How Your Vault Is Organized (PARA)

| Folder | What Goes Inside |
| :--- | :--- |
| **`00_Inbox/`** | Daily Notes (`Daily Notes/`), quick captures, and meeting notes (`Meetings/`). |
| **`01_Projects/`** | Active initiatives with a clear finish line or deadline. |
| **`02_Areas/`** | Ongoing life and work responsibilities (Work, Home, Health, Finance). |
| **`03_Resources/`** | Reference guides, recipes, research, templates, and saved articles. |
| **`04_Archive/`** | Completed projects and older daily notes. |
| **`05_Attachments/`** | Images, PDFs, and screenshots linked into notes. |
| **`06_Metadata/Gemini/`** | Persistent AI memory (`Memory/`, `Plans/`, `Walkthroughs/`, `Artifacts/`, `Agent-Sessions/`, `Prompts/`, `System-Prompts/`, `Skills/`, and [[Brain_Cockpit]]). |

---

## Everyday Slash Commands Inside Copilot Chat

Type **`/`** in the Copilot chat box to pick any built-in Waypost Notes workflow:

* **`/onboard`** - 5-minute guided vault personalization interview.
* **`/morning-plan`** - Build today's Daily Note, Top 3 Priorities, and rolled-over tasks.
* **`/daily-review`** - Wrap up the day, mark completed tasks, and carry open items to tomorrow.
* **`/inbox-processor`** - Sort messy notes in `00_Inbox/` into the right PARA folders.
* **`/action-extractor`** - Pull commitments and action items out of meeting notes.
* **`/context-restorer`** - Instant recap of where you left off on any project.
* **`/task-breakdown`** - Turn an overwhelming task into tiny 5-15 minute steps.
* **`/health-pacer`** - Log energy/health notes and pace today's workload.
* **`/thinking-partner`** - Brainstorm an idea before writing.
* **`/de-aiify`** - Rewrite robotic drafts into your natural human voice.
* **`/research-assistant`** - Synthesize vault notes and external research into a clean brief.
* **`/weekly-synthesis`** - Weekly review of wins, open loops, and next week's focus.

---

## Low-Glare Calm Slate Dark Theme

The **Calm Slate & Warm Ink** dark CSS snippet is already included and enabled to reduce eye strain and harsh glare. You can toggle it anytime under **Obsidian Settings > Appearance > CSS snippets > `calm-slate-dark`**.
