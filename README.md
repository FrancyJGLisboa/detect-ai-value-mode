# detect-ai-value-mode

An **agent skill** that reads a codebase and tells you *how its AI product
creates value* — and therefore how it should be positioned and sold. Point it at
your own repo or anyone else's, and it returns a sober, evidence-grounded verdict
report with every claim cited to a specific file or function.

It classifies the product against four value modes from the Enterprise AI
Adoption Framework:

| Mode | The product… | Pattern |
|------|--------------|---------|
| **Amplifier** | speeds up an existing task | copilot |
| **Substitute** | replaces a human function end to end | autonomous agent |
| **Job Creator** | enables a new professional role that did not exist | net-new |
| **Democratiser** | makes specialist work accessible to non-specialists | leveling |

This is a **skill for AI coding agents** (Claude Code, GitHub Copilot, Cursor,
Codex CLI, and anything that reads the [agentskills.io](https://agentskills.io)
open standard). It is not a standalone CLI — you install the skill into your
agent, then invoke it on a codebase.

---

## Install (about 20 seconds)

Copy the skill folder into your agent's skills directory. Keep the folder name
exactly `detect-ai-value-mode-from-codebase` (the skill name must match its folder).

```bash
git clone https://github.com/FrancyJGLisboa/detect-ai-value-mode.git

# Claude Code — personal (available in every project):
cp -R detect-ai-value-mode/detect-ai-value-mode-from-codebase ~/.claude/skills/

# …or project-scoped (just this repo):
cp -R detect-ai-value-mode/detect-ai-value-mode-from-codebase .claude/skills/
```

Other agents use the same folder, different location:

| Agent | Personal path | Project path |
|-------|---------------|--------------|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.github/skills/` |
| Cursor / Codex / others | `~/.agents/skills/` | `.agents/skills/` |

Restart or reload your agent so it picks up the new skill.

---

## Run it on a codebase

Inside your agent, invoke the skill with a target. Three ways to point it:

```text
# 1. Your own codebase — run from inside the project
cd ~/work/my-ai-product
/detect-ai-value-mode-from-codebase .

# 2. Any local path (your machine, doesn't need to be the current dir)
/detect-ai-value-mode-from-codebase ~/work/some-other-repo

# 3. Someone else's codebase by URL (it shallow-clones, reads, discards)
/detect-ai-value-mode-from-codebase https://github.com/org/their-repo
```

You can also just **describe the intent** in natural language and the agent will
trigger the skill from its description — e.g. *"what value mode is this codebase?"*
or *"read this repo and tell me how it creates value and who the buyer is."*
Pasting or uploading code works too.

### What you get (excerpt)

```text
VERDICT: SUBSTITUTE (primary) / AMPLIFIER (secondary)   Confidence: MODERATE

This product replaces a human triage function rather than accelerating one.
The evidence is in agents/triage.py, where classify_and_route() acts on model
output with no human-in-the-loop checkpoint in the normal path; the approval
gate in review.py:guard() is exercised only on the low-confidence branch...
```

Full scoring rubric: [`references/value_modes.md`](detect-ai-value-mode-from-codebase/references/value_modes.md).
Exact report schema: [`references/verdict_schema.md`](detect-ai-value-mode-from-codebase/references/verdict_schema.md).

---

## Repository layout

```
detect-ai-value-mode/
├── detect-ai-value-mode-from-codebase/   ← the skill (this is what you install)
│   ├── SKILL.md                          ← instructions + metadata the agent reads
│   ├── evals.yaml                        ← trigger eval set (should-fire / should-not-fire)
│   └── references/                       ← scoring rubric + report schema
└── tools/
    └── validate_skill.py                 ← pre-publish validator + trigger-eval harness
```

## Validate before you change it

The skill ships green against the agentskills.io standard and the Anthropic
importer. If you fork or edit it, re-check with the bundled validator (zero
install — `uv` resolves its one dependency on first run):

```bash
uv run tools/validate_skill.py detect-ai-value-mode-from-codebase

# also score trigger reliability (needs an Anthropic key):
ANTHROPIC_API_KEY=sk-... uv run tools/validate_skill.py detect-ai-value-mode-from-codebase --eval
```

See [`tools/README.md`](tools/README.md) for the full gate list and CI wiring.

---

## Attribution & license

The four value modes are drawn from the Enterprise AI Adoption Framework
attributed to **Derley Morais (Iron Flow)**. This repository packages that
framework as a repeatable analysis workflow; the framework itself remains the
property of its author.

Skill packaging and tooling: **MIT** — see [`LICENSE`](LICENSE).
