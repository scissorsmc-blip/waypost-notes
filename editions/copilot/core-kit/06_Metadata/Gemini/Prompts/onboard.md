# Vault Setup Interview (`/onboard`)

Guide a brand-new user through personalizing their **Waypost Notes (Copilot Edition)** vault inside Obsidian in plain, warm, jargon-free English.

## Interview Rules
* Ask **one or two short questions at a time** so the user never feels overwhelmed.
* Keep explanations plain and friendly (assume the user is non-technical).
* Never invent personal details. Only record what the user tells you.

## Step-by-Step Interview Sequence

1. **Welcome & Basics**:
   * Ask for their preferred name, timezone, and a one-sentence description of what they do day-to-day (work, school, caregiving, volunteering, small business, etc.).
2. **Life & Work Areas (`02_Areas/`)**:
   * Ask what 3 to 5 ongoing areas of life they want to keep organized (for example: Work, Family, Health, Finance, Creative Projects).
   * Confirm the folder names before creating them under `02_Areas/`.
3. **Communication & Accessibility Preferences**:
   * Ask how they like information formatted:
     - Short chunked headers and checklists (great for ADHD, TBI, or busy schedules) vs. narrative paragraphs.
     - Direct and concise vs. warm and conversational.
     - Whether they want an optional daily Energy/Health check-in inside their Daily Note.
4. **Daily Briefing Preferences**:
   * Ask if they want `/morning-plan` to cover any specific topics or reminders.
5. **Optional Full-Kit Check**:
   * Mention that if they installed the **Full Kit**, they can later turn on Calendar sync, Granola meeting notes, Google Tasks, or YNAB from `FULL_KIT_GUIDE.md` whenever they are ready.

## Automatic Vault Wiring (After Answers Are Confirmed)

1. Update `AGENTS.md` with the user's profile, tone, accessibility preferences, and life/work areas.
2. Add a concise 4-6 bullet **User Context Summary** at the bottom of `06_Metadata/Gemini/System-Prompts/Waypost Operating Rules.md` and save a clean baseline memory note in `06_Metadata/Gemini/Memory/User Profile.md`.
3. Create the user's chosen folders under `02_Areas/` with a short `Overview.md` note in each.
4. Update `06_Metadata/Templates/Daily Note Template.md` so its `## Tasks by Domain` headings match the user's real Areas.
5. Update `06_Metadata/Gemini/Brain_Cockpit.md` to mark onboarding complete with today's ISO date.
6. Offer to run their very first **`/morning-plan`** right away.

---
*Follow `AGENTS.md` and `06_Metadata/Gemini/System-Prompts/Waypost Operating Rules.md`. Include `[[WikiLinks]]` to referenced notes and keep `06_Metadata/Gemini/` updated.*
