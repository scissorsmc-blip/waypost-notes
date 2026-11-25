# Waypost Notes

**A calm, local-first personal knowledge and daily executive system built on Obsidian, Granola meeting notes, and persistent AI memory (`06_Metadata/Gemini/`).**

* **Website & Ideas Board:** [waypostnotes.com](https://waypostnotes.com) | [Community Ideas](https://waypostnotes.com/ideas.html)
* **New to Obsidian or AI tools?** Start with the plain-English **[Beginner's Start-to-Finish Guide](BEGINNER_GUIDE.md)** (includes important privacy warnings and step-by-step checklists).
* **Volunteer-Run Project:** Waypost Notes is free, open source (MIT License), and maintained solely by volunteers in their spare time.

---

## Choose Your Edition (Both Included in This Repo)

Both editions share the exact same PARA vault structure, persistent AI memory (`06_Metadata/Gemini/`), 24 modular skills, free **Granola** meeting sync (`granola_sync.py`), **Calm Slate** low-glare dark theme, and free device sync guides.

| Feature | Copilot Edition *(Recommended for Beginners & Mobile)* | Antigravity Edition *(Desktop Power Workspace)* |
| :--- | :--- | :--- |
| **Apps Needed** | **One single app: Obsidian** (with pre-configured [Obsidian Copilot](https://github.com/logancyang/obsidian-copilot) plugin) + Granola | **Obsidian** (zero plugins required) + **Google Antigravity** + Granola |
| **AI Providers** | Pre-configured for free Google Gemini; works with **any Copilot-compatible AI** (Gemini, OpenAI, Claude, Groq, OpenRouter, or local Ollama) | Google Antigravity (Google account sign-in, no API key needed) |
| **Best For** | Beginners, mobile users (Windows, Mac, Linux, iPhone, iPad, Android), or bring-your-own-AI / offline Ollama setups | Desktop power users who want deep multi-step agentic workflows and an ultra-clean plugin-free Obsidian vault |
| **Step-by-Step Guide** | [Copilot Edition Beginner Guide](editions/copilot/BEGINNER_GUIDE.md) | [Antigravity Edition Beginner Guide](editions/antigravity/BEGINNER_GUIDE.md) |

---

## Choose Your Kit (Picked During Install)

| Feature | Core Kit *(Recommended for Beginners)* | Full Kit *(Power-Up Bundle)* |
| :--- | :---: | :---: |
| **Obsidian PARA Vault** (`Inbox`, `Projects`, `Areas`, `Resources`, `Archive`) | Yes | Yes |
| **Granola Meeting Notes & Sync** (Free plan, zero-dependency `granola_sync.py` -> `00_Inbox/Granola/`) | **Yes** | **Yes** |
| **Built-In Free Auto-Sync** (Apple iCloud for Mac/iOS, Syncthing + `.stignore` for Android/Windows, `SYNC_GUIDE.md`) | **Yes** | **Yes** |
| **Persistent AI Memory** (`06_Metadata/Gemini/` + `Brain_Cockpit.md`) | Yes | Yes |
| **5-Minute AI Setup Interview** (`/onboard`) | Yes | Yes |
| **12 Everyday Skills & `/` Commands** (Morning Plan, Daily Review, Action Extractor, Task Breakdown, De-AI, etc.) | Yes | Yes |
| **Calm Slate Low-Glare Dark Theme** (`calm-slate-dark.css`) | Yes | Yes |
| **12 Extended Skills & `/` Commands** (Premortem, Slide Decks, Financial Audit, Privacy, Study Coach, etc.) | - | **Yes** |
| **5 Matching Calm Slate Wallpapers + Android/Samsung System Theme Guide** | - | **Yes** |
| **Optional Sync Add-Ons** (Outlook/Google Calendar ICS, Google Tasks, YNAB, Termux Pack) | - | **Yes** |

---

## Option 1: One-Command Guided Install (Easiest)

### Copilot Edition (Single App: Obsidian + Copilot Plugin)

**Windows 10 / 11 (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/scissorsmc-blip/waypost-notes/main/installers/install-copilot-windows.ps1 | iex
```

**macOS (Terminal):**
```bash
curl -fsSL https://raw.githubusercontent.com/scissorsmc-blip/waypost-notes/main/installers/install-copilot-mac.sh | bash
```

### Antigravity Edition (Obsidian + Google Antigravity)

**Windows 10 / 11 (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/scissorsmc-blip/waypost-notes/main/installers/install-antigravity-windows.ps1 | iex
```

**macOS (Terminal):**
```bash
curl -fsSL https://raw.githubusercontent.com/scissorsmc-blip/waypost-notes/main/installers/install-antigravity-mac.sh | bash
```

> **Tip:** You can also run the unified interactive installer (`installers/install-windows.ps1` or `installers/install-mac.sh`) directly and pick your edition on screen.

---

## Option 2: Zero-Terminal Install (No Scripts)

Prefer not to run any terminal commands (or setting up on a locked-down work PC)?

1. Download and install **[Obsidian](https://obsidian.md)** and **[Granola](https://www.granola.ai)** (plus **[Google Antigravity](https://antigravity.google)** if choosing Antigravity Edition).
2. Click the green **`<> Code`** button -> **Download ZIP** and unzip it.
3. Move the **`core-kit/`** folder into your **Documents**, **OneDrive**, or **iCloud** folder and rename it **`WaypostNotes`** (or **`WaypostNotesCopilot`**).
4. Copy the files from your chosen edition overlay into that same vault folder:
   * **Copilot Edition:** Copy everything inside `editions/copilot/core-kit/` into your vault folder.
   * **Antigravity Edition:** Copy everything inside `editions/antigravity/core-kit/` into your vault folder (and copy `06_Metadata/Gemini/Skills/` into `.agents/skills/`).
   * *(Optional Full Kit)*: Copy `full-kit-addons/` and `editions/<your-edition>/full-kit-addons/` into your vault folder.
5. Open **Obsidian** -> **Open folder as vault** -> pick your new folder.
   * **Copilot Edition:** Go to **Settings > Community Plugins > Turn on > Browse** -> install and enable **`Copilot`** (by Logan Yang). Your pre-configured settings load automatically.
   * **Antigravity Edition:** Open **Google Antigravity** -> **Open Folder** -> pick your vault folder.
6. Run `python "03_Resources/Automation & Scripts/granola_sync.py" --auth` once (uses Python standard library only) so your Granola meetings sync into `00_Inbox/Granola/`.

---

## Repository Structure

```text
waypost-notes/
├── core-kit/                  # Shared Core Kit (PARA, templates, Calm Slate theme, granola_sync.py, 11 shared core skills)
├── full-kit-addons/           # Shared Full Kit (12 extended skills, 5 wallpapers, theme guide, optional sync scripts)
├── editions/
│   ├── copilot/               # Copilot Edition overlay (plugin config, 24 Copilot /prompts, Memory/, System-Prompts/, guide)
│   └── antigravity/           # Antigravity Edition overlay (.agents/, AGENTS.md, Brain_Cockpit.md, guide)
└── installers/                # Unified Windows/macOS installers + edition shortcut launchers
```

---

## Important Disclaimer & Privacy Warning

* **Free & Provided "As-Is":** Shared free of charge under the MIT License with no warranties or guarantees. Not officially affiliated with Obsidian, Google, Granola, Microsoft, or Apple.
* **Not Medical, Legal, or Financial Advice:** AI tools can make mistakes. Always confirm important decisions with a qualified human professional.
* **Public Cloud AI Privacy Warning:** Although your notes live as plain files on your own device, anything you send to a cloud AI chat is processed by that cloud AI provider. Keep Social Security numbers, bank/card numbers, passwords, sensitive medical or VA claim records, private legal files, and confidential work data out of public cloud AI chats.

---

## License

MIT License. Free to use, remix, and share with friends, colleagues, and communities.
