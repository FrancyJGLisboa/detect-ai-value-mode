# Input codebase (synthetic): plainlease

A web app that explains residential lease contracts in plain English for renters
with no legal background.

- Language/framework: Python, Streamlit
- Entry point: `app.py` (file upload widget + results view)
- AI integration: `core/explain.py` sends the extracted contract text to a
  hosted model with a domain system prompt held in `prompts/tenant_rights.md`
- Domain assets: `prompts/tenant_rights.md` encodes jurisdiction-specific tenant
  protections and red-flag clause patterns; `rules/red_flags.yaml` lists clause
  types to surface (auto-renewal, unilateral rent change, waiver of repair duty)
- Interaction: a renter uploads a PDF and reads a plain-language summary plus a
  flagged-clauses list; no legal knowledge required to operate it
- Output validation: `core/explain.py` checks that flagged clauses cite a line
  number in the source document before display
- Deployment: hosted SaaS, self-serve sign-up; no account manager flow in code

Invoked with: `/detect-ai-value-mode-from-codebase https://github.com/example/plainlease`
