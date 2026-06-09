# Input codebase (synthetic): inline-complete

A VS Code extension that offers inline code completions.

- Language/framework: TypeScript, VS Code extension API
- Entry point: `src/extension.ts` (`activate()` registers an
  `InlineCompletionItemProvider`)
- AI integration: `src/llm/client.ts` calls a hosted model with the current
  buffer prefix/suffix as context; streaming token completions
- Interaction: suggestions appear as ghost text; the developer presses Tab to
  accept or keeps typing to reject — nothing is applied without an explicit
  keystroke
- Config: `package.json` contributes settings for model, max tokens, and a
  per-language enable/disable toggle
- Deployment: runs locally in the user's editor; the model is called over HTTPS
- No autonomous file writes, no background execution, no CI/webhook triggers

Invoked with: `/detect-ai-value-mode-from-codebase .`
