# Waypost Notes: Beginner's Start-to-Finish Guide

Welcome. This guide walks you step by step from zero to a working, calm, organized personal workspace using **Obsidian** (your notes), **Google Antigravity** (your AI assistant), and **Granola** (your meeting note-taker).

You do **not** need a technical background. Take it one step at a time, check off boxes as you go, and take breaks whenever you need them.

---

## Important Disclaimer & Privacy Warning (Please Read First)

* **Free & Provided "As-Is"**: Waypost Notes is shared **free of charge** under the MIT License for personal and educational use. It is provided **"as is," with no warranties, guarantees, or promises of uptime, accuracy, or fitness for any specific purpose**. The creators are not responsible for data loss, sync issues, or decisions made using this system. Waypost Notes is an independent community project and is **not** officially affiliated with Obsidian, Google, Granola, Microsoft, Apple, or any government agency.
* **Not Medical, Legal, or Financial Advice**: AI assistants can make mistakes or invent details. Never rely solely on AI output for medical, VA/disability benefit, legal, tax, or financial decisions. Always confirm important information with a qualified human professional.
* **Public Cloud AI Privacy Warning**: While your notes are stored as plain files on your own computer, **anything you type into the AI chat or ask the AI to read is sent to a public cloud AI service (Google Gemini / Google Antigravity)** to generate answers.
  * **DO NOT** put highly sensitive personal information into notes that you ask the AI to read.
  * Keep the following **OUT** of AI chats and AI-accessible notes: Social Security numbers, bank or credit card numbers, passwords or PINs, sensitive medical or VA claim records, private legal case files, and confidential employer or client data.

---

## Before You Start (2 Minutes)

Make sure you have:
- [ ] A **Windows 10/11 PC** or a **Mac**
- [ ] A free **Google account** (Gmail)
- [ ] About **10 to 15 minutes**

**Tip on Core Kit vs. Full Kit**: During Step 1, the installer asks if you want the **Core Kit** or **Full Kit**.
* Choose **`1` (Core Kit)** if you want the simplest, cleanest setup to start. You can always add extras later.

---

## Step 1: Download & Install Waypost Notes (5 Minutes)

### On Windows 10 / 11
- [ ] Press the **Windows key** on your keyboard.
- [ ] Type **`PowerShell`** and click **Windows PowerShell**.
- [ ] Copy this exact line, paste it into the blue/black window (right-click to paste), and press **Enter**:

```powershell
irm https://raw.githubusercontent.com/scissorsmc-blip/waypost-notes/main/installers/install-antigravity-windows.ps1 | iex
```

- [ ] Answer the 3 simple prompts on screen:
  1. **Kit**: Press **`1`** (Core Kit) and hit Enter.
  2. **Device Sync**: Press **`1`** if you have an Android phone/tablet (free Syncthing), **`2`** for OneDrive, or **`3`** for this PC only.
  3. **Folder Location**: Press **Enter** to accept the recommended folder.

### On Mac
- [ ] Press **Command + Space**, type **`Terminal`**, and press **Enter**.
- [ ] Copy this exact line, paste it into Terminal, and press **Enter**:

```bash
curl -fsSL https://raw.githubusercontent.com/scissorsmc-blip/waypost-notes/main/installers/install-antigravity-mac.sh | bash
```

- [ ] Answer the 3 simple prompts on screen:
  1. **Kit**: Press **`1`** (Core Kit) and hit Enter.
  2. **Device Sync**: Press **`1`** if you use an iPhone/iPad (automatic free Apple iCloud), **`2`** for Android/Windows (free Syncthing), or **`3`** for Mac only.
  3. **Folder Location**: Press **Enter** to accept the recommended folder.

