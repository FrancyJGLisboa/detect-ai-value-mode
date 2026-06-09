# detect-ai-value-mode-from-codebase

An agent skill that reads a codebase and tells you **how its AI product creates
value** — and therefore how it should be positioned and sold.

It classifies the product against four value modes from the Enterprise AI
Adoption Framework and returns a sober, evidence-grounded verdict report (plain
prose, every claim cited to a file or function — no hype, no emojis):

- **Amplifier** — AI speeds up an existing task (the copilot pattern)
- **Substitute** — AI replaces a human function end to end (the agentic pattern)
- **Job Creator** — AI enables a new professional role that did not exist before
- **Democratiser** — AI makes specialist work accessible to non-specialists

## Install

Drop this folder (keep the name `detect-ai-value-mode-from-codebase`) into a
skills directory your agent reads:

- Project-scoped: `.claude/skills/`, `.github/skills/`, or `.agents/skills/`
- Personal-scoped: `~/.claude/skills/`, `~/.copilot/skills/`, or `~/.agents/skills/`

Works with any agent that supports the [agentskills.io](https://agentskills.io)
open SKILL.md standard — Claude Code, GitHub Copilot, Cursor, Codex CLI, and others.

## Use

```
/detect-ai-value-mode-from-codebase .
/detect-ai-value-mode-from-codebase https://github.com/org/repo
```

Or just ask in natural language, e.g. *"what value mode is this codebase?"* —
the skill triggers from its description. You can also paste or upload code.

## What you get (excerpt)

```
VERDICT: SUBSTITUTE (primary) / AMPLIFIER (secondary)   Confidence: MODERATE

This product replaces a human triage function rather than accelerating one.
The evidence is in agents/triage.py, where classify_and_route() acts on model
output with no human-in-the-loop checkpoint in the normal path; the approval
gate in review.py:guard() is exercised only on the low-confidence branch...
```

See `references/value_modes.md` for the full scoring rubric and
`references/verdict_schema.md` for the exact report schema.

## Attribution

The four value modes are drawn from the Enterprise AI Adoption Framework
attributed to **Derley Morais (Iron Flow)**. This skill packages that framework
as a repeatable analysis workflow; the framework itself remains the property of
its author. See `LICENSE` for details.

## License

MIT (skill packaging) — see [`LICENSE`](LICENSE).
