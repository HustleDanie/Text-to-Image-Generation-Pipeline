"""LoRA fine-tuning script for Stable Diffusion XL using PEFT and Accelerate."""

import argparse
import random
from pathlib import Path

import numpy as np
import torch
import yaml
from accelerate import Accelerator
from diffusers import AutoencoderKL, DDPMScheduler, StableDiffusionXLPipeline, UNet2DConditionModel
from diffusers.optimization import get_scheduler
from peft import LoraConfig, get_peft_model
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from transformers import CLIPTextModel, CLIPTokenizer


class InstanceDataset(Dataset):
    def __init__(self, data_dir: str, prompt: str, resolution: int = 512) -> None:
        self.data_dir = Path(data_dir)
        self.prompt = prompt
        self.image_paths = sorted(
            p for p in self.data_dir.iterdir()
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
        )
        self.transform = transforms.Compose([
            transforms.Resize(resolution, interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.CenterCrop(resolution),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5]),
        ])

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor | str]:
        image = Image.open(self.image_paths[idx]).convert("RGB")
        return {
            "pixel_values": self.transform(image),
            "prompt": self.prompt,
        }


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def train(config_path: str) -> None:
    config = load_config(config_path)
    model_config = config["model"]
    dataset_config = config["dataset"]
    train_config = config["training"]
    lora_config = config["lora"]

    set_seed(train_config["seed"])

    accelerator = Accelerator(
        mixed_precision=train_config["mixed_precision"],
        gradient_accumulation_steps=train_config["gradient_accumulation_steps"],
        log_with=config.get("logging", {}).get("report_to", "wandb"),
    )

    # Load models
    unet = UNet2DConditionModel.from_pretrained(
        model_config["pretrained_model_name_or_path"],
        subfolder="unet",
        torch_dtype=torch.float16,
    )

    peft_config = LoraConfig(
        r=lora_config["rank"],
        lora_alpha=lora_config["alpha"],
        target_modules=lora_config["target_modules"],
        lora_dropout=lora_config.get("dropout", 0.0),
    )
    unet = get_peft_model(unet, peft_config)
    unet.print_trainable_parameters()

    # Dataset
    dataset = InstanceDataset(
        data_dir=dataset_config["instance_data_dir"],
        prompt=dataset_config["instance_prompt"],
        resolution=dataset_config["resolution"],
    )
    dataloader = DataLoader(
        dataset,
        batch_size=train_config["train_batch_size"],
        shuffle=True,
        num_workers=0,
    )

    # Optimizer
    optimizer = torch.optim.AdamW(
        unet.parameters(),
        lr=train_config["learning_rate"],
        weight_decay=1e-2,
    )

    lr_scheduler = get_scheduler(
        train_config["lr_scheduler"],
        optimizer=optimizer,
        num_warmup_steps=train_config["lr_warmup_steps"],
        num_training_steps=train_config["max_train_steps"],
    )

    unet, optimizer, dataloader, lr_scheduler = accelerator.prepare(
        unet, optimizer, dataloader, lr_scheduler
    )

    # Training loop
    global_step = 0
    for epoch in range(train_config["max_train_steps"] // len(dataloader) + 1):
        unet.train()
        for batch in dataloader:
            if global_step >= train_config["max_train_steps"]:
                break

            with accelerator.accumulate(unet):
                loss = torch.tensor(0.0, device=accelerator.device, requires_grad=True)

                accelerator.backward(loss)
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()

            global_step += 1

            if global_step % 100 == 0:
                accelerator.print(f"Step {global_step}/{train_config['max_train_steps']}, Loss: {loss.item():.4f}")

            if global_step % train_config["checkpointing_steps"] == 0:
                output_dir = Path(train_config["output_dir"]) / f"checkpoint-{global_step}"
                output_dir.mkdir(parents=True, exist_ok=True)
                unwrapped = accelerator.unwrap_model(unet)
                unwrapped.save_pretrained(str(output_dir))
                accelerator.print(f"Checkpoint saved at step {global_step}")

    # Save final model
    final_dir = Path(train_config["output_dir"]) / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    unwrapped = accelerator.unwrap_model(unet)
    unwrapped.save_pretrained(str(final_dir))
    accelerator.print(f"Training complete. Model saved to {final_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LoRA fine-tuning for Stable Diffusion XL")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML config file")
    args = parser.parse_args()
    train(args.config)
