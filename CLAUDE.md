# Text-to-Image Generation Pipeline with Fine-Tuning

## Architecture
Monorepo: `backend/` (FastAPI + TaskIQ) | `training/` (LoRA/DreamBooth) | `frontend/` (Next.js 16)

Async job-based flow:
```
POST /api/generate → TaskIQ (Redis) → GPU Worker → GET /api/status/{id} → GET /api/images/{id}
```

## Quick Start
```bash
# Backend
cd backend && uv sync && uv run fastapi dev app/main.py

# Frontend
cd frontend && npm install && npm run dev

# Training
cd training && uv sync && uv run python scripts/train_lora.py --config configs/lora_default.yaml

# Docker (full stack)
docker compose up
```

## Tech Stack
- **Python 3.12** | **uv** for deps | **ruff** for linting
- **FastAPI 0.135** + Pydantic v2 + TaskIQ (Redis) async task queue
- **diffusers 0.37** + PyTorch 2.11 + PEFT 0.18 (LoRA/DreamBooth)
- **Next.js 16.2** + React 19.2 + TypeScript + Tailwind CSS 4
- **Zustand** (client state) + **TanStack Query v5** (server state)
- **pytest** (backend) + **vitest** (frontend)

## Project Structure
```
backend/
  app/main.py          # FastAPI app with lifespan
  app/config.py        # Pydantic BaseSettings
  app/routes/           # API endpoints
  app/schemas/          # Pydantic request/response models
  app/guardrails/       # Prompt filtering, NSFW check, rate limiting
  app/ml/               # Pipeline wrapper, LoRA manager
  app/utils/            # Logging, errors, storage
  workers/              # TaskIQ broker + generation tasks
  tests/                # pytest tests
training/
  scripts/              # train_lora.py, train_dreambooth.py, evaluate.py
  configs/              # YAML hyperparameter configs
  utils/                # Data prep, metrics, callbacks
frontend/
  app/                  # Next.js App Router pages
  components/           # React components
  lib/                  # API client, types, utilities
  hooks/                # TanStack Query hooks
  stores/               # Zustand stores
```

## Conventions
- **Python**: Type hints on all functions. Use `async def` for handlers. Pydantic v2 (`model_validate`, `model_dump`). No `print()` — use structured logging.
- **TypeScript**: Strict mode. No `any`. Server Components by default; add `'use client'` only when needed.
- **Imports**: stdlib → third-party → local (separated by blank lines).
- **Commits**: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:` prefixes.
- **Tests**: Colocate with source in `tests/` dirs. AAA pattern (Arrange-Act-Assert).
- **Errors**: Custom exception classes → FastAPI exception handlers. Never expose internals.

## Key Commands
```bash
# Linting
cd backend && uv run ruff check . --fix
cd frontend && npx eslint . --fix

# Type checking
cd backend && uv run pyright
cd frontend && npx tsc --noEmit

# Testing
cd backend && uv run pytest -x -q
cd frontend && npx vitest run

# Format
cd backend && uv run ruff format .
cd frontend && npx prettier --write .
```

## Environment Variables
Backend (`.env`):
- `MODEL_ID` — HuggingFace model ID (default: `stabilityai/stable-diffusion-xl-base-1.0`)
- `REDIS_URL` — Redis connection (default: `redis://localhost:6379`)
- `DEVICE` — `cuda` or `cpu`
- `STORAGE_PATH` — generated image storage path
- `ALLOWED_ORIGINS` — CORS origins (comma-separated)

@backend/pyproject.toml
@training/pyproject.toml
@frontend/package.json
