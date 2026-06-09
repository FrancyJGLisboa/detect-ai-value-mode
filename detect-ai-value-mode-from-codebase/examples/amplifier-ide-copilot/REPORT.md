    ═══════════════════════════════════════════════════
    AI VALUE MODE ASSESSMENT
    Codebase: inline-complete
    Assessment date: 2026-06-09
    Confidence: CONFIRMED
    ═══════════════════════════════════════════════════

Section 1 — Codebase Profile

inline-complete is a TypeScript VS Code extension built on the editor's
extension API. Its single entry point registers an inline completion provider
(file: src/extension.ts, function: activate), which the editor invokes as the
developer types. The AI integration layer is a thin streaming client (file:
src/llm/client.ts, function: streamCompletion) that sends the surrounding buffer
prefix and suffix to a hosted model over HTTPS and returns token deltas. The
product runs entirely inside the developer's editor; there is no server, no
background process, and no persistence beyond editor settings contributed in
package.json. The user-facing surface is ghost text rendered inline, accepted or
discarded by keystroke.

Section 2 — Evidence Summary

The core proposition is to make an existing activity — writing code — faster.
The model is not in the critical path of any deliverable; it produces optional
suggestions that the developer already knows how to write themselves. The output
is consumed by the same person who triggered it, in the same second, with no
downstream system involved (file: src/extension.ts, function: provideInlineCompletionItems).

Sales-ease signals point to self-serve adoption by individual practitioners. The
extension installs from a marketplace, configures through a settings panel, and
requires no documented process or administrator (file: package.json, key:
contributes.configuration). There is no team, billing, or admin surface in the
code, which implies the buyer and the user are the same developer.

Implementation-effort signals are minimal and deliberately so. Every suggestion
requires an explicit Tab keystroke to apply; rejection is the default outcome of
continuing to type (file: src/extension.ts, function: provideInlineCompletionItems).
There is no autonomous action, no file write outside the accepted insertion, and
no scheduled or webhook trigger anywhere in the codebase.

Internal-resistance signals are low. The product augments the developer rather
than replacing a named role; the framing throughout package.json and the README
is assistive ("suggestions", "completions"), not autonomous. The closest
prior-art equivalent (real example) is editor autocomplete and snippet expansion
— a tool category developers already accept. The main risk implied by the
architecture is suggestion quality and latency, not process failure: a poor
completion costs one wasted keystroke, and the human is always the gate.

    ─────────────────────────────────────────────
    MODE SCORES  (0–10, one decimal place)
    ─────────────────────────────────────────────
    Amplifier      9.0   core proposition: optional inline suggestions, human always the gate
    Substitute     1.5   impl. effort: no autonomous path, no role replaced
    Job Creator    1.0   real example: no new role; maps to existing autocomplete
    Democratiser   3.0   sales ease: self-serve, but aimed at developers, not non-specialists
    ─────────────────────────────────────────────
    Primary mode:   Amplifier
    Secondary mode: (none — gap > 1.5 pts)
    ─────────────────────────────────────────────

Section 4 — Verdict

This codebase is an Amplifier. The core proposition, expressed in the inline
completion provider (file: src/extension.ts, function: provideInlineCompletionItems),
is to accelerate an existing task without taking it over: the model proposes,
the developer disposes, and the normal path requires a human keystroke to apply
anything. The sales-ease dimension reinforces this — the absence of any team,
admin, or billing surface (file: package.json) means this is a self-serve tool
bought by the practitioner who uses it, not an enterprise process sale. The main
risk is purely quality-and-latency: there is no autonomous side effect to fail,
because nothing happens without the human. No secondary mode reaches within 1.5
points; the Democratiser score is held down because the audience is developers,
not non-specialists. Strategically, this product must be sold on productivity per
developer and priced per seat — positioning it as an autonomous agent would
overpromise against an architecture that is, by design, never autonomous.

Section 5 — Defensibility Assessment

As read, the position is differentiated only weakly. The implementation effort a
customer would incur to switch is near zero — there is no proprietary data
pipeline, no domain-specific fine-tuning, and no vertical process knowledge
encoded anywhere; client.ts is a generic streaming wrapper around a hosted model.
That makes the switching-cost moat shallow: a competitor with a better base model
or lower latency can displace this with an equivalent extension. The core
proposition is a commodity (inline completion) and the code contains no signal of
a defensible asset. The defensibility, such as it is, would have to come from
model quality and editor integration polish, neither of which is owned here.

Section 6 — Recommended Actions

    1. Core proposition: Capture accept/reject telemetry at the keystroke gate
       (file: src/extension.ts, function: provideInlineCompletionItems) to build
       a proprietary preference dataset no competitor has.
    2. Impl. effort: Add an opt-in multi-line / whole-function mode behind a
       confirmation step to climb toward Substitute value without removing the
       human gate that defines the current low-resistance position.
    3. Sales ease: Introduce a team settings surface in package.json so the buyer
       can become an engineering manager, opening a higher-ACV motion than
       per-developer self-serve.
    4. Real example: Encode language- or framework-specific completion rules in
       src/llm/client.ts to move beyond generic autocomplete toward a defensible,
       vertical Amplifier.

    ─────────────────────────────────────────────
    Framework: Four AI Value Modes (Iron Flow / Derley Morais)
    Skill: detect-ai-value-mode-from-codebase
    ─────────────────────────────────────────────
