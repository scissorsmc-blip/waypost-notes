# Calm Slate (Obsidian + Google Antigravity)

A ready-to-use, local-first personal knowledge and daily executive system built on **Obsidian** and **Google Antigravity**.

Everything lives in plain Markdown files on your own device (synced with OneDrive, iCloud, Dropbox, or Obsidian Sync). Your AI assistant remembers your projects, plans, rules, and preferences inside `06_Metadata/Gemini/` so you never have to re-explain your life every time you open a new chat.

---

## Choose Your Kit

During installation, you can pick either kit (and you can always upgrade from Core to Full later):

| Feature | Core Kit *(Recommended for Beginners)* | Full Kit *(Power-Up Bundle)* |
| :--- | :---: | :---: |
| **Obsidian PARA Vault** (`Inbox`, `Projects`, `Areas`, `Resources`, `Archive`) | Yes | Yes |
| **Granola Meeting Notes & Sync** (Free plan, Obsidian plugin + `granola_sync.py` -> `00_Inbox/Granola/`) | **Yes** | **Yes** |
| **Persistent AI Memory** (`06_Metadata/Gemini/` + `Brain_Cockpit.md`) | Yes | Yes |
| **5-Minute AI Setup Interview** (`/onboard`) | Yes | Yes |
| **12 Everyday Skills** (Morning Plan, Daily Review, Action Extractor, Task Breakdown, Inbox, De-AI, etc.) | Yes | Yes |
| **Calm Slate Low-Glare Dark Theme** (Anti-glare, cognitive-friendly) | Yes | Yes |
| **Zero Extra Python Packages / Zero Paid Subscriptions** | **Yes** | Optional Python venv |
| **12 Extended Skills** (Premortem, Slide Decks, Financial Audit, Privacy, Study Coach, etc.) | - | **Yes** |
| **Optional Sync Add-Ons** (Outlook/Google Calendar ICS, Google Tasks, YNAB) | - | **Yes** |
| **Android Tablet & Phone Pack + Wallpapers** (Termux widgets, Share Sheet, 5 matching wallpapers & theme guide) | - | **Yes** |

---

## Option 1: One-Command Guided Install (Easiest)

### Windows 10 / 11
1. Press the **Windows key**, type **`PowerShell`**, and open **Windows PowerShell**.
2. Copy and paste this line, then press **Enter**:

```powershell
irm https://raw.githubusercontent.com/scissorsmc-blip/calm-slate/main/installers/install-windows.ps1 | iex
```

The installer will ask whether you want the **Core Kit** or **Full Kit**, install **Obsidian** and **Google Antigravity**, create your vault (in OneDrive or Documents), and link everything together automatically.

### macOS
1. Press **Cmd + Space**, type **`Terminal`**, and press **Enter**.
2. Copy and paste this line, then press **Enter**:

```bash
curl -fsSL https://raw.githubusercontent.com/scissorsmc-blip/calm-slate/main/installers/install-mac.sh | bash
```

---

## Option 2: Zero-Terminal Install (3 Clicks, No Scripts)

Prefer not to run any terminal commands (or using a locked-down work PC)? You can set up the **Core Kit** in 3 clicks:

1. Download and install **[Obsidian](https://obsidian.md)** (free), **[Google Antigravity](https://antigravity.google)**, and **[Granola](https://www.granola.ai)** (free AI meeting notepad).
2. On this GitHub page, click the green **`<> Code`** button -> **Download ZIP**:
   * Unzip the download.
   * Move the **`core-kit`** folder into your **OneDrive**, **iCloud**, or **Documents** folder and rename it **`CalmSlate`**.
   * *(Optional Full Kit)*: Copy everything inside `full-kit-addons/` into that same `CalmSlate` folder.
3. Open **Obsidian** -> **Open folder as vault** -> pick `CalmSlate`:
   * Go to **Settings > Community Plugins** -> **Turn on community plugins** -> **Browse** -> install & enable **`Granola Meetings Simple Sync`** (your pre-configured template and `00_Inbox/Granola` folder load automatically) -> click **Sign In with Granola**.
4. Open **Google Antigravity** -> **Open Folder** -> pick `CalmSlate`.

Because `.agents/rules/AGENTS.md` and `.agents/skills/` live inside the vault, Antigravity automatically loads your rules and skills the moment you open the folder.

---

## Your First 5 Minutes After Install

1. Open **Google Antigravity** pointed at your new **`CalmSlate`** folder.
2. Type this into the chat box and press Enter:

```text
/onboard
```

3. Answer 6-8 plain-English questions (your name, life/work areas, preferred communication style, optional energy/health check-ins, and news topics).
4. Antigravity customizes your `AGENTS.md`, builds your `02_Areas/` folders, and walks you through your first **`/morning-plan`**.

---

## Everyday Commands You Will Use

* **`/morning-plan`** (or *"good morning"*) - Build today's Daily Note, Top 3 Priorities, and rolled-over tasks.
* **`/daily-review`** (or *"good night"*) - Check off finished work, move unfinished tasks to tomorrow, and keep your vault clean.
* **`/inbox-processor`** - Clean up and file loose notes from `00_Inbox/` into the right folders.
* **`/task-breakdown`** - Turn any big or stressful task into tiny 5-15 minute steps.
* **`/context-restorer`** - Instant recap of where you left off on any project.
* **`/thinking-partner`** - Think through an idea with probing questions before writing.
* **`/de-aiify`** - Rewrite drafts into natural, plain human language.
* **`/weekly-synthesis`** - Weekly retrospective of wins, stalled items, and next week's focus.

---

## Privacy & Local-First Guarantee

* **Your notes stay yours**: Everything is plain Markdown on your computer or personal cloud drive.
* **No secrets committed**: `.gitignore` blocks `.env`, OAuth tokens, and local credential files by default.
* **Automatic Undo**: Before editing important existing notes, the assistant saves a timestamped snapshot in `06_Metadata/Gemini/Backups/`.

---

## License

MIT License. Free to use, remix, and share with friends, colleagues, and communities.
