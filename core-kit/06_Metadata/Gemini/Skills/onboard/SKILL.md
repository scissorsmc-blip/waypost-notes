---
name: onboard
description: Friendly 5-minute interactive setup interview for new Calm Slate users. Personalizes AGENTS.md, creates life/work Areas, sets accessibility preferences, and launches the first Daily Note. Triggered by "/onboard" or "start my setup interview".
---

# Vault Setup Interview (`/onboard`)

Guide a brand-new user through personalizing their Calm Slate (Obsidian + Google Antigravity) vault in plain, warm, jargon-free English.

## Interview Rules
* Ask **one or two short questions at a time** so the user never feels overwhelmed.
* Keep explanations plain and friendly (assume the user is non-technical).
* Never invent personal details. Only record what the user tells you.

## Step-by-Step Interview Sequence

1. **Welcome & Basics**:
   * Ask for their preferred name, timezone, and a one-sentence description of what they do day-to-day (work, school, volunteering, caregiving, small business, etc.).
2. **Life & Work Areas (`02_Areas/`)**:
   * Ask what 3 to 5 ongoing areas of life they want to keep organized (for example: Work, Family, Health, Finance, Creative Projects, Community/Board work).
   * Confirm the folder names before creating them under `02_Areas/`.
3. **Communication & Accessibility Preferences**:
   * Ask how they like information formatted:
     - Short chunked headers and checklists (great for ADHD, TBI, or busy schedules) vs. narrative paragraphs.
     - Direct and concise vs. warm and conversational.
     - Whether they want an optional daily Energy/Health check-in inside their Daily Note.
4. **Daily Briefing Preferences**:
   * Ask if they want `/morning-plan` to fetch 2-3 daily headlines on any topics they care about (for example: tech, finance, parenting, local news, or none).
5. **Optional Add-Ons Check**:
   * Mention that if they installed the **Full Kit**, they can later turn on Calendar sync, Granola meeting notes, Google Tasks, or YNAB whenever they are ready (no pressure during setup).

## Automatic Vault Wiring (After Answers Are Confirmed)

1. Save a backup of the template `AGENTS.md` to `06_Metadata/Gemini/Backups/`.
2. Update `AGENTS.md` and mirror it identically to `.agents/rules/AGENTS.md` with the user's profile, tone, accessibility preferences, and daily briefing topics.
3. Create the user's chosen folders under `02_Areas/` with a brief `Overview.md` index note in each.
4. Update `06_Metadata/Templates/Daily Note Template.md` so its `## Tasks by Domain` headings match the user's real Areas.
5. Update `06_Metadata/Gemini/Brain_Cockpit.md` to mark onboarding complete with today's ISO date.
6. Offer to run their very first **`/morning-plan`** right away.
