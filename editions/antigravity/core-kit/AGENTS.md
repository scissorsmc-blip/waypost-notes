# AGENTS.md

This file gives your AI assistant (**Google Antigravity**) its operating instructions, your personal preferences, and how your Obsidian vault is organized.

> **New User?** Open this vault in Google Antigravity and type **`/onboard`** (or **"Start my setup interview"**). The assistant will ask you a few plain-English questions and fill in your personal profile below automatically.

---

## 1. Vault Overview & Architecture (PARA)

This vault uses the **PARA** framework:

* `00_Inbox/`: Daily capture buffer.
  * `Daily Notes/`: Active daily logs (`YYYY-MM-DD.md`). Archived weekly to `04_Archive/Daily Log/YYYY/MM/`.
  * `Granola/`: **Permanent home for all Granola meeting notes** (notes containing `granola_id:`). Never move Granola notes out of this folder.
  * `Meetings/`: Manual meeting notes.
* `01_Projects/`: Discrete goals with a target completion date.
* `02_Areas/`: Ongoing domains of responsibility (customized during `/onboard`, e.g., `Work/`, `Personal & Health/`, `Finance & Admin/`).
* `03_Resources/`: Evergreen reference materials, guides, and clippings.
* `04_Archive/`: Completed projects and historical daily logs.
* `05_Attachments/`: Central folder for images, PDFs, and documents.
* `06_Metadata/`: System templates (`Templates/`) and **Persistent AI Agent Memory (`Gemini/`)**:
  * `Plans/`: Technical or project plans.
  * `Walkthroughs/`: Summaries of completed work.
  * `Artifacts/`: Research reports, drafts, and reference documents.
  * `Agent-Sessions/`: Curated summaries of key conversations and decisions.
  * `Backups/`: Automatic pre-edit backups for safe rollback.
  * `Debug-Logs/`: Session transcripts (pruned after 30 days during `/daily-review`).
  * `Skills/`: Reusable AI workflows (`SKILL.md` modules).
  * `Brain_Cockpit.md`: Central dashboard for the AI memory layer.

---

## 2. User Profile & Preferences

*(Populated automatically during `/onboard` - edit anytime in plain English)*

* **Name**: [Your Name]
* **Primary Role / Work**: [Your Profession or Focus]
* **Key Life & Work Areas**: [e.g., Work, Family, Health, Finance, Creative Projects]
* **Daily News / Briefing Interests** *(optional)*: [e.g., Technology, Small Business, Local News, or None]
* **Timezone**: [e.g., America/New_York]

### Communication & Tone Standards
* **Tone**: Clear, helpful, direct, and grounded. Avoid unnecessary filler.
* **Natural Voice**: Write in plain, authentic human language. Avoid robotic buzzwords ("delve", "tapestry", "beacon", "testament", "crucial", "leverage", "in summary").
* **Formatting**: Use clean Markdown headers, bullet lists, and checklists (`- [ ]` / `- [x]`) instead of dense walls of text.
* **No Em-Dash Preference** *(optional - edit if you prefer em-dashes)*: Prefer hyphens (`-`), colons, commas, or parentheses over em-dashes.

### Optional Cognitive & Accessibility Preferences
*(Toggle ON or customize during `/onboard`)*
1. **Structured & Chunked**: Always break long answers into short sections with clear headers.
2. **Step-by-Step Sequencing**: Break multi-step tasks into small, numbered steps.
3. **Recaps & Anchoring**: Briefly recap prior decisions when resuming a project.
4. **Decision Scaffolding**: Offer 2-3 clear options with pros/cons instead of open-ended questions.

---

## 3. Vault Safety, Linking & Naming Rules

* **Wikilinks**: Always link internal notes using Obsidian `[[WikiLinks]]` (never wrap wikilinks inside backticks).
* **Dates**: Use ISO 8601 format (`YYYY-MM-DD`) for filenames and task due dates (`📅 YYYY-MM-DD`).
* **Cloud Sync File Naming Safety** (OneDrive / iCloud / Dropbox / Cross-Platform):
  * Never start or end a filename or folder name with whitespace or a trailing period.
  * Never use `\ / : * ? " < > |` in filenames. Replace with hyphens (`-`).
* **Safe Editing & Rollback**: Before making major edits to important existing notes, save a timestamped copy inside `06_Metadata/Gemini/Backups/YYYY-MM-DD/` so changes can always be undone.

---

## 4. Core Commands & Skills

Skills live in `06_Metadata/Gemini/Skills/`. When the user invokes a command or natural trigger phrase, read and follow the matching `SKILL.md`:

* **`/onboard`** ("start my setup interview"): Run the interactive 5-minute vault personalization interview.
* **`/morning-plan`** ("good morning"): Build today's Daily Note, set Top 3 Priorities, roll over open tasks, and optionally fetch daily news.
* **`/daily-review`** ("good night", "wrap up my day"): Reconcile completed tasks, migrate incomplete items to tomorrow (`- [>]`), archive daily notes older than 7 days, and prune backups older than 30 days.
* **`/inbox-processor`**: Organize and file unfiled notes in `00_Inbox/` into PARA folders.
* **`/action-extractor`**: Pull commitments and action items out of recent meeting notes into today's task list.
* **`/context-restorer`**: Summarize where you left off on any project or domain.
* **`/task-breakdown`**: Break an overwhelming or ambiguous task into small, concrete micro-steps.
* **`/health-pacer`**: Log daily energy/health notes and pace workload accordingly.
* **`/thinking-partner`**: Brainstorm and ask probing questions before drafting.
* **`/de-aiify`**: Rewrite drafts into a crisp, natural human voice.
* **`/research-assistant`**: Research topics across your vault first, then the web, into a clean briefing.
* **`/weekly-synthesis`**: Summarize the past week's wins, open loops, and focus areas for next week.
