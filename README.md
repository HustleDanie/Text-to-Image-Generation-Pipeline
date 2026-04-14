# Text-to-Image Generation Pipeline with Fine-Tuning

[![CI](https://github.com/username/text-to-image-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/username/text-to-image-pipeline/actions/workflows/ci.yml)

> Generate high-quality images from text prompts using fine-tuned Stable Diffusion XL with LoRA/DreamBooth adapters. Features an async FastAPI backend with task queue architecture and a modern Next.js 16 frontend.

## Architecture

```
Frontend (Next.js 16 on Vercel)
    │
    ├── POST /api/generate ──▶ FastAPI ──▶ TaskIQ (Redis) ──▶ GPU Worker
    │                              │                              │
    ├── GET /api/status/{id} ◀────┘   (polls Redis for status)   │
    │                                                             │
    └── GET /api/images/{id} ◀──────── (serves from storage) ◀───┘
```

**Key Design Decisions:**
- **Async job-based flow** — generation takes 5-30 seconds; never blocks the API
- **Model loaded once** per worker process, not per request
- **Safety layer** — prompt filtering + NSFW output detection + rate limiting
- **LoRA adapters** — lightweight (50-100MB) fine-tuned models, hot-swappable

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| ML Framework | PyTorch | 2.11.0 |
| Diffusion | diffusers + PEFT | 0.37.1 / 0.18.1 |
| Backend | FastAPI + TaskIQ | 0.135.3 |
| Frontend | Next.js + React | 16.2 / 19.2 |
| State | Zustand + TanStack Query | 5.x / 5.x |
| Styling | Tailwind CSS | 4.x |
| Package Mgmt | uv (Python) / npm (Node) | 0.11.x |
| Testing | pytest / vitest | latest |

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 22+
- [uv](https://docs.astral.sh/uv/) package manager
- Redis (for task queue)
- NVIDIA GPU with CUDA (for inference/training)

### Backend
```bash
cd backend
uv sync
cp .env.example .env  # configure your settings
uv run fastapi dev app/main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker (Full Stack)
```bash
docker compose up
```
Open http://localhost:3000

## Training

### LoRA Fine-Tuning
```bash
cd training
uv sync
# Place 10-30 training images in data/raw/
uv run python utils/data_preparation.py --input data/raw/ --output data/processed/
uv run accelerate launch scripts/train_lora.py --config configs/lora_default.yaml
```

### DreamBooth
```bash
uv run accelerate launch scripts/train_dreambooth.py --config configs/dreambooth_default.yaml
```

See [training/README.md](training/README.md) for detailed instructions.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/generate` | Submit image generation job |
| GET | `/api/status/{id}` | Poll job status |
| GET | `/api/images/{id}` | Retrieve generated image |
| GET | `/api/models` | List available models |
| GET | `/health` | Health check |

Full API docs at `http://localhost:8000/docs` (Swagger UI).

## Project Structure

```
├── .claude/               # Claude Code configuration
│   ├── rules/             # Path-scoped coding rules (9 files)
│   ├── skills/            # Development workflow guides (5 skills)
│   └── agents/            # Custom agents (reviewer, debugger)
├── backend/               # FastAPI + TaskIQ backend
│   ├── app/
│   │   ├── routes/        # API route handlers
│   │   ├── schemas/       # Pydantic request/response models
│   │   ├── guardrails/    # Safety: prompt filter, NSFW, rate limit
│   │   ├── ml/            # SD pipeline wrapper, LoRA manager
│   │   └── utils/         # Logging, errors, storage
│   ├── workers/           # TaskIQ async task workers
│   └── tests/             # pytest tests
├── training/              # Fine-tuning scripts
│   ├── scripts/           # train_lora.py, train_dreambooth.py, evaluate.py
│   ├── configs/           # YAML hyperparameter configs
│   └── utils/             # Data prep, metrics, callbacks
├── frontend/              # Next.js 16 frontend
│   ├── app/               # App Router pages
│   ├── components/        # React 19 components
│   ├── hooks/             # TanStack Query hooks
│   ├── stores/            # Zustand stores
│   └── lib/               # API client, types, utilities
├── .github/workflows/     # CI/CD pipelines
├── CLAUDE.md              # Project context for Claude Code
└── docker-compose.yml     # Local dev orchestration
```

## Deployment

- **Frontend**: Vercel (auto-deploy on push to main)
- **Backend**: HuggingFace Spaces with ZeroGPU (5 free GPU hours/month)

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for setup instructions.

## License

MIT
