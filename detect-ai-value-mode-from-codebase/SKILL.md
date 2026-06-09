---
name: detect-ai-value-mode-from-codebase
description: >
  Analyse a codebase to determine which of the four AI product value modes it
  embodies — Amplifier, Substitute, Job Creator, or Democratiser — and produce a
  sober, evidence-grounded verdict report in plain prose (Unicode text only, no
  emojis). Use this skill when the user wants to understand the strategic
  positioning or business model of an AI product by reading its code: triggers
  include "what mode is this", "detect AI value mode", "which quadrant does this
  fall into", "classify my AI product", or any pairing of a codebase path or
  pasted code with a question about how the product creates value, who its buyer
  is, or how it should be positioned. Trigger even when the user does not name
  the four modes explicitly — intent to classify an AI product from its code is
  sufficient.
license: MIT
metadata:
  version: "1.0.0"
  author: Francy Lisboa Charuto
---

# detect-ai-value-mode-from-codebase

## Purpose

This skill reads a codebase — or a significant excerpt thereof — and produces a
structured verdict report that classifies the product against the four AI value
modes defined in the enterprise AI adoption framework. The report is written in
plain prose, uses only Unicode text (no emojis, no markdown decorations beyond
headers and horizontal rules), and is designed to be sober and directly useful
in a product strategy or sales conversation.

The four modes are defined in full in `references/value_modes.md`. Load that
file before beginning the analysis. The verdict report schema and scoring rubric
are in `references/verdict_schema.md`. Load that file before writing the report.

---

## Workflow

### Step 0 — Locate the codebase

The skill accepts three input forms. Detect which one is present and act
accordingly before doing anything else.

**Form A — Dot or local path**

The user types `.` or a local filesystem path (absolute or relative).

```bash
# List the tree first to understand scope
find . -type f | grep -v -E '(\.git|node_modules|__pycache__|\.pyc|dist/|build/)' | head -150

# Then read selectively in this priority order:
# 1. Entry points: main.py, index.ts, app.py, cli.py, server.py, cmd/main.go
# 2. AI integration layer: any file importing openai, anthropic, langchain,
#    llamaindex, huggingface, litellm, or similar
# 3. Agent/tool definitions: tools.py, tools.ts, agents/, functions/
# 4. Prompt files: prompts/, system_prompts/, *.txt in root, *.md in prompts/
# 5. Configuration: config.yaml, .env.example, settings.py, config.ts
# 6. User interface: routes/, api/, ui/, components/, cli/
# 7. README.md and any docs/ files that describe the product's purpose
```

**Form B — GitHub or GitLab URL**

The user provides a URL of the form:
`https://github.com/org/repo` or `https://gitlab.com/org/repo`

Clone to a temporary directory and proceed as Form A:

```bash
git clone --depth=1 <url> /tmp/assess-$(date +%s)
cd /tmp/assess-<timestamp>
find . -type f | grep -v -E '(\.git|node_modules|__pycache__|\.pyc|dist/|build/)' | head -150
# then follow Form A priority read order
```

If the URL includes a branch or subdirectory
(`https://github.com/org/repo/tree/branch/subdir`), parse it:

```bash
# Extract branch and subdir from URL, then:
git clone --depth=1 --branch <branch> <base-url> /tmp/assess-$(date +%s)
cd /tmp/assess-<timestamp>/<subdir>
```

**Form C — Pasted code or uploaded files**

The user has pasted one or more files into the conversation, or files are
available at `/mnt/user-data/uploads/`. Read them from context. If the paste
is fewer than ~150 lines with no imports or entry point visible, flag the
assessment as LOW CONFIDENCE in the header and note what architectural context
is missing.

**If none of the above**

Ask the user for one of: a local path (or `.` for current directory), a
GitHub/GitLab URL, or a code paste. Do not guess or proceed without a target.

---

Do not proceed to Step 1 without having read enough of the codebase to form
evidence-based conclusions. Minimum viable read: entry point(s), AI/model
integration layer, any prompt or tool definition files, configuration, and the
primary user-facing interface (CLI, API routes, UI components, or webhook
handlers).

### Step 1 — Architecture reconnaissance

Read and note the following signals, organised by the six framework dimensions.
Document your raw findings before scoring.

**Identity signals** (baseline — applies to all dimensions)
- Primary language and framework
- Entry points (CLI, API server, web app, library, SDK, agent harness)
- Deployment model (local, SaaS, embedded, on-premise)

**Core proposition signals**
- Is the model in the critical path or an optional accelerator?
- Does the product deliver a new capability, or does it speed up an existing one?
- Is the output consumed by the same person who triggered the request, or by
  an external system or downstream human?

**Sales ease signals**
- Who is implied as the buyer: a practitioner, a team manager, a CFO/COO,
  or a self-serve individual?
