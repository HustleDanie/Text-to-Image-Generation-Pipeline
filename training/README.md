# Training Guide

## Quick Start

### 1. Install Dependencies
```bash
cd training
uv sync
```

### 2. Prepare Data
Place 10-30 training images in `data/raw/`, then:
```bash
uv run python utils/data_preparation.py --input data/raw/ --output data/processed/ --resolution 512
```

### 3. LoRA Fine-Tuning
```bash
uv run accelerate launch scripts/train_lora.py --config configs/lora_default.yaml
```

### 4. DreamBooth Fine-Tuning
```bash
uv run accelerate launch scripts/train_dreambooth.py --config configs/dreambooth_default.yaml
```

### 5. Evaluate
Create `eval_prompts.txt` with one prompt per line, then:
```bash
uv run python scripts/evaluate.py --model_path outputs/lora_default/final --prompts eval_prompts.txt
```

### 6. Upload to HuggingFace
```bash
uv run python scripts/upload_model.py --model_path outputs/lora_default/final --repo_id username/my-lora-model
```

## Tips
- **LoRA**: Best for style transfer. Fast to train (15-30 min on T4 GPU). Small adapters (~50-100MB).
- **DreamBooth**: Best for specific subjects. Longer training. Generates class images first.
- **Resolution**: Match the base model (512 for SD 1.5, 1024 for SDXL). Start with 512 even for SDXL to save memory.
- **Wandb**: Set `WANDB_API_KEY` env variable for experiment tracking.
