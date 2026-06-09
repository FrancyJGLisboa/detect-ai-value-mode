    ═══════════════════════════════════════════════════
    AI VALUE MODE ASSESSMENT
    Codebase: plainlease
    Assessment date: 2026-06-09
    Confidence: CONFIRMED
    ═══════════════════════════════════════════════════

Section 1 — Codebase Profile

plainlease is a Python Streamlit web application. Its entry point presents a file
upload widget and a results view (file: app.py, function: main). The AI
integration layer extracts text from an uploaded lease and sends it to a hosted
model together with a domain system prompt (file: core/explain.py, function:
explain_contract; file: prompts/tenant_rights.md). The application carries two
domain assets that are not generic: a jurisdiction-specific tenant-rights prompt
and a red-flag clause registry (file: rules/red_flags.yaml). It is deployed as a
hosted, self-serve SaaS; the user-facing surface is a plain-language summary plus
a flagged-clauses list rendered back to the uploader.

Section 2 — Evidence Summary

The core proposition is to make specialist work — reading and interpreting a
legal contract — accessible to someone with no legal training. The product does
not speed up a lawyer; it removes the need for one in the common case. The output
is written for a layperson and consumed directly by the person who uploaded the
document (file: core/explain.py, function: explain_contract), with the
interpretation framed in everyday language rather than legal terminology.

Sales-ease signals indicate self-serve adoption by individuals. There is sign-up
and a single-document workflow, but no account-manager flow, seat management, or
enterprise configuration anywhere in the codebase (file: app.py). The buyer is
the end user — a renter — and the sale is frictionless because the product
assumes no documented process and works on any uploaded lease.

Implementation effort for the user is near zero, which is the point: upload a
PDF, read the result. The architecture encodes the expertise instead of asking
the user to supply it. The vertical knowledge lives in prompts/tenant_rights.md
and rules/red_flags.yaml, where specific clause types (auto-renewal, unilateral
rent change, waiver of repair duty) are enumerated for the model to surface.

Internal-resistance signals are mixed in a way that matters. The product helps a
population that previously could not afford the specialist at all, so it faces
little resistance from its users; but it approaches the boundary of a regulated
profession, which is the closest prior-art equivalent (real example): the unpaid,
inaccessible work of a tenant-rights lawyer or housing advice clinic. The main
risk implied by the architecture is incorrect interpretation presented to a user
who cannot detect the error. The code mitigates this partially — flagged clauses
must cite a source line number before display (file: core/explain.py, function:
explain_contract) — but there is no escalation path to a human professional for
genuinely ambiguous clauses.

    ─────────────────────────────────────────────
    MODE SCORES  (0–10, one decimal place)
    ─────────────────────────────────────────────
    Amplifier      2.5   core proposition: does not speed up a lawyer, removes the need for one
    Substitute     4.0   real example: substitutes basic legal review, but for the unserved, not a paid role
    Job Creator    1.5   internal resistance: no new profession created in code
    Democratiser   8.5   impl. effort: domain expertise encoded in prompts/tenant_rights.md, zero user skill required
    ─────────────────────────────────────────────
    Primary mode:   Democratiser
    Secondary mode: Substitute
    ─────────────────────────────────────────────

Section 4 — Verdict

This codebase is a Democratiser. The core proposition, expressed in the explainer
and its domain assets (file: core/explain.py, function: explain_contract; file:
prompts/tenant_rights.md), is to encode specialist legal judgement so that a
non-specialist can act on a contract without hiring anyone. Sales ease maps to the
easy quadrant: a self-serve, single-document workflow with no enterprise surface
(file: app.py) means the renter buys directly and the sale needs no process
change. The Substitute secondary score reflects that the product does perform work
a junior lawyer would otherwise do, and the tiebreaker is who the value lands on:
the first user interaction serves a person who would not have engaged a lawyer at
all, which is a democratising move, not a headcount replacement. The dominant main
risk is confidently wrong interpretation for a user unable to catch it. Strategically,
this product should be positioned and priced on access and affordability — a low
per-document or freemium model — not as a substitute sold against legal-team cost,
and its trust narrative must lead with the source-citation safeguard.

Section 5 — Defensibility Assessment

The position is more defensible than a generic wrapper because vertical knowledge
is encoded in the repository rather than left to the base model. prompts/tenant_rights.md
and rules/red_flags.yaml are proprietary process knowledge that a competitor would
have to rebuild jurisdiction by jurisdiction, which creates a real, if modest,
moat. The core proposition is differentiated by that domain depth rather than by
model access. The clearest weakness is the absence of a human escalation path and
of any feedback loop capturing which interpretations users acted on or disputed —
without that, the domain assets cannot compound, and the regulatory exposure of
giving unsupervised legal interpretation remains unbounded.

Section 6 — Recommended Actions

    1. Main risk: Add a confidence threshold in core/explain.py that routes
       ambiguous clauses to a "consult a professional" path instead of presenting
       a plain-language verdict the user cannot check.
    2. Impl. effort: Expand rules/red_flags.yaml and prompts/tenant_rights.md to
       additional jurisdictions to deepen the encoded-expertise moat that defines
       the Democratiser position.
    3. Core proposition: Capture which flagged clauses users expand or dispute to
       build a proprietary feedback dataset that compounds the domain assets over
       time.
    4. Sales ease: Keep the self-serve workflow in app.py but add an optional paid
       human-review upsell, converting the Substitute-adjacent capability into
       revenue without compromising the democratising entry point.

    ─────────────────────────────────────────────
    Framework: Four AI Value Modes (Iron Flow / Derley Morais)
    Skill: detect-ai-value-mode-from-codebase
    ─────────────────────────────────────────────
