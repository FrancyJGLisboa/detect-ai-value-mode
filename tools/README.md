# skill-validator

A single-file, zero-install pre-publish gate for agent skills. A green run means
the skill is portable across the agentskills.io open standard **and** the
narrower Anthropic importer — i.e. it will load on Claude Code, Codex, Copilot,
and Cursor without rejection.

It enforces the discipline that should be in the loop from a skill's first
commit, so "is this distributable?" is never a question you answer reactively.

## Run

```bash
# static spec validation (no API key, no install — uv resolves pyyaml on first run)
uv run validate_skill.py ../detect-ai-value-mode-from-codebase

# also score trigger reliability (needs evals.yaml in the skill + ANTHROPIC_API_KEY)
ANTHROPIC_API_KEY=sk-... uv run validate_skill.py ../detect-ai-value-mode-from-codebase --eval
```

Exit code is `0` when there are no ERRORs (WARNs are allowed), `1` otherwise — so
it drops straight into CI or a pre-commit hook.

## What it checks

**Static (ERROR = blocks distribution):**
- `SKILL.md` exists and starts with a closed `---` frontmatter block that parses as YAML.
- Only spec-allowed top-level keys: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. A top-level `version`/`author`/`category`/`tags` is flagged with a "move it to metadata" hint — the exact gotcha that breaks the Anthropic importer.
- `name`: 1–64 chars, lowercase alphanumeric + single hyphens, **and matches the parent directory name**.
- `description`: 1–1024 chars, with a margin warning above 95%.
- `compatibility`: must be a **string** ≤500 chars (a nested object is rejected); warns that the Anthropic importer ignores it.
- `metadata`: a mapping of scalar values; warns if `metadata.version` is missing.
- Referenced `references/ | scripts/ | assets/` files actually exist.
- Secret/credential scan (ERROR) and machine-specific absolute-path scan (WARN).

**Static (WARN = advisory):** body over 500 lines, missing `LICENSE` file, missing `README.md`, missing `examples/`.

**Eval (`--eval`):** always validates `evals.yaml` structure (no key needed). To
*score* the description against the `should_fire` / `should_not_fire` phrases there
are two paths — **no API key required for the normal one:**

- **Agent-native (recommended, uses your subscription):** inside Claude Code (or
  Copilot / Codex), ask your agent to run the eval — e.g. *"score
  `detect-ai-value-mode-from-codebase/evals.yaml` against the skill's description
  and report should-fire recall and should-not-fire specificity."* This uses the
  subscription you already pay for. No key, no extra cost.
- **Offline / CI (optional, needs a key):** if you set `ANTHROPIC_API_KEY`, the
  script scores the phrases itself and fails when recall or specificity drops below
  `--eval-threshold` (default 0.9). Only useful for fully headless automation.

Either way this is the discovery loss function — a clean skill that never triggers
is still a failed skill.

> Note: the **skill itself never needs an API key.** It runs on the user's agent
> subscription. The key is only ever relevant to this optional offline eval path.

## evals.yaml format

Drop this in the skill directory next to `SKILL.md`:

```yaml
should_fire:
  - "phrase that MUST activate the skill"
should_not_fire:
  - "off-topic phrase that MUST stay quiet"
```

## Wiring into CI

CI runs the **static** gate only — no API key, no secret, free on every push:

```yaml
# .github/workflows/validate-skill.yml
- uses: astral-sh/setup-uv@v5
- run: uv run tools/validate_skill.py detect-ai-value-mode-from-codebase
```

Keep trigger scoring as a manual, subscription-based step (above) rather than a
CI secret, so forks without a key still get a green, meaningful build.

## Wiring into the bdistill factory

The factory emits skills; make this the final gate so every generated skill is
born distributable instead of needing a one-off audit:

1. After `bdistill_factory_finalize`, run `validate_skill.py <emitted_dir>` and
   fail the build on a non-zero exit.
2. Have the factory also emit a starter `evals.yaml` (it already knows the skill's
   intended triggers from the manifest) so `--eval` has something to score.
3. Treat the static gate as a hard block and the eval recall/specificity as a
   tunable quality bar in the factory's manifest.

## Note

This validates against the published spec by hand; it is not the official
`skills-ref` binary (from github.com/agentskills/agentskills). Run that too before
a high-stakes publish — but this catches every failure class we have hit, with no
install and no network for the static pass.