- Is there a configuration burden that implies a technical sale vs. self-serve?
- Does the code assume an existing documented process, or does it work on any
  unstructured input?

**Impl. effort signals**
- Presence of autonomous action (tool calls, browser control, code execution,
  file writes, API side-effects) vs. pure generation
- Human-in-the-loop checkpoints (confirmation prompts, approval gates, review
  steps) — are they in the normal path or the exception path?
- Does the entry trigger require a human or is it automated (schedule, webhook)?

**Internal resistance signals**
- Does the product replace a named job function or augment it?
- Is the product framed (in comments, READMEs, config) as a copilot or as an
  autonomous agent?
- Would an existing practitioner in this domain feel threatened or empowered?

**Real example signals**
- What is the closest prior-art human role or manual process this code
  approximates?
- Are there domain-specific prompt files, rule sets, or ontologies that
  indicate vertical depth?

**Main risk signals**
- Is there output validation, or does the code trust model output directly?
- Is there an escalation or fallback path for edge cases?
- Does the onboarding complexity match the target user's likely technical level?

### Step 2 — Score against the four modes

Load `references/value_modes.md` and score each mode on a 0–10 scale using the
criteria defined there. Do not round to avoid false precision — use one decimal
place. Record your reasoning for each score before writing the report. This
internal scratchpad is not included in the final report but must be completed
first to ensure the verdict is grounded.

Scoring is relative: the mode with the highest score is the Primary Mode. If
the second-highest score is within 1.5 points of the primary, flag it as a
Secondary Mode and explain the tension.

### Step 3 — Write the verdict report

Follow the schema in `references/verdict_schema.md` exactly. The report must:

- Use plain prose paragraphs, not bullet lists or tables, except where the
  schema explicitly calls for a structured block.
- Cite specific files, functions, patterns, or configuration keys as evidence
  for every claim. Assertions without file-level evidence are not permitted.
- Be written in the same language the user used (default English).
- Contain no emojis, no decorative characters, and no hedging language that
  weakens the verdict (phrases like "it could be argued" or "one might say"
  are prohibited — state the conclusion directly, then qualify with evidence).
- Be self-contained: a reader who has not seen the codebase must be able to
  understand the verdict and its reasoning.

---

## Edge cases and failure modes

**Insufficient codebase access**: If the available code is a small snippet
(under ~150 lines) or a single file with no architectural context, say so
explicitly at the top of the report and flag all scores as LOW CONFIDENCE.
Provide the best available analysis but recommend a full-codebase run.

**Hybrid products**: Many real products span two modes. The skill must still
return a Primary Mode — tie-breaking is not permitted. When scores are close,
the tiebreaker is "where does the value proposition land in the first user
interaction?" — the mode that best describes the product's opening move is
primary.

**Non-AI codebases**: If the codebase contains no model calls, no AI APIs, and
no generation or inference logic, return a one-paragraph report stating that no
AI value mode classification is possible and explain what was found instead.

**Internal tooling vs. commercial product**: The four modes were defined for
commercial AI products sold to enterprise buyers. Internal developer tools,
infrastructure libraries, and research codebases may not map cleanly. When this
is the case, note it explicitly and apply the framework as far as it applies,
with the caveat stated.

---

## Output

The final output is the verdict report as defined in `references/verdict_schema.md`,
written directly to the conversation (not saved to a file unless the user asks).
No preamble, no meta-commentary about the skill or the process. Begin directly
with the report header.

---

## Compatibility and installation

This skill follows the agentskills.io open SKILL.md standard and runs on any
agent that reads it.

**Tested / supported agents**
- Claude Code (Anthropic)
- GitHub Copilot — VS Code agent mode and Copilot CLI
- Cursor (manual placement)
- Codex CLI (OpenAI)
- Any agent that reads the agentskills.io open standard

**Install paths**
- Project-scoped: `.github/skills/`, `.claude/skills/`, or `.agents/skills/`
- Personal-scoped: `~/.copilot/skills/`, `~/.claude/skills/`, or `~/.agents/skills/`

Place this folder (named `detect-ai-value-mode-from-codebase`) in one of the
paths above so the folder name matches the skill `name`.

**Invocation**
```
/detect-ai-value-mode-from-codebase .
/detect-ai-value-mode-from-codebase <github-or-gitlab-url>
```
Or simply describe the intent (for example, "what value mode is this codebase?")
and the agent will trigger the skill from its description.

## Attribution

The four value modes (Amplifier, Substitute, Job Creator, Democratiser) are drawn
from the Enterprise AI Adoption Framework attributed to Derley Morais (Iron Flow).
This skill packages that framework as an analysis workflow; the framework itself
remains the property of its author.
