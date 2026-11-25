# Health Pacer (`/health-pacer`)

Log health/energy check-ins quickly and pace today's workload to match real stamina.

## Execution Sequence

1. **Capture Check-In**:
   * Log any metrics the user shares (energy 1-5, sleep, headaches, pain 0-10, blood pressure, stress, medications, or notes) into the `## Energy & Health Check` section of today's Daily Note (`00_Inbox/Daily Notes/YYYY-MM-DD.md`).
2. **Pace the Day**:
   * **High Energy (4-5)**: Tackle complex or deep-focus priorities first.
   * **Moderate Energy (3)**: Keep to Top 3 Priorities; batch admin tasks.
   * **Low Energy / Flare (1-2)**: Proactively suggest deferring non-urgent tasks to tomorrow, narrowing today down to 1 essential win, and keeping replies ultra-short.
3. **Spot Patterns (When Asked)**:
   * Review the past 7-14 Daily Notes to surface trends between sleep, stress, symptoms, and energy.

---
*Follow `AGENTS.md` and `06_Metadata/Gemini/System-Prompts/Waypost Operating Rules.md`. Include `[[WikiLinks]]` to referenced notes and keep `06_Metadata/Gemini/` updated.*
