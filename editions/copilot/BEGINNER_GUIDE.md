# Waypost Notes (Copilot Edition): Beginner's Start-to-Finish Guide

Welcome. This guide walks you step by step from zero to a working, calm, organized personal workspace running inside **one single app: Obsidian**, using the **Obsidian Copilot** plugin powered by **Google Gemini**, plus **Granola** for automatic meeting notes.

You do **not** need a technical background. Take it one step at a time, check off boxes as you go, and take breaks whenever you need them.

---

## Important Disclaimer & Privacy Warning (Please Read First)

* **Free & Provided "As-Is"**: Waypost Notes (Copilot Edition) is shared **free of charge** under the MIT License for personal and educational use. It is provided **"as is," with no warranties, guarantees, or promises of uptime, accuracy, or fitness for any specific purpose**. The creators are not responsible for data loss, sync issues, or decisions made using this system. This is an independent community project and is **not** officially affiliated with Obsidian, Obsidian Copilot, Google, Granola, Microsoft, Apple, or any government agency.
* **Not Medical, Legal, or Financial Advice**: AI assistants can make mistakes or invent details. Never rely solely on AI output for medical, VA/disability benefit, legal, tax, or financial decisions. Always confirm important information with a qualified human professional.
* **Public Cloud AI Privacy Warning**: While your notes are stored as plain files on your own device, **anything you type into Copilot chat or ask Copilot to read is sent to a public cloud AI service (Google Gemini API)** to generate answers.
  * **DO NOT** put highly sensitive personal information into notes that you send to Copilot.
  * Keep the following **OUT** of AI chats and AI-accessible notes: Social Security numbers, bank or credit card numbers, passwords or PINs, sensitive medical or VA claim records, private legal case files, and confidential employer or client data.

---

## Before You Start (2 Minutes)

Make sure you have:
- [ ] A **Windows 10/11 PC** or a **Mac** (and optionally an iPhone, iPad, or Android device)
- [ ] A free **Google account** (Gmail)
- [ ] About **10 to 15 minutes**

**Tip on Core Kit vs. Full Kit**: During Step 1, the installer asks if you want the **Core Kit** or **Full Kit**.
* Choose **`1` (Core Kit)** if you want the simplest, cleanest setup to start. You can always add extras later.

---

## Step 1: Download & Install Waypost Notes (Copilot Edition) (5 Minutes)

### On Windows 10 / 11
- [ ] Press the **Windows key** on your keyboard.
- [ ] Type **`PowerShell`** and click **Windows PowerShell**.
- [ ] Copy this exact line, paste it into the window (right-click to paste), and press **Enter**:

```powershell
irm https://raw.githubusercontent.com/scissorsmc-blip/waypost-notes/main/installers/install-copilot-windows.ps1 | iex
```

- [ ] Answer the 3 simple prompts on screen:
  1. **Kit**: Press **`1`** (Core Kit) and hit Enter.
  2. **Device Sync**: Press **`1`** if you have an Android phone/tablet (free Syncthing), **`2`** for OneDrive, or **`3`** for this PC only.
  3. **Folder Location**: Press **Enter** to accept the recommended folder.

### On Mac
- [ ] Press **Command + Space**, type **`Terminal`**, and press **Enter**.
- [ ] Copy this exact line, paste it into Terminal, and press **Enter**:

```bash
curl -fsSL https://raw.githubusercontent.com/scissorsmc-blip/waypost-notes/main/installers/install-copilot-mac.sh | bash
```

- [ ] Answer the 3 simple prompts on screen:
  1. **Kit**: Press **`1`** (Core Kit) and hit Enter.
  2. **Device Sync**: Press **`1`** if you use an iPhone/iPad (automatic free Apple iCloud), **`2`** for Android/Windows (free Syncthing), or **`3`** for Mac only.
  3. **Folder Location**: Press **Enter** to accept the recommended folder.

