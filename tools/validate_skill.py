# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Pre-publish validator and trigger-eval harness for agent skills.

Static mode (default) checks a skill directory against the agentskills.io open
SKILL.md standard AND the narrower Anthropic importer key allowlist, so a green
run means the skill is portable across Claude Code, Codex, Copilot, and Cursor.

Eval mode (--eval) measures trigger reliability: it reads an evals.yaml of
should-fire / should-not-fire phrases and, when ANTHROPIC_API_KEY is set, scores
the skill's description against them with a cheap model. This is the discovery
loss function: a skill that never triggers is worthless no matter how clean.

Usage:
    uv run validate_skill.py <skill_dir>
    uv run validate_skill.py <skill_dir> --eval
    uv run validate_skill.py <skill_dir> --eval --eval-threshold 0.85

Exit code 0 = no ERRORs (WARNs allowed); 1 = at least one ERROR or bad usage.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import yaml

# --- Spec constants (agentskills.io + Anthropic allowlist intersection) --------

ALLOWED_KEYS = frozenset(
    {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
)
# Keys people reach for that BELONG under metadata, not top-level. Mapped to a hint.
MISPLACED_KEYS = {
    "version": "metadata.version",
    "author": "metadata.author",
    "category": "metadata (or omit)",
    "tags": "metadata (or omit)",
}
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESC = 1024
MAX_COMPAT = 500
MAX_BODY_LINES = 500

# Lightweight portability red flags for the body / references.
SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)
ABS_PATH_RE = re.compile(r"(/Users/[^\s`'\"]+|/home/[^\s`'\"]+|[A-Z]:\\\\Users)")

ERROR, WARN, OK = "ERROR", "WARN", "OK"


@dataclass(frozen=True)
class Finding:
    level: str
    gate: str
    message: str


# --- Frontmatter parsing ------------------------------------------------------


