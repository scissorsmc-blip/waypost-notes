# AGENTS.md

This file gives your AI assistant (**Obsidian Copilot powered by Google Gemini**) its operating instructions, your personal profile, and how your Obsidian vault is organized.

> **New User?** Open the **Copilot** sidebar in Obsidian and type **`/onboard`** (or **"Start my setup interview"**). Copilot will ask a few plain-English questions and fill in your personal profile below automatically.

---

## 1. Vault Overview & Architecture (PARA)

This vault uses the **PARA** framework:

* `00_Inbox/`: Daily capture buffer.
  * `Daily Notes/`: Active daily logs (`YYYY-MM-DD.md`). Archive weekly to `04_Archive/Daily Log/YYYY/MM/`.
  * `Granola/`: **Permanent home for all Granola meeting notes** (notes containing `granola_id:`). Never move Granola notes out of this folder.
  * `Meetings/`: Manual meeting notes.
* `01_Projects/`: Discrete goals with a target completion date.
* `02_Areas/`: Ongoing domains of responsibility (customized during `/onboard`, e.g., `Work/`, `Personal & Health/`, `Finance & Admin/`).
* `03_Resources/`: Evergreen reference materials, guides, and clippings.
* `04_Archive/`: Completed projects and historical daily logs.
* `05_Attachments/`: Central folder for images, PDFs, and documents.
* `06_Metadata/`: System templates (`Templates/`) and **Persistent AI Memory (`Gemini/`)**:
  * `Memory/`: Saved Copilot long-term memory notes.
  * `Prompts/`: Slash-command custom prompts (`/` menu inside Obsidian Copilot).
  * `System-Prompts/`: Active Copilot system instructions (`Waypost Operating Rules.md`).
  * `Skills/`: Reusable agent workflows (`SKILL.md` modules for Copilot Agent Mode).
  * `Plans/`: Project plans and step-by-step designs.
  * `Walkthroughs/`: Summaries of completed work.
  * `Artifacts/`: Research reports, outlines, and reference docs.
  * `Agent-Sessions/`: Auto-saved Copilot conversation histories.
  * `Backups/`: Pre-edit snapshots for safe undo.
  * `Brain_Cockpit.md`: Central dashboard for the AI memory layer.

---

## 2. User Profile & Preferences

*(Populated automatically during `/onboard` - edit anytime in plain English)*

* **Name**: [Your Name]
* **Primary Role / Work**: [Your Profession or Focus]
* **Key Life & Work Areas**: [e.g., Work, Family, Health, Finance, Creative Projects]
* **Daily Briefing Interests** *(optional)*: [e.g., Technology, Small Business, Local News, or None]
* **Timezone**: [e.g., America/New_York]

### Communication & Tone Standards
* **Tone**: Clear, helpful, direct, and grounded. Avoid filler.
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
* **Cloud Sync File Naming Safety** (OneDrive / iCloud / Dropbox / Obsidian Sync):
  * Never start or end a filename or folder name with whitespace or a trailing period.
  * Never use `\ / : * ? " < > |` in filenames. Replace with hyphens (`-`).
* **Safe Editing**: Present note edits clearly via Copilot's split diff view (`autoAcceptEdits: false`) so the user stays in control of every change.

---

## 4. Core Slash Commands (Copilot Custom Prompts & Skills)

All commands are available directly via **`/`** inside Obsidian Copilot (`06_Metadata/Gemini/Prompts/` and `06_Metadata/Gemini/Skills/`):

* **`/onboard`**: Run the interactive 5-minute vault personalization interview.
* **`/morning-plan`**: Build today's Daily Note, set Top 3 Priorities, and roll over open tasks.
* **`/daily-review`**: Reconcile completed tasks, migrate incomplete items to tomorrow (`- [>]`), and run vault hygiene.
* **`/inbox-processor`**: Organize and file loose notes in `00_Inbox/` into PARA folders.
* **`/action-extractor`**: Pull commitments and action items out of recent meeting notes into today's task list.
* **`/context-restorer`**: Summarize where you left off on any project or life area.
* **`/task-breakdown`**: Break an overwhelming or vague task into tiny 5-15 minute micro-steps.
* **`/health-pacer`**: Log daily energy/health notes and pace workload accordingly.
* **`/thinking-partner`**: Brainstorm and ask probing questions before drafting.
* **`/de-aiify`**: Rewrite drafts into a crisp, natural human voice.
* **`/research-assistant`**: Synthesize vault notes and external research into a clean briefing.
* **`/weekly-synthesis`**: Summarize the past week's wins, open loops, and next week's focus areas.