### Prefer No Terminal Commands At All? (3-Click Alternative)
- [ ] Download and install **[Obsidian](https://obsidian.md)**, **[Google Antigravity](https://antigravity.google)**, and **[Granola](https://www.granola.ai)** directly from their websites.
- [ ] On GitHub, click the green **`<> Code`** button -> **Download ZIP** -> unzip it -> move the **`core-kit`** folder into your Documents, OneDrive, or iCloud folder and rename it **`WaypostNotes`**, then copy everything inside **`editions/antigravity/core-kit/`** into that same folder (and copy `06_Metadata/Gemini/Skills/` into `.agents/skills/`).
- [ ] Open **Obsidian** -> click **Open folder as vault** -> pick **`WaypostNotes`**.

---

## Step 2: Connect Free Granola Meeting Notes (2 Minutes)

Granola listens quietly during meetings (no awkward bot joins your call) and writes clean summaries. Waypost Notes pulls those notes straight into `00_Inbox/Granola/` so you never forget what was decided.

- [ ] Open the **Granola** app and sign in to create your free account.
- [ ] Run this one-time sign-in command from inside your new `WaypostNotes` folder (Windows PowerShell or Mac Terminal):

```bash
python "03_Resources/Automation & Scripts/granola_sync.py" --auth
```
*(On Mac, type `python3` instead of `python`.)*

- [ ] A browser window opens -> click **Approve / Authorize**. You only need to do this once.
- [ ] From now on, whenever you run `/morning-plan` or `/daily-review` (or run `granola_sync.py --link-daily`), your meetings sync into Obsidian automatically.

---

## Step 3: Run Your 5-Minute AI Setup Interview (5 Minutes)

Now connect your vault to your AI assistant so it learns how you like to work.

- [ ] Open **Google Antigravity** and sign in with your Google account.
- [ ] Click **Open Folder** and select your new **`WaypostNotes`** folder.
- [ ] In the chat box, type this exact command and press **Enter**:

```text
/onboard
```

- [ ] Answer the 6-8 plain-English questions (your first name, general areas of life you want to organize, and whether you prefer short checklists and step-by-step formatting).
  * *Reminder: Keep answers general and leave out sensitive personal data.*
- [ ] Antigravity automatically updates your rulebook (`AGENTS.md`), creates your personal folders in `02_Areas/`, and sets up your first Daily Note.

---

## Step 4: Connect Your Phone or Tablet *(Optional, 3 Minutes)*

> **Golden Rule**: Only use **ONE** sync tool on your vault folder. Running two sync apps at the same time can cause deleted files to reappear.

* **If you have a Mac + iPhone / iPad**:
  - [ ] Install **Obsidian** from the Apple App Store -> open it -> tap **`WaypostNotes`**. Because the Mac installer placed it in Apple's Obsidian iCloud folder, it syncs automatically with zero extra apps.
* **If you have a Windows PC (or Mac) + Android Phone / Tablet**:
  - [ ] Install free **Syncthing-Fork** from the Google Play Store (or F-Droid) and **Obsidian** from the Play Store.
  - [ ] On your computer, open **`http://127.0.0.1:8384`** -> click **Actions > Show ID** to display a QR code.
  - [ ] In Android **Syncthing-Fork**, tap **Devices > `+`** -> scan the QR code -> tap **Accept** when your computer asks to share the `Waypost Notes` folder.
  - [ ] Open Android **Obsidian** -> **Open folder as vault** -> pick the synced folder.
* **Need OneDrive, Google Drive, or Windows + iPhone instructions?** Open **`SYNC_GUIDE.md`** inside Obsidian.

---

## Step 5: How to Use Waypost Notes Every Day (Your 5-Minute Rhythm)

You do not need to memorize dozens of features. Just use these simple commands inside **Google Antigravity** (and view/edit your notes anytime in **Obsidian**):

### In the Morning (2 Minutes)
* Type **`/morning-plan`** (or just say **"good morning"**).
* Tell it anything on your mind in plain English.
* It creates today's Daily Note (`00_Inbox/Daily Notes/YYYY-MM-DD.md`), rolls over unfinished tasks from yesterday, pulls recent Granola meeting action items, and helps you pick just **Top 3 Priorities** so you do not get overwhelmed.

### During the Day (Whenever You Need Help)
* **Feeling overwhelmed by a big task?** Type **`/task-breakdown`** and describe the task. It breaks it into tiny 5-15 minute steps.
* **Lost your train of thought after an interruption?** Type **`/context-restorer`** and name the project. It gives you an instant "where you left off" recap.
* **Low energy or headache day?** Type **`/health-pacer`** and share how you feel. It logs a quick note and helps trim your day down to essentials.
* **Want to brainstorm before writing?** Type **`/thinking-partner`**.
* **Want a draft rewritten in natural, plain English?** Type **`/de-aiify`**.
* **Messy notes piling up in `00_Inbox/`?** Type **`/inbox-processor`** to file everything neatly.

### At the End of the Day (2 Minutes)
* Type **`/daily-review`** (or just say **"good night"**).
* It checks off what you finished, moves unfinished tasks cleanly to tomorrow so nothing is forgotten, and archives old daily notes automatically.

### Once a Week (Optional, 5 Minutes)
* Type **`/weekly-synthesis`** to review your wins, clear stale tasks, and pick 3 focus areas for next week.

---

## Quick Troubleshooting & Comfort Tips

* **Want Light Mode instead of Dark Mode?** Open Obsidian **Settings > Appearance** -> change Base color scheme to **Light** (or toggle off **CSS snippets > `calm-slate-dark`**).
* **Worried about accidentally losing an edit?** Before major edits to existing notes, Waypost Notes saves timestamped backup copies in **`06_Metadata/Gemini/Backups/`**.
* **Where does the AI's memory live?** Everything lives as normal readable Markdown files inside **`06_Metadata/Gemini/`** (open **`Brain_Cockpit.md`** inside Obsidian to browse it anytime). You own 100% of your files.
