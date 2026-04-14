# Architecture

## System Overview

This project implements a text-to-image generation pipeline with fine-tuning capabilities using a modern async architecture.

## Data Flow

```
User Request → Next.js Frontend → FastAPI Backend → TaskIQ Broker → Redis Queue
                                                                        │
GPU Worker ◀────────────────────────────────────────────────────────────┘
    │
    ├── Load/swap LoRA adapters
    ├── Run Stable Diffusion pipeline
    ├── NSFW content check
    ├── Save image to storage
    └── Update job status in Redis
                                                                        │
User Polling → Frontend → GET /api/status/{id} → Redis ─────────────────┘
User Fetch  → Frontend → GET /api/images/{id}  → File Storage
```

## Why Async Task Queue?

Image generation takes 5-30 seconds depending on:
- Model size (SDXL = ~6.5GB VRAM)
- Number of inference steps (20-100)
- Image resolution (256x256 to 1024x1024)

Synchronous endpoints would:
- Block the API server for each request
- Hit HTTP timeout limits
- Prevent concurrent request handling

The async pattern (submit → poll → retrieve) solves all of these.

## Model Serving Pattern

```python
# Singleton pattern — model loaded ONCE per worker process
_pipeline: StableDiffusionXLPipeline | None = None

def get_pipeline() -> StableDiffusionXLPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = StableDiffusionXLPipeline.from_pretrained(...)
    return _pipeline
```

Loading a model takes 10-30 seconds and 4-7 GB memory. The singleton pattern ensures:
- Model loaded once at worker startup
- Shared across all tasks on that worker
- LoRA adapters can be hot-swapped without reloading the base model

## Safety Architecture

```
User Prompt → Prompt Filter (blocklist regex) → Task Queue → Generation
                                                                  │
                                                           NSFW Checker
                                                                  │
                                                      Safe? → Store image
                                                      NSFW? → Return error
```

Three layers:
1. **Prompt filter**: Pre-generation blocklist (regex, fast)
2. **SD Safety Checker**: Built into pipeline (during generation)
3. **Post-generation check**: Secondary content filter hook

## Technology Choices

| Choice | Alternative | Rationale |
|--------|------------|-----------|
| TaskIQ + Redis | Celery | Lighter, async-native, simpler config |
| uv | pip/poetry | 10-100x faster, modern standard |
| ruff | black+isort+flake8 | Single tool, fastest available |
| Zustand | Redux | Much simpler, fewer boilerplate |
| TanStack Query | SWR / manual fetch | Better polling, caching, devtools |
| SDXL base | SD 1.5 | Higher quality, industry standard |
| LoRA primary | Full fine-tune | 50-100MB vs 6GB, free hosting friendly |
