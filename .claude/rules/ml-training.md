---
description: "ML training conventions for reproducibility and quality"
paths:
  - "training/**"
---

# ML Training Rules

## Reproducibility
- Set ALL random seeds: `torch.manual_seed()`, `random.seed()`, `np.random.seed()`
- Log full config (hyperparameters, model ID, dataset info) at training start
- Pin exact library versions in `pyproject.toml`
- Store training configs as YAML files — never hardcode hyperparameters

## Config-Driven Training
- All hyperparameters in YAML config files (`configs/`)
- CLI overrides via argparse or hydra for quick experiments
- Config schema: learning_rate, epochs, batch_size, rank, alpha, target_modules, resolution, seed

## Checkpointing
- Save checkpoints every N steps (configurable, default: 500)
- Use SafeTensors format (`.safetensors`) — faster, safer than pickle
- Include optimizer state for resumable training
- Save final adapter weights separately for inference

## LoRA Specifics
- Default rank: 4-16 (start low, increase if underfitting)
- Default alpha: same as rank (or 2x rank)
- Target modules: typically `to_q`, `to_k`, `to_v`, `to_out.0` for attention layers
- Use `fp16` mixed precision training for memory efficiency

## DreamBooth Specifics
- Use prior preservation loss to prevent language drift
- Generate class images before training (200-300 images)
- 400-800 training steps for subjects, 1000-1500 for styles
- Learning rate: 1e-6 for full fine-tune, 1e-4 for LoRA

## Evaluation
- Track metrics: FID (quality), CLIP score (text alignment), LPIPS (diversity)
- Generate validation images at regular intervals during training
- Compare against base model outputs for same prompts
