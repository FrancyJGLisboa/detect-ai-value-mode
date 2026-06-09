# Value Modes Reference

Source: Enterprise AI Adoption Framework — Four Value Modes of AI
(Webinar: Derley Morais, Iron Flow)

The six dimensions used throughout this reference match the matrix in the
framework infographic exactly:
  Core proposition | Sales ease | Impl. effort |
  Internal resistance | Real example | Main risk

---

## Overview

Every AI product delivers value through one of four distinct mechanisms. The
mode is determined by how the product changes the relationship between human
effort and output — not by the technology stack, the model used, or the
industry served. Classification is based on the product's primary value
proposition as expressed in its architecture, not its marketing copy.

---

## Mode 1 — Amplifier

**Core proposition**: The same person who does the work today continues to do
it, but produces significantly more output in the same time, or the same output
with significantly less effort.

**Defining characteristic**: The human remains in the loop on every significant
decision. The AI accelerates, enriches, or offloads repetitive sub-tasks, but
does not replace the human's judgment or ownership of the outcome.

**Typical architecture**: Copilot pattern — the model is called on demand by
the user, suggestions are presented for human review, and the human commits or
discards each suggestion. Tool calls, if present, require explicit confirmation.
The product is embedded in an existing workflow rather than replacing it.

**Real example**: AI writing assistant inside a CRM, code completion in an IDE,
AI-powered meeting summariser that the user reviews before sending, sales
copilot that drafts follow-ups for the rep to approve.

**Sales ease**: Easy — company wants productivity without layoffs. Value is
measured in time saved per task, not headcount reduction. Budget owner is
typically the team manager or head of function, not the C-suite.

**Internal resistance**: Low. The product is framed as making the existing team
more productive — a benefit to the people using it, not a threat to their roles.

**Impl. effort**: Low to medium. The existing process does not need to be
redesigned; the AI is inserted at specific friction points.

**Main risk**: Under-adoption. If users do not integrate the copilot into their
daily flow, there is no value — the product becomes shelfware.

### Scoring criteria for Amplifier (0–10)

Award points as follows:

- 0–2: Human is in the loop on every action; AI only suggests or drafts (2 pts)
- 0–2: Product is embedded in an existing workflow, not a standalone replacement (2 pts)
- 0–2: No autonomous side-effects without explicit user approval (2 pts)
- 0–2: Value metric is speed or quality improvement, not cost elimination (2 pts)
- 0–2: Target user is the practitioner doing the work, not a supervisor removing them (2 pts)

---

## Mode 2 — Substitute

**Core proposition**: A human function that existed before is now executed
entirely, or predominantly, by an AI agent. The human's role shifts from
executor to supervisor, monitor, or exception handler.

**Defining characteristic**: The AI owns the process end-to-end. It initiates
actions, makes decisions, handles the full range of normal cases autonomously,
and escalates only edge cases or failures to a human. The human does not need
to be present for the process to run.

**Typical architecture**: Agentic pipeline — the system has a defined entry
trigger (webhook, schedule, inbound message, API call), executes a sequence of
tool calls without human confirmation, writes outputs to external systems, and
generates a summary or audit trail for post-hoc review. Human-in-the-loop
exists as an exception path, not the normal path.

**Real example**: Fully automated customer service agent handling tier-1
support, AI system that processes and routes inbound sales leads end-to-end,
automated document review pipeline that produces a decision with an audit log.

**Sales ease**: Hard — full process redesign required. Requires a documented,
well-understood process, executive sponsorship, and a clear ROI narrative tied
to cost reduction or throughput increase. Budget owner is typically the CFO
or COO.

**Internal resistance**: High. The product explicitly replaces a function. Even
when the messaging is about "freeing people for higher-value work," the
architectural reality is that a job category is being automated.

**Impl. effort**: Very high. The process must be fully documented, redesigned
for autonomous execution, and tested against all known edge cases before
production deployment.

**Main risk**: Process failure without redesign. Deploying a Substitute agent
on top of an undocumented or inconsistent process reliably produces the pilot
purgatory failure pattern.

### Scoring criteria for Substitute (0–10)

Award points as follows:

- 0–2: Agent has autonomous tool calls with no required human confirmation in the happy path (2 pts)
- 0–2: Entry trigger is automated (schedule, webhook, external event) rather than human-initiated (2 pts)
- 0–2: Output is written to external systems (CRM, database, email, API) without human review (2 pts)
- 0–2: Human role is post-hoc review or exception handling, not participation in the normal path (2 pts)
- 0–2: The product replaces a named job function or department activity (2 pts)

---

## Mode 3 — Job Creator

**Core proposition**: The AI enables a new professional role, workflow, or
category of work that did not exist — or was not commercially viable — before
AI. The product does not automate what humans did before; it creates a new
thing for humans to do.

