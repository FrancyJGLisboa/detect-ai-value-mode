# Examples

Illustrative runs of the skill so you can see the output shape before installing.

Each folder has:
- `INPUT.md` — a short description of the (synthetic) codebase that was analysed
- `REPORT.md` — the verdict report the skill produces, following
  [`../references/verdict_schema.md`](../references/verdict_schema.md)

| Example | Codebase | Primary mode |
|---------|----------|--------------|
| [`amplifier-ide-copilot/`](amplifier-ide-copilot/) | A VS Code inline code-completion extension | Amplifier |
| [`democratiser-legal-explainer/`](democratiser-legal-explainer/) | A web app that explains contracts in plain English | Democratiser |

These reports are **synthetic and illustrative** — the file paths reference
hypothetical codebases to demonstrate tone, structure, and the citation style.
To generate a real one, install the skill and run it on an actual repo:

```text
/detect-ai-value-mode-from-codebase .
/detect-ai-value-mode-from-codebase https://github.com/org/repo
```