### Prefer No Terminal Commands At All? (3-Click Alternative)
- [ ] Download and install **[Obsidian](https://obsidian.md)** and **[Granola](https://www.granola.ai)** directly from their websites.
- [ ] On GitHub, click the green **`<> Code`** button -> **Download ZIP** -> unzip it -> move the **`core-kit`** folder into your Documents, OneDrive, or iCloud folder and rename it **`WaypostNotesCopilot`**, then copy everything inside **`editions/copilot/core-kit/`** into that same folder.
- [ ] Open **Obsidian** -> **Open folder as vault** -> pick **`WaypostNotesCopilot`** -> go to **Settings > Community Plugins > Turn on > Browse** -> search **`Copilot`** (by Logan Yang) -> click **Install** and **Enable**.

---

## Step 2: Connect Your AI Provider Inside Obsidian (2 Minutes)

> **Any Compatible AI Works**: Waypost Notes (Copilot Edition) is pre-configured for **Google Gemini** because Google offers an easy free tier, **but you can use any AI provider or model compatible with the [Obsidian Copilot community plugin](https://github.com/logancyang/obsidian-copilot)** ([obsidiancopilot.com](https://www.obsidiancopilot.com)), including OpenAI (ChatGPT), Anthropic Claude, Groq, OpenRouter, or local offline models like Ollama / LM Studio.

- [ ] Open **[Google AI Studio](https://aistudio.google.com/apikey)** in your web browser and sign in with your Google account *(or open your preferred provider supported by Obsidian Copilot)*.
- [ ] Click **Create API Key** and copy the key (Google's free tier works great for personal vaults).
- [ ] Open **Obsidian** -> click the **Settings** gear icon (bottom left).
- [ ] Click **Community Plugins** -> if prompted, click **Turn on community plugins** -> confirm **Copilot** is toggled **ON**.
- [ ] Click **Copilot** in the left settings menu -> go to **Providers > Google Gemini** -> paste your API key and select a Gemini model (for example, **`gemini-2.5-flash`** for fast daily use).

---

## Step 3: Connect Free Granola Meeting Notes (2 Minutes)

Granola listens quietly during meetings (no awkward bot joins your call) and writes clean summaries. Waypost Notes pulls those notes straight into `00_Inbox/Granola/` so Obsidian stays your single source of truth.

- [ ] Open the **Granola** app and sign in to create your free account.
- [ ] Run this one-time sign-in command from inside your new `WaypostNotesCopilot` folder (Windows PowerShell or Mac Terminal):

```bash
python "03_Resources/Automation & Scripts/granola_sync.py" --auth
```
*(On Mac, type `python3` instead of `python`.)*

- [ ] A browser window opens -> click **Approve / Authorize**. You only need to do this once.
- [ ] Run `python "03_Resources/Automation & Scripts/granola_sync.py" --link-daily` anytime to pull new meetings into `00_Inbox/Granola/` and link them into today's Daily Note.

---

## Step 4: Run Your 5-Minute AI Setup Interview (5 Minutes)

- [ ] Inside **Obsidian**, click the **Copilot** icon in the left ribbon to open the AI chat panel.
- [ ] Type this exact command and press **Enter**:

```text
/onboard
```

- [ ] Answer the 6-8 plain-English questions (your first name, general areas of life you want to organize, and whether you prefer short checklists and step-by-step formatting).
  * *Reminder: Keep answers general and leave out sensitive personal data.*
- [ ] Copilot updates your rulebook (`AGENTS.md`), saves your profile in `06_Metadata/Gemini/Memory/`, creates your `02_Areas/` folders, and helps you start your first Daily Note.

---

## Step 5: Connect Your Phone or Tablet *(Optional, 3 Minutes)*

> **Golden Rule**: Only use **ONE** sync tool on your vault folder. Running two sync apps at the same time can cause deleted files to reappear or crash mobile Obsidian.

* **If you have a Mac + iPhone / iPad**:
  - [ ] Install **Obsidian** from the Apple App Store -> open it -> tap **`WaypostNotesCopilot`**. Because the Mac installer placed it in Apple's Obsidian iCloud folder, it syncs automatically with zero extra apps.
* **If you have a Windows PC (or Mac) + Android Phone / Tablet**:
  - [ ] Install free **Syncthing-Fork** from the Google Play Store (or F-Droid) and **Obsidian** from the Play Store.
  - [ ] On your computer, open **`http://127.0.0.1:8384`** -> click **Actions > Show ID** to display a QR code.
  - [ ] In Android **Syncthing-Fork**, tap **Devices > `+`** -> scan the QR code -> tap **Accept** when your computer asks to share the `Waypost Notes Copilot` folder.
  - [ ] Open Android **Obsidian** -> **Open folder as vault** -> pick the synced folder.
* **Need OneDrive, Google Drive, or Windows + iPhone instructions?** Open **`SYNC_GUIDE.md`** inside Obsidian.

---

## Step 6: How to Use Waypost Notes Every Day (Your 5-Minute Rhythm)

Open the **Copilot** sidebar in Obsidian and type **`/`** to pick any workflow:

### In the Morning (2 Minutes)
* Type **`/morning-plan`** and share anything on your mind.
* It creates today's Daily Note (`00_Inbox/Daily Notes/YYYY-MM-DD.md`), carries over unfinished tasks from yesterday, pulls action items from recent Granola meetings, and helps you focus on just **Top 3 Priorities**.

### During the Day (Whenever You Need Help)
* **Feeling overwhelmed by a big task?** Type **`/task-breakdown`** -> breaks it into tiny 5-15 minute steps.
* **Lost your train of thought after an interruption?** Type **`/context-restorer`** -> gives an instant "where you left off" recap.
* **Low energy or headache day?** Type **`/health-pacer`** -> logs a quick check-in and helps trim your day down to essentials.
* **Want to think through an idea first?** Type **`/thinking-partner`**.
* **Want stiff text rewritten in plain human language?** Type **`/de-aiify`**.
* **Messy notes in `00_Inbox/`?** Type **`/inbox-processor`** to sort them neatly.

### At the End of the Day (2 Minutes)
* Type **`/daily-review`** to check off completed work and roll unfinished tasks cleanly to tomorrow.

### Once a Week (Optional, 5 Minutes)
* Type **`/weekly-synthesis`** to review wins, clear stale tasks, and pick 3 focus areas for next week.

---

## Quick Troubleshooting & Comfort Tips

* **Want Light Mode instead of Dark Mode?** Open Obsidian **Settings > Appearance** -> change Base color scheme to **Light** (or toggle off **CSS snippets > `calm-slate-dark`**).
* **Reviewing AI edits**: Copilot is pre-set to show a split side-by-side preview (`autoAcceptEdits: false`) so you approve every edit before it saves.
* **Where does the AI's memory live?** Everything lives as plain readable Markdown files inside **`06_Metadata/Gemini/`** (open **`Brain_Cockpit.md`** in Obsidian anytime). You own 100% of your files.