def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Return (frontmatter, body, error). frontmatter is None on failure."""
    if not text.startswith("---"):
        return None, "", "SKILL.md must begin with a '---' frontmatter delimiter on line 1"
    # Match the closing delimiter on its own line.
    parts = re.split(r"(?m)^---\s*$", text, maxsplit=2)
    # re.split keeps a leading empty string before the first delimiter.
    if len(parts) < 3:
        return None, "", "SKILL.md frontmatter is not closed with a second '---' line"
    raw_fm, body = parts[1], parts[2]
    try:
        data = yaml.safe_load(raw_fm)
    except yaml.YAMLError as exc:
        return None, body, f"frontmatter is not valid YAML: {exc}"
    if not isinstance(data, dict):
        return None, body, "frontmatter did not parse to a mapping"
    return data, body, None


# --- Static gates -------------------------------------------------------------


def check_keys(fm: dict) -> list[Finding]:
    out: list[Finding] = []
    for key in fm:
        if key in ALLOWED_KEYS:
            continue
        if key in MISPLACED_KEYS:
            out.append(
                Finding(
                    ERROR,
                    "frontmatter-keys",
                    f"'{key}' is not a valid top-level key; move it to {MISPLACED_KEYS[key]}",
                )
            )
        else:
            out.append(
                Finding(
                    ERROR,
                    "frontmatter-keys",
                    f"'{key}' is not an allowed frontmatter key "
                    f"(allowed: {', '.join(sorted(ALLOWED_KEYS))})",
                )
            )
    return out


def check_name(fm: dict, skill_dir: Path) -> list[Finding]:
    out: list[Finding] = []
    name = fm.get("name")
    if not isinstance(name, str) or not name:
        return [Finding(ERROR, "name", "missing or empty 'name' field")]
    if len(name) > MAX_NAME:
        out.append(Finding(ERROR, "name", f"name is {len(name)} chars (max {MAX_NAME})"))
    if not NAME_RE.match(name):
        out.append(
            Finding(
                ERROR,
                "name",
                "name must be lowercase alphanumeric with single hyphens, "
                "no leading/trailing/consecutive hyphens",
            )
        )
    if name != skill_dir.name:
        out.append(
            Finding(
                ERROR,
                "name-matches-dir",
                f"name '{name}' must match the parent directory name '{skill_dir.name}'",
            )
        )
    return out


def check_description(fm: dict) -> list[Finding]:
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        return [Finding(ERROR, "description", "missing or empty 'description' field")]
    n = len(desc)
    if n > MAX_DESC:
        return [Finding(ERROR, "description", f"description is {n} chars (max {MAX_DESC})")]
    out = [Finding(OK, "description", f"description is {n} chars (max {MAX_DESC})")]
    if n > MAX_DESC * 0.95:
        out.append(
            Finding(WARN, "description", f"description {n} chars leaves <5% margin; trim for safety")
        )
    if not re.search(r"\b(use|when|trigger)\b", desc, re.IGNORECASE):
        out.append(
            Finding(
                WARN,
                "description",
                "description should say WHEN to use the skill (no use/when/trigger language found)",
            )
        )
    return out


def check_compatibility(fm: dict) -> list[Finding]:
    if "compatibility" not in fm:
        return []
    compat = fm["compatibility"]
    if not isinstance(compat, str):
        return [
            Finding(
                ERROR,
                "compatibility",
                "compatibility must be a STRING (max 500 chars), not a list/object; "
                "move agents/install-paths/invoke into the SKILL.md body",
            )
        ]
    out: list[Finding] = []
    if len(compat) > MAX_COMPAT:
        out.append(Finding(ERROR, "compatibility", f"compatibility is {len(compat)} chars (max {MAX_COMPAT})"))
    out.append(
        Finding(
            WARN,
            "compatibility",
            "compatibility is accepted by agentskills.io but ignored by the Anthropic importer; "
            "for max portability keep this minimal and document compatibility in the body",
        )
    )
    return out


def check_metadata(fm: dict) -> list[Finding]:
    if "metadata" not in fm:
        return []
    meta = fm["metadata"]
    if not isinstance(meta, dict):
        return [Finding(ERROR, "metadata", "metadata must be a mapping of string keys to string values")]
    out: list[Finding] = []
    for k, v in meta.items():
        if not isinstance(v, (str, int, float, bool)):
            out.append(
                Finding(ERROR, "metadata", f"metadata.{k} must be a scalar string value, got {type(v).__name__}")
            )
    if "version" not in meta:
        out.append(Finding(WARN, "metadata", "no metadata.version; add a semantic version for release tracking"))
    return out


def check_allowed_tools(fm: dict) -> list[Finding]:
    if "allowed-tools" not in fm:
        return []
    if not isinstance(fm["allowed-tools"], str):
        return [Finding(ERROR, "allowed-tools", "allowed-tools must be a space-separated string")]
    return []


def check_body(body: str) -> list[Finding]:
    out: list[Finding] = []
    n_lines = body.count("\n")
    if n_lines > MAX_BODY_LINES:
        out.append(
            Finding(WARN, "body-length", f"SKILL.md body is {n_lines} lines (>{MAX_BODY_LINES}); push detail to references/")
        )
    return out


def check_references(body: str, skill_dir: Path) -> list[Finding]:
    out: list[Finding] = []
    for rel in re.findall(r"\b((?:references|scripts|assets)/[\w./-]+)", body):
        if not (skill_dir / rel).exists():
            out.append(Finding(ERROR, "references", f"referenced file '{rel}' does not exist"))
    return out


def check_files(skill_dir: Path, fm: dict) -> list[Finding]:
    out: list[Finding] = []
    has_license_file = any((skill_dir / n).exists() for n in ("LICENSE", "LICENSE.md", "LICENSE.txt"))
    if "license" in fm and not has_license_file:
        out.append(Finding(WARN, "license", "license declared in frontmatter but no LICENSE file is bundled"))
    if "license" not in fm:
        out.append(Finding(WARN, "license", "no 'license' field; add one before public distribution"))
    if not (skill_dir / "README.md").exists():
        out.append(Finding(WARN, "readme", "no README.md; recommended for marketplace discovery"))
    if not (skill_dir / "examples").is_dir():
        out.append(Finding(WARN, "examples", "no examples/ dir; sample input->output greatly aids adoption"))
    return out


def check_portability(skill_dir: Path) -> list[Finding]:
    out: list[Finding] = []
    for path in skill_dir.rglob("*"):
        if not path.is_file() or path.name == "LICENSE" or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = path.relative_to(skill_dir)
        if SECRET_RE.search(text):
            out.append(Finding(ERROR, "secrets", f"possible secret/credential in {rel}"))
        if ABS_PATH_RE.search(text):
            out.append(Finding(WARN, "portability", f"machine-specific absolute path in {rel}"))
    return out


def run_static(skill_dir: Path) -> list[Finding]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [Finding(ERROR, "structure", f"no SKILL.md in {skill_dir}")]
    text = skill_md.read_text(encoding="utf-8")
    fm, body, err = parse_frontmatter(text)
    if err is not None or fm is None:
        return [Finding(ERROR, "frontmatter", err or "could not parse frontmatter")]
    findings: list[Finding] = []
    findings += check_keys(fm)
    findings += check_name(fm, skill_dir)
    findings += check_description(fm)
    findings += check_compatibility(fm)
    findings += check_metadata(fm)
    findings += check_allowed_tools(fm)
    findings += check_body(body)
    findings += check_references(body, skill_dir)
    findings += check_files(skill_dir, fm)
    findings += check_portability(skill_dir)
    return findings


# --- Trigger eval -------------------------------------------------------------


def load_evals(skill_dir: Path) -> tuple[dict | None, str | None]:
    for name in ("evals.yaml", "evals.yml", "evals.json"):
        path = skill_dir / name
        if path.exists():
            try:
                raw = path.read_text(encoding="utf-8")
                data = json.loads(raw) if path.suffix == ".json" else yaml.safe_load(raw)
            except (yaml.YAMLError, json.JSONDecodeError) as exc:
                return None, f"{name} is not valid: {exc}"
            return data, None
    return None, None


def validate_eval_structure(data: dict) -> list[Finding]:
    out: list[Finding] = []
    for key in ("should_fire", "should_not_fire"):
        items = data.get(key)
        if not isinstance(items, list) or not items:
            out.append(Finding(ERROR, "eval-structure", f"evals must have a non-empty '{key}' list"))
        elif not all(isinstance(x, str) and x.strip() for x in items):
            out.append(Finding(ERROR, "eval-structure", f"every '{key}' entry must be a non-empty string"))
    return out


def claude_yesno(description: str, phrase: str, api_key: str, model: str) -> bool | None:
    """Ask whether the skill should activate for a phrase. None on API failure."""
    prompt = (
        "You decide whether an agent skill should activate.\n\n"
        f"Skill description:\n{description}\n\n"
        f'User says: "{phrase}"\n\n'
        "Would this skill be the relevant one to trigger? Answer with exactly YES or NO."
    )
    payload = json.dumps(
        {"model": model, "max_tokens": 5, "messages": [{"role": "user", "content": prompt}]}
    ).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        text = "".join(b.get("text", "") for b in data.get("content", [])).strip().upper()
        return text.startswith("YES")
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, TimeoutError):
        return None


def run_eval(skill_dir: Path, threshold: float, model: str) -> list[Finding]:
    data, err = load_evals(skill_dir)
    if err:
        return [Finding(ERROR, "eval-structure", err)]
    if data is None:
        return [Finding(WARN, "eval", "no evals.yaml found; create one to measure trigger reliability")]
    findings = validate_eval_structure(data)
    if any(f.level == ERROR for f in findings):
        return findings

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        findings.append(
            Finding(OK, "eval", "eval file structurally valid; set ANTHROPIC_API_KEY to run live trigger scoring")
        )
        return findings

    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    fm, _, _ = parse_frontmatter(text)
    description = (fm or {}).get("description", "")

    fire_hits, fire_total = 0, len(data["should_fire"])
    for phrase in data["should_fire"]:
        verdict = claude_yesno(description, phrase, api_key, model)
        if verdict is None:
            return [Finding(ERROR, "eval", "Anthropic API call failed; check key/network")]
        fire_hits += int(verdict)
    skip_hits, skip_total = 0, len(data["should_not_fire"])
    for phrase in data["should_not_fire"]:
        verdict = claude_yesno(description, phrase, api_key, model)
        if verdict is None:
            return [Finding(ERROR, "eval", "Anthropic API call failed; check key/network")]
        skip_hits += int(not verdict)

    recall = fire_hits / fire_total
    specificity = skip_hits / skip_total
    findings.append(Finding(OK, "eval", f"should-fire recall {recall:.0%} ({fire_hits}/{fire_total})"))
    findings.append(Finding(OK, "eval", f"should-not-fire specificity {specificity:.0%} ({skip_hits}/{skip_total})"))
    if recall < threshold:
        findings.append(Finding(ERROR, "eval", f"trigger recall {recall:.0%} below threshold {threshold:.0%}"))
    if specificity < threshold:
        findings.append(Finding(ERROR, "eval", f"trigger specificity {specificity:.0%} below threshold {threshold:.0%}"))
    return findings


# --- CLI ----------------------------------------------------------------------


def render(findings: list[Finding]) -> None:
    order = {ERROR: 0, WARN: 1, OK: 2}
    for f in sorted(findings, key=lambda x: (order[x.level], x.gate)):
        print(f"  [{f.level:5}] {f.gate}: {f.message}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Validate an agent skill for distribution.")
    parser.add_argument("skill_dir", type=Path, help="path to the skill directory")
    parser.add_argument("--eval", action="store_true", help="also run the trigger-eval harness")
    parser.add_argument("--eval-threshold", type=float, default=0.9, help="min recall/specificity (default 0.9)")
    parser.add_argument("--model", default="claude-haiku-4-5", help="model for live trigger eval")
    args = parser.parse_args(argv)

    skill_dir = args.skill_dir.resolve()
    if not skill_dir.is_dir():
        print(f"error: {skill_dir} is not a directory", file=sys.stderr)
        return 1

    print(f"Validating skill: {skill_dir.name}")
    findings = run_static(skill_dir)
    if args.eval:
        findings += run_eval(skill_dir, args.eval_threshold, args.model)
    render(findings)

    errors = sum(f.level == ERROR for f in findings)
    warns = sum(f.level == WARN for f in findings)
    print(f"\n{'FAIL' if errors else 'PASS'} — {errors} error(s), {warns} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
