---
type: guide
title: Calm Slate - Android & Samsung System Theme Guide
tags:
  - android
  - samsung
  - theme
  - dark-mode
  - accessibility
  - cognitive-comfort
---

# Calm Slate & Warm Ink: System-Wide Android & Samsung Theme Guide

A unified, low-glare, cognitive-friendly dark theme spanning **Android / One UI**, **Samsung Good Lock (Theme Park)**, **Chrome**, **Obsidian**, and **Termux** across both tablets and phones.

Designed to:
* Eliminate pure-black (`#000000`) OLED halation and pure-white (`#FFFFFF`) glare.
* Lower blue-light load and visual motion triggers for eye-strain and headache comfort.
* Reduce home-screen visual clutter and executive-function friction.

---

## 1. Master Hex Palette (Copy-Paste Reference)

Use these exact hex codes inside **Samsung Good Lock > Theme Park** so every menu, toggle, notification card, keyboard key, and app matches Obsidian and Termux:

| Role | Hex Code | Visual Look |
| :--- | :---: | :--- |
| **Primary Background** | `#191816` | Warm deep charcoal (anti-halation) |
| **Card / Notification Surface** | `#22201D` | Elevated warm slate |
| **Divider / Subtle Border** | `#312E28` | Soft charcoal line |
| **Primary Text** | `#DDD8CE` | Warm cream-gray (crisp, zero glare) |
| **Secondary / Subtext** | `#A69F93` | Muted warm stone |
| **Primary Accent (Active Toggles / Highlights)** | `#8FBC9F` | Calm sage green |
| **Secondary Accent (Selected / Focus / Badges)** | `#CFA085` | Warm sand / terracotta |
| **Alert / Warning** | `#C97B72` | Muted clay red (never neon) |
| **Keyboard Key Surface** | `#262420` | Soft matte dark keycaps |
| **Keyboard Function Keys** | `#1F1D1A` | Subtle contrast shift |

---

## 2. Included Wallpapers (`05_Attachments/Themes/CalmSlate/`)

**Dark Misty Smoky Mountains (Photographic Matte Edition - Recommended)**:
* Tablet (Landscape): [[CalmSlate_SmokyMountains_Tablet.jpg]]
* Phone (Portrait): [[CalmSlate_SmokyMountains_Phone.jpg]]

**Minimalist Matte Vector Edition**:
* Tablet Home Screen: [[CalmSlate_Tablet_Home.png]]
* Phone Home Screen: [[CalmSlate_Phone_Home.png]]
* Lock Screen (Tablet & Phone): [[CalmSlate_Lock.png]]

---

## 3. Step-by-Step System-Wide Setup (Tablet & Phone)

### Step A: Wallpaper & System Color Palette (2 Minutes)
1. Save or copy your chosen wallpaper from `05_Attachments/Themes/CalmSlate/` into your device Gallery.
2. Open **Settings > Wallpaper and style > Change wallpapers > Gallery** and apply to **Home screen** and **Lock screen**.
3. Turn ON **Dim wallpaper when Dark mode is on**.
4. Tap **Color palette** -> toggle **ON** -> pick the **warm charcoal / sage / sand** palette extracted from the wallpaper -> toggle **Apply palette to app icons** ON.

### Step B: Display & Cognitive Comfort Settings (2 Minutes)
1. **Settings > Display > Dark**: Set to **Dark** (Always On).
2. **Settings > Display > Eye comfort shield**: Turn **ON** -> **Custom** (gentle warm tint around 35-45%).
3. **Settings > Accessibility > Vision enhancements**:
   * Turn **Reduce transparency and blur** **ON**.
   * Turn **Reduce animations** **ON**.
   * Pin **Extra dim** to Quick Settings for 1-tap headache/migraine dimming.

### Step C: Full System Theme via Samsung Good Lock -> Theme Park (4 Minutes)
Install free **Good Lock** from the **Galaxy Store** -> install **Theme Park** -> create each section with **Dark Mode (moon icon)** selected:

1. **Theme** (save as `Calm Slate` -> Apply):
   * Background: `191816` | Surface / Cards: `22201D` | Text: `DDD8CE`
   * Primary Accent: `8FBC9F` | Secondary Accent: `CFA085`
2. **Quick Panel** (save as `Calm Slate Panel` -> Apply):
   * Panel Backdrop: `151412` | Cards: `22201D` | Active Icons: `8FBC9F` | Inactive: `787268` | Brightness Slider: `CFA085`
3. **Keyboard** (save as `Calm Slate Keys` -> Apply):
   * Background: `191816` | Main Keys: `262420` | Function Keys: `1F1D1A` | Labels: `DDD8CE` | Action Key: `8FBC9F`
4. **Icons** *(Optional)*: Rounded square (squircle) with `#24221E` dark slate tray.

### Step D: Dark Mode for White Websites (Chrome)
1. Open Chrome -> go to `chrome://flags` -> search **`Auto Dark Mode for Web Contents`**.
2. Set to **Enabled with selective inversion of non-image elements** -> **Relaunch**.

### Step E: One-Tap "Low-Stim / Recovery Mode" (Samsung Modes & Routines)
1. Open **Settings > Modes and Routines > Add mode** -> name it **`Low-Stim / Recovery`**.
2. Add actions: **Do Not Disturb** (allow family/emergency contacts only), **Brightness 25%**, **Extra Dim ON**, **Eye Comfort Shield ON** (warm).
3. Add the **Modes** tile to your Quick Settings shade for 1-tap relief.
