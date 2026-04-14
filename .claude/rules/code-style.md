---
description: "Global code style and conventions for the entire project"
---

# Code Style

## Commit Messages
Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`
Include scope when relevant: `feat(backend): add generation endpoint`

## Branch Naming
`feature/description`, `fix/description`, `docs/description`

## General
- No commented-out code in commits
- No `TODO` or `FIXME` in production code — file issues instead
- Import order: stdlib → third-party → local (blank line between groups)
- One export per file for components; barrel exports via `__init__.py` / `index.ts`
- Prefer composition over inheritance
- Keep functions under 40 lines; extract helpers for complex logic
- Use descriptive variable names; no single-letter vars except loop indices
