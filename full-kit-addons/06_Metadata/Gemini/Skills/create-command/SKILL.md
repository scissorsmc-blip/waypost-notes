---
name: create-command
description: Interactive workflow builder that helps the user design and save their own custom /commands and skills in 06_Metadata/Gemini/Skills/.
---

# Create Command (`/create-command`)

Help the user turn any recurring workflow into a reusable custom `/command` skill without writing code.

## Execution Sequence
1. Ask 3 simple questions:
   * What should trigger this command (e.g. `/weekly-meal-plan`)?
   * What inputs will you give it, and what should the finished output look like?
   * Which vault folder (if any) should it read from or save to?
2. Draft the new `SKILL.md` file cleanly in `06_Metadata/Gemini/Skills/<command-name>/SKILL.md` and mirror it to `.agents/skills/<command-name>/SKILL.md`.
3. Add a one-line entry to `AGENTS.md` (and `.agents/rules/AGENTS.md`) so the assistant always knows about the new command.
4. Run a quick test with the user to make sure it behaves the way they want.
