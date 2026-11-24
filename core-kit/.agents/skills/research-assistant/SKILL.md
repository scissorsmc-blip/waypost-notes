---
name: research-assistant
description: Structured research combining internal vault knowledge first and targeted web search second, formatted as a clean executive briefing.
---

# Research Assistant (`/research-assistant`)

Deliver objective, high-signal research grounded in both the user's vault and verified external sources.

## Execution Sequence

1. **Audit Internal Vault First**:
   * Search `01_Projects/`, `02_Areas/`, `03_Resources/`, and `06_Metadata/Gemini/` to see what the user has already gathered and avoid duplicating work.
2. **Fetch External Facts**:
   * Run targeted web searches for primary documentation, current pricing/rules, or authoritative references.
3. **Format as a Clean Briefing**:
   * **Executive Summary**: 3-5 bullet takeaways in plain language.
   * **Key Details & Comparison**: Tables, steps, or pros/cons where helpful.
   * **Recommended Next Steps**: Concrete actions or decisions.
   * **Sources & References**: Explicit `[[WikiLinks]]` for internal notes and direct URLs for external sources.
4. **Offer to Save**:
   * Offer to save the briefing under `03_Resources/` or `06_Metadata/Gemini/Artifacts/` and link it into `Brain_Cockpit.md`.
