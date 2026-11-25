---
type: guide
title: Android Termux Mobile Setup Guide
tags:
  - android
  - termux
  - mobile
  - guide
---

# Android Tablet & Phone Setup Guide (Optional Power-Up)

Run your Waypost Notes vault + Google Antigravity CLI (`agy`) on Android tablets and phones with one-tap home-screen widgets and Share Sheet capture.

---

## 1. Install Required Android Apps

1. **Obsidian** (Google Play Store)
2. **A Cloud Sync App** (Obsidian Sync, OneSync, or FolderSync) synced to a local folder such as `Internal Storage/Obsidian/WaypostNotes`
3. **Termux** (install from **F-Droid**, not Google Play)
4. **Termux:Widget** (from F-Droid - adds one-tap home-screen shortcuts)
5. *(Optional)* **Termux:API** (from F-Droid - enables Gallery media scanning and Android notifications)

---

## 2. Link Your Vault & Run the One-Line Installer

Open **Termux** and run:

```bash
termux-setup-storage
ln -s ~/storage/shared/Obsidian/WaypostNotes ~/vault
curl -fsSL https://antigravity.google/cli/install.sh | bash
bash ~/vault/"03_Resources/Automation & Scripts/termux/install_termux_pack.sh"
```

*(Adjust `~/storage/shared/Obsidian/WaypostNotes` to match your synced vault folder path.)*

---

## 3. Finish Setup (2 Minutes)

1. **Disable Battery Optimization**: Android **Settings > Apps > Termux > Battery > Unrestricted** (repeat for **Termux:Widget**).
2. **Add Home-Screen Widget**: Long-press your home screen -> **Widgets > Termux:Widget** -> place the 4x2 list widget to get instant one-tap buttons for Daily Note, Health Log, Expense Log, Sync, and Launch Antigravity.
3. **Share Sheet Capture**: Share any link from Chrome or any PDF from email -> choose **Termux** -> automatically saved into `00_Inbox/`.
