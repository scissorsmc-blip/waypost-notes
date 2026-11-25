---
type: guide
title: Android Termux Optional Automation Guide (Waypost Notes (Copilot Edition))
tags:
  - android
  - termux
  - mobile
  - guide
---

# Android Optional Automation Guide (Full Kit)

Because **Obsidian Copilot** runs natively inside Obsidian on Android, iPhone, and iPad (`isDesktopOnly: false`), you do **NOT** need Termux just to chat with Gemini on mobile.

Install this optional Termux pack only if you also want Android **Share Sheet** web/PDF capture or one-tap home-screen sync widgets for Calendar, Granola, Google Tasks, and YNAB.

---

## 1. Install Optional Android Apps (F-Droid)
1. **Obsidian** (Google Play Store) synced to your cloud folder (Obsidian Sync, OneSync, or FolderSync)
2. **Termux** (from F-Droid)
3. **Termux:Widget** (from F-Droid)

## 2. Link Your Vault & Run the One-Line Installer
```bash
termux-setup-storage
ln -s ~/storage/shared/Obsidian/WaypostNotesCopilot ~/vault
bash ~/vault/"03_Resources/Automation & Scripts/termux/install_termux_pack.sh"
```
