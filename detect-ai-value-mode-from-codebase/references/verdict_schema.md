# Verdict Report Schema

This file defines the exact structure and writing rules for the output of the
detect-ai-value-mode-from-codebase skill. Follow this schema precisely.

The six dimensions used in the Score Block and throughout the report match the
matrix in the framework infographic exactly:
  Core proposition | Sales ease | Impl. effort |
  Internal resistance | Real example | Main risk

---

## Writing rules (global)

1. Plain prose paragraphs only, except for the Score Block (see below).
2. No emojis, no decorative Unicode symbols, no markdown decorations beyond
   the headers and horizontal rules defined in this schema.
3. No hedging constructions: "it could be argued", "one might say", "arguably",
   "it seems", "it appears", "perhaps". State conclusions directly, then support
   them with evidence.
4. Every claim about the codebase must cite at least one specific file, function
   name, configuration key, or code pattern as evidence. Format citations
   inline as: (file: path/to/file.py, function: function_name) or
   (file: path/to/config.yaml, key: model_provider).
5. Write in the same language as the user's request. Default is English.
6. Target length: 600–900 words for the full report body (excluding headers,
   score block, and horizontal rules). Reports shorter than 600 words are
   likely under-evidenced. Reports longer than 900 words are likely
   over-explaining.
7. Confidence levels: CONFIRMED (strong multi-file evidence), MODERATE
   (single-file or inferential evidence), LOW (absent key files, snippet only).
   Every claim that is not CONFIRMED must be prefixed with its confidence level.

---

## Schema

### Header

    ═══════════════════════════════════════════════════
    AI VALUE MODE ASSESSMENT
    Codebase: [repository name or path]
    Assessment date: [YYYY-MM-DD]
    Confidence: [CONFIRMED | MODERATE | LOW]
    ═══════════════════════════════════════════════════

The confidence field in the header reflects the overall confidence of the
assessment, set to the lowest confidence level encountered across any of the
four scored dimensions.

---

### Section 1 — Codebase Profile

One paragraph. Describe what the codebase is and does, based solely on what
was read. Cover: primary language and framework, entry points, deployment
model, AI integration layer (which models, how invoked), and the primary
user-facing interface. This section must not contain any value mode language —
it is a neutral description.

---

### Section 2 — Evidence Summary

Two to four paragraphs. Describe the architectural patterns and signals
observed, grouped by the six framework dimensions:

  - Core proposition (what value the product is structured to deliver)
  - Sales ease (signals about who buys this and how hard the sale is)
  - Impl. effort (how much process redesign the architecture implies)
  - Internal resistance (whether the product threatens or helps existing roles)
  - Real example (the closest prior-art equivalent to what this code does)
  - Main risk (the primary failure mode implied by the architecture)

Each paragraph should synthesise related signals across dimensions. This
section builds the evidentiary record that the verdict draws on. Do not reach
conclusions here — describe what was found.

---

### Section 3 — Score Block

The score block is the only structured (non-prose) element in the report.
Format it exactly as shown:

    ─────────────────────────────────────────────
    MODE SCORES  (0–10, one decimal place)
    ─────────────────────────────────────────────
    Amplifier      [X.X]   [evidence anchor]
    Substitute     [X.X]   [evidence anchor]
    Job Creator    [X.X]   [evidence anchor]
    Democratiser   [X.X]   [evidence anchor]
    ─────────────────────────────────────────────
    Primary mode:   [MODE NAME]
    Secondary mode: [MODE NAME]  (omit if gap > 1.5 pts)
    ─────────────────────────────────────────────

The evidence anchor is a one-line phrase naming the single strongest piece of
evidence for that score, using the dimension language where natural. Examples:
  "impl. effort: autonomous dispatch loop requires full process redesign"
  "sales ease: zero-config CLI implies self-serve, not enterprise deal"
  "main risk: no output validation for non-specialist user"

---

### Section 4 — Verdict

One to two paragraphs structured around the six dimensions. State the primary
mode, then walk through the dimensions that most strongly support it — in
particular core proposition, sales ease, and main risk, as these are the most
strategically relevant for a PM. If a secondary mode is present, explain which
dimensions pull toward it and which dimension is the tiebreaker. End with one
sentence stating the strategic implication: how this classification should
change how the product is sold, priced, or positioned.

---

### Section 5 — Defensibility Assessment

One paragraph. Assess how defensible the current mode classification is as a
business position, given the codebase as read. Address: whether the impl.
effort required is high enough to create a switching-cost moat, whether the
core proposition is differentiated or commodity, and whether there are signals
in the code (proprietary data pipelines, domain-specific fine-tuning, vertical
process knowledge encoded in prompts or rules) that harden the position. Be
direct about weaknesses.

---

### Section 6 — Recommended Actions

Three to five numbered sentences, each stating one concrete action the
engineering or product team could take to either strengthen their current mode
or deliberately migrate toward a more defensible one. Frame each action against
one of the six dimensions so the PM can map it to the framework directly. Each
action must be grounded in something observed in the codebase — no generic
advice. Format:

    1. [Dimension]: [Action sentence citing specific code observation.]
    2. [Dimension]: [Action sentence.]
    ...

---

### Footer

    ─────────────────────────────────────────────
    Framework: Four AI Value Modes (Iron Flow / Derley Morais)
    Skill: detect-ai-value-mode-from-codebase
    ─────────────────────────────────────────────

---

## Example score block (for reference only — do not copy scores)

    ─────────────────────────────────────────────
    MODE SCORES  (0–10, one decimal place)
    ─────────────────────────────────────────────
    Amplifier      3.0   sales ease: no autonomous path, but sold to wrong buyer
    Substitute     7.5   impl. effort: autonomous dispatch in agent/runner.py:execute()
    Job Creator    2.0   core proposition: clear prior-art SDR function being replaced
    Democratiser   6.3   real example: zero-config CLI lowers access barrier
    ─────────────────────────────────────────────
    Primary mode:   Substitute
    Secondary mode: Democratiser
    ─────────────────────────────────────────────

## Example verdict paragraph (for tone and style reference only)

"This codebase is a Substitute. The core proposition, as expressed in
agent/runner.py:execute(), is unambiguous: the system runs on a cron schedule,
dispatches tool calls without any confirmation gate, and writes results directly
to Salesforce via integrations/crm.py:push_qualified_lead() — the normal path
completes without any human present. The sales ease dimension maps to the
hardest quadrant: this product requires a documented SDR process, executive
sponsorship from a revenue operations leader, and a cost-per-qualified-lead ROI
narrative before any enterprise buyer will sign. The main risk is process
failure without redesign — config/schedule.yaml sets human_review to false
with no fallback defined for undocumented edge cases in the lead data. The
Democratiser secondary score reflects the zero-config CLI, but that simplicity
serves a process replacement, not a capability extension to non-specialists.
Strategically, this product must be positioned and priced against headcount
reduction, not productivity improvement — selling it as a copilot to sales
managers will create misaligned expectations and accelerate churn."
