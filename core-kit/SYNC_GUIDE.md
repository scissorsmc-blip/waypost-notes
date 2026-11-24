---
type: guide
title: Simple Device Sync Guide (Zero Zombie Files)
tags:
  - sync
  - guide
  - mobile
  - accessibility
---

# Simple, Reliable Device Sync Guide

> **Golden Rule (Read First)**: Use **ONLY ONE** sync method on your vault folder. Never run two sync tools (such as OneSync + Remotely Save) against the same folder at the same time - that is what causes deleted files to reappear and can crash mobile Obsidian.

Pick your device combination below and follow the 3 numbered steps once. After setup, syncing happens automatically in the background.

---

## Option A: Mac + iPhone / iPad *(100% Free, Zero Extra Apps)*

Obsidian natively supports Apple iCloud Drive on Mac, iPhone, and iPad.

1. **On your Mac**: Put your vault folder inside Obsidian's official iCloud folder *(the Calm Slate Mac installer does this automatically when you pick Option 1)*:
   `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/`
2. **On your iPhone / iPad**: Install **Obsidian** from the App Store -> open Obsidian -> tap your synced vault (it appears automatically from iCloud).
3. **Important Warning**: Do **not** use iCloud Drive if your primary computer is Windows (iCloud for Windows causes duplicate/conflicted vault files).

---

## Option B: Windows or Mac + Android Phone / Tablet *(Recommended - 100% Free, Private, Zero Zombie Files)*

Uses **Syncthing** on your computer and **Syncthing-Fork** on Android. Notes sync directly device-to-device with encryption (never stored on third-party servers), deleted files stay deleted, and Obsidian never crashes.

1. **On your Computer**: Choose **Syncthing** during the Calm Slate installer. It installs Syncthing, starts it silently in the background, applies the pre-built `.stignore` file, registers your vault folder, and opens `http://127.0.0.1:8384` (click **Actions > Show ID** for your QR code).
2. **On your Android Phone / Tablet**:
   * Install free **Syncthing-Fork** (Google Play Store or F-Droid).
   * Open Syncthing-Fork -> **Devices** tab -> tap **`+`** -> scan the QR code on your computer screen -> tap **Save**.
   * When your computer pops up a banner asking to add the phone and share your vault folder, tap **Add Device** / **Accept**.
3. **In Android Obsidian**: Open Obsidian -> **Open folder as vault** -> pick the synced folder. Done forever.

*(Optional Cloud Backup: You can still keep your Windows vault inside OneDrive with "Always keep on this device" enabled as a passive cloud backup while Syncthing handles PC <-> Android sync.)*

---

## Option C: Windows + Android Using OneDrive or Google Drive *(No Remotely Save)*

If you prefer OneDrive or Google Drive as your sync hub instead of Syncthing:

1. **On Windows**: Keep your vault inside OneDrive or Google Drive for Desktop, right-click the folder, and choose **Always keep on this device**.
2. **On Android**: Install **FolderSync** (or **OneSync** / **DriveSync**) - **never** enable Obsidian's Remotely Save plugin at the same time.
3. **Turn on 3 Required Settings** inside your Android sync app:
   * Sync Type: **Two-way**
   * **Sync Deletions**: **ON** (prevents deleted files from reappearing)
   * Ignore folders: `.obsidian/workspace*.json`, `.trash`, `06_Metadata/Gemini/Debug-Logs`, `06_Metadata/Gemini/Backups`

---

## Option D: Windows PC + iPhone / iPad

Apple restricts third-party background folder sync on iOS, so there is no zero-friction free background folder sync between Windows and iPhone.

* **Simplest, Zero-Stress Choice**: **[Obsidian Sync](https://obsidian.md/sync)** ($4/month Standard). Built directly into Obsidian, works across Windows, Mac, iPhone, iPad, and Android with end-to-end encryption and zero troubleshooting.
