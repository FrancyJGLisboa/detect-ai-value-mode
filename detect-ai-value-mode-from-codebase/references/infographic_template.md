# Infographic Template — Optional Visual Form of the Verdict Report

This file defines the optional HTML infographic output. It is rendered only
when the user explicitly asks for a diagram, infographic, or visual version of
the assessment — see Step 4 in SKILL.md. The prose verdict report is always
the canonical output; the infographic is derived from it after the fact and
must never diverge from it.

The design system below is adapted from the infographic-extractor skill's
generator handoff specification (attribution: same author). It is copied here
in full so this skill remains standalone-installable.

---

## Hard rules

1. The completed prose verdict report is the ONLY content source. Never
   re-derive scores, re-read the codebase, or introduce claims that are not in
   the report.
2. Scores, confidence level, primary/secondary mode, and assessment date must
   match the prose report digit-for-digit and word-for-word.
3. One single self-contained `.html` file. All CSS in one `<style>` block in
   the `<head>`. No JavaScript. The only external dependency permitted is the
   Google Fonts `@import` for Montserrat and Inter.
4. No emojis and no decorative Unicode anywhere in the rendered text, matching
   the skill's prose ethos. Visual emphasis comes from the design system, not
   from symbols.
5. File name: `<codebase-name>-value-mode-infographic.html`, saved in the
   current working directory unless the user specifies another location.
   Report the saved absolute path in the conversation after writing it.

---

## Design system (invariant)

### Palette (hex values are fixed — do not substitute)

| Role | Hex | Usage |
|---|---|---|
| Navy primary | `#1B2A47` | Title, section number squares, footer block, body emphasis |
| Teal secondary | `#2A8B8C` | Tagline, subtitles, primary-mode highlight, positive accents |
| Warning orange | `#E45A2E` | Risk signals, LOW-confidence badge |
| Cream gray | `#F5F1EA` | Card backgrounds (quadrant cells, section cards) |
| White | `#FFFFFF` | Page background |
| Divider gray | `#D9D9D9` | Separators, score-bar tracks, non-primary cell borders |

### Typography

```css
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;900&family=Inter:wght@400;600&display=swap');
```

- Title: Montserrat 900, ALL CAPS, ends with a period, navy.
- Tagline / subtitles: Montserrat 600, all caps, teal, `letter-spacing: 0.02em`.
- Body: Inter 400, navy, 14–15px, line-height 1.5.
- Section numbers: Montserrat 700, white on a navy 32×32px square.
- File-path citations: a monospace stack (`"SF Mono", Menlo, monospace`),
  13px, navy on cream.

### Layout

Vertical poster, 800px wide, natural height (roughly 2:3 or taller). Centered
on the page. Top-to-bottom order:

1. **Header** — title, tagline, meta row.
2. **Score visual block** — the 2×2 mode quadrant.
3. **Numbered sections** — 2-column grid of four cards.
4. **Footer** — navy block with the pull quote.

### Content rules (transversal)

- Each numbered section: at most 60 words.
- Each bullet or action line: at most 12 words.
- Every score shown with one decimal place, every scale labeled (0–10).
- No filler, no hedging — same prose discipline as the report.
- Output language: the language of the prose report.

---

## Report-to-infographic mapping (fixed)

### 1. Header

- Title: `AI VALUE MODE ASSESSMENT.`
- Tagline: a one-line essence of the verdict, 12 words or fewer, written
  fresh from the Verdict section (e.g. "A substitute wearing copilot
  clothes." style — declarative, no hedging).
- Meta row (Inter, small, single line, divider-gray rules above and below):
  codebase name or path · assessment date · confidence badge.
- Confidence badge: small rounded pill — CONFIRMED in teal, MODERATE in
  divider gray with navy text, LOW in warning orange. White text on teal and
  orange.

### 2. Score visual block (the 2×2 mode quadrant)

A 2×2 CSS grid of the four modes, fixed positions:

```
Amplifier    | Substitute
-------------+-------------
Job Creator  | Democratiser
```

Each cell contains, top to bottom:
- Mode name (Montserrat 600, all caps, small).
- Score (Montserrat 900, large, one decimal place).
- A horizontal score bar: full-width track in divider gray, filled
  proportionally to score/10 — teal fill for the primary mode, navy fill for
  all others.
- The evidence anchor phrase from the Score Block (Inter, small).

Cell emphasis, taken from the prose report's Score Block:
- Primary mode: cream background, 3px solid teal border, a small teal
  `PRIMARY` tag in the top corner.
- Secondary mode (only if the report names one): white background, 2px solid
  teal border, small `SECONDARY` tag in teal text.
- Other modes: white background, 1px divider-gray border.

### 3. Numbered sections (2-column grid)

Four cards on cream backgrounds, each headed by a navy number square and a
teal subtitle. Condense — do not copy paragraphs verbatim; distill to the
word limits above.

1. **CODEBASE PROFILE** — language, framework, entry point, deployment model,
   AI integration layer. From the report's Codebase Profile section.
2. **EVIDENCE HIGHLIGHTS** — the 3–4 strongest citations from the Evidence
   Summary, each as one line: monospace file path, then the finding in 12
   words or fewer.
3. **DEFENSIBILITY** — the moat assessment condensed to 60 words or fewer.
   If the report finds the moat weak, render the key phrase in warning orange.
4. **RECOMMENDED ACTIONS** — the top 3 actions from the report, numbered,
   each 12 words or fewer.

### 4. Footer (pull quote)

Full-width navy block. The strategic-implication closing sentence from the
Verdict section, in Inter italic, white, centered, flanked by large
decorative quotation marks rendered in teal via CSS pseudo-elements (these
are typographic quotes, part of the design system — not emojis). Below it,
one small line in divider gray: framework attribution (Derley Morais, Iron
Flow) and the skill name.

---

## Skeleton (structure reference — adapt content, keep structure)

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Value Mode Assessment — {codebase}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;900&family=Inter:wght@400;600&display=swap');
  body { background:#FFFFFF; margin:0; font-family:'Inter',sans-serif; color:#1B2A47; }
  .poster { width:800px; margin:0 auto; padding:48px 56px; }
  h1 { font-family:'Montserrat',sans-serif; font-weight:900; text-transform:uppercase; color:#1B2A47; }
  .tagline { font-family:'Montserrat',sans-serif; font-weight:600; text-transform:uppercase; color:#2A8B8C; letter-spacing:0.02em; }
  .quadrant { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
  .sections { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  .card { background:#F5F1EA; padding:20px; }
  .num { font-family:'Montserrat',sans-serif; font-weight:700; background:#1B2A47; color:#FFFFFF; width:32px; height:32px; display:inline-flex; align-items:center; justify-content:center; }
  .footer { background:#1B2A47; color:#FFFFFF; font-style:italic; text-align:center; padding:32px 48px; }
</style>
</head>
<body>
  <div class="poster">
    <!-- 1 header / 2 quadrant / 3 sections / 4 footer -->
  </div>
</body>
</html>
```

---

## Pre-delivery checklist

- [ ] Four scores match the prose Score Block exactly (one decimal each).
- [ ] Primary/secondary emphasis matches the report's named modes.
- [ ] Confidence badge matches the report header.
- [ ] Every palette color is one of the six fixed hex values.
- [ ] No JavaScript; only external request is the Google Fonts import.
- [ ] No emojis or decorative Unicode in rendered text.
- [ ] Word limits respected (sections ≤60, bullets ≤12).
- [ ] File saved and absolute path reported to the user.
