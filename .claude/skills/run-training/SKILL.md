---
name: run-training
description: "Fine-tuning workflow: data prep, training, evaluation, and model upload"
---

# Run Training

## Workflow

### 1. Prepare Data
```bash
# Organize images in data/{concept_name}/ (10-30 for LoRA, 20-40 for DreamBooth)
# Images should be consistent quality, diverse poses/angles, clean backgrounds
cd training && uv run python utils/data_preparation.py --input data/raw/ --output data/processed/ --resolution 512
```

### 2. Configure Hyperparameters
- Copy `configs/lora_default.yaml` → `configs/my_experiment.yaml`
- Adjust: `learning_rate`, `rank`, `max_train_steps`, `resolution`
- Set `seed` for reproducibility

### 3. Train
```bash
cd training
uv run accelerate launch scripts/train_lora.py --config configs/my_experiment.yaml
# OR for DreamBooth:
uv run accelerate launch scripts/train_dreambooth.py --config configs/dreambooth_default.yaml
```

### 4. Evaluate
```bash
cd training && uv run python scripts/evaluate.py --model_path outputs/my_experiment/ --prompts eval_prompts.txt
```
Check: FID score, CLIP alignment, visual quality of generated samples

### 5. Upload to HuggingFace Hub
```bash
cd training && uv run python scripts/upload_model.py --model_path outputs/my_experiment/ --repo_id username/model-name
```

## Troubleshooting
- **OOM**: Reduce batch size, enable gradient checkpointing, use fp16
- **Underfitting**: Increase rank, increase steps, check learning rate
- **Overfitting**: Reduce steps, increase regularization images, lower learning rate