**Defining characteristic**: The product's core value is only legible to people
who understand the new category. Early adopters are enthusiasts or technically
sophisticated users who discover the capability; mainstream adoption follows
market education.

**Typical architecture**: Highly variable. May be a platform, an API, a
toolchain, or an agent harness. The defining signal is not the architecture but
the absence of a clear prior-art job description that the product is replacing
or accelerating. The product's value requires constructing a new mental model.

**Real example**: The first LLM prompt engineering tools (before prompt
engineering was a recognised discipline), AI orchestration platforms targeting
a new "agent ops" role, tools that enable a new category of AI-native service
businesses.

**Sales ease**: Medium — market category must mature. The product must educate
the market about the category before selling the solution. Early revenue comes
from early adopters and experimenters; mainstream revenue requires waiting for
the category to mature.

**Internal resistance**: Low. The product is not threatening existing jobs — it
is creating new ones. However, it faces a different obstacle: potential buyers
may not yet understand what they are buying or why they need it.

**Impl. effort**: Medium. The product itself may be technically straightforward,
but the customer's organisation needs to build new internal capabilities around
it.

**Main risk**: Timing — market may not be ready. The product may be technically
correct and commercially sound but arrive before the market understands the
category. A product that was a Job Creator in 2023 may have become an Amplifier
by 2025 as the category normalised.

### Scoring criteria for Job Creator (0–10)

Award points as follows:

- 0–2: The product enables a workflow or role with no clear pre-AI equivalent (2 pts)
- 0–2: The product's value requires learning a new mental model, not just a new tool (2 pts)
- 0–2: Target users are category pioneers or technically sophisticated early adopters (2 pts)
- 0–2: The product does not automate an existing named job function (2 pts)
- 0–2: The value proposition is about new capability, not speed or cost on existing work (2 pts)

---

## Mode 4 — Democratiser

**Core proposition**: A capability that previously required specialist expertise,
expensive tooling, or significant time investment is made accessible to a much
broader population — often non-specialists — through an AI-powered interface.

**Defining characteristic**: The product's key design constraint is radical
simplicity. The target user is not the existing specialist but the person who
previously could not do this at all. Scale of adoption, not depth of feature
set, is the primary success metric.

**Typical architecture**: Strongly user-facing. Zero-config or near-zero-config
onboarding. The AI absorbs complexity that would otherwise require the user to
have domain expertise. Typically involves a simple natural-language interface,
a template system, or a guided workflow that hides the underlying complexity.
Quality curation (guardrails, output validation, style enforcement) is critical
because the user cannot independently judge whether the output is correct.

**Real example**: Lovable / Bolt / similar vibe-coding tools (software
development for non-developers), AI legal document generators for individuals,
AI medical triage tools for patients, no-code AI workflow builders for business
analysts.

**Sales ease**: Medium — depends on adoption at mass scale. The product's
addressable market is very large (everyone who previously could not do this),
but individual contract values may be low (self-serve, consumer or SMB
pricing). Enterprise version requires adding governance and audit layers that
the base product may not have.

**Internal resistance**: Medium — requires cultural shift. Medium to high in
professional communities (experts resist tools that devalue their expertise),
low among the newly empowered non-specialists.

**Impl. effort**: High at the platform level (building the simplification layer
is hard), low at the user level (that is the point).

**Main risk**: Quality without curation. When non-specialists cannot evaluate
outputs, errors propagate. Products in this mode that do not invest in output
guardrails accumulate credibility damage as users discover and share failures.

### Scoring criteria for Democratiser (0–10)

Award points as follows:

- 0–2: Target user is a non-specialist or someone who previously could not do this task (2 pts)
- 0–2: Onboarding requires minimal configuration — the product absorbs complexity on behalf of the user (2 pts)
- 0–2: The primary interface is designed for simplicity, not power-user control (2 pts)
- 0–2: Scale of adoption is a more important metric than depth of enterprise feature set (2 pts)
- 0–2: The product addresses a task that previously required hiring a specialist or purchasing expensive tooling (2 pts)

---

## Mode interaction patterns

**Amplifier + Substitute tension**: Many products start as Amplifiers and
migrate toward Substitute as the product matures and the process becomes better
understood. A product that has both copilot features and autonomous pipeline
features should be scored on which mode dominates the primary user journey.

**Democratiser + Amplifier overlap**: A Democratiser aimed at complete
beginners looks very different from an Amplifier aimed at practitioners, but
a product aimed at "junior practitioners" can score moderately on both. The
tiebreaker is whether the product's core value claim is "you will be faster"
(Amplifier) or "you will now be able to do something you could not do before"
(Democratiser).

**Job Creator decay**: Job Creator is a temporal classification. Products that
were Job Creators when the category was new often become Amplifiers or
Democratisers as the category matures and the job description normalises. When
classifying a codebase, consider when it was likely written.
